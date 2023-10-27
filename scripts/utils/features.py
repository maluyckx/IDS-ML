"""
Goal of the script : Functions to convert the data to a dataframe and encode the features

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""
# ML dependencies
from sklearn.preprocessing import LabelEncoder

# Other dependencies
import pandas as pd
import itertools
from statistics import mean
import parsing_dns_trace as parser

# Personal dependencies
import sys
sys.path.append("../../")
import scripts.utils.constants as constants

def aggregate_data(data):
    """
    TODO explain function
    
    Example of data : 
    {'request': {'timestamp': '13:22:44.546969', 'host': 'unamur021', 'query_id': 18712, 'query_type': ['A'], 'domain': 'kumparan.com', 'length': 30, 'responses': None, 'counts': None}, 'response': {'timestamp': '13:22:44.580851', 'host': 'one', 'query_id': 18712, 'query_type': ['A', 'A'], 'domain': None, 'length': 62, 'responses': {'A': ['104.18.130.231', '104.18.129.231']}, 'counts': (2, 0, 0)}}
    
    """
    
    request = data['request']
    response = data['response']
    
    #### Request ####
    if len(request) == 0: # TODO: double check -> no request : There is one particular case where we have a response but no corresponding request
    # This line : 14:55:35.387285 IP one.one.one.one.domain > unamur138.47506: 10732 NXDomain 0/1/0 (120)
        
    #    timestamp = '0'
    #    host = None
    #    query_type = None
    #    domain = None
    #    length_request = '0'
        return None
    
    else:
        query_id = request['query_id']
        timestamp_req = request['timestamp']
        host = request['host']
        request_type = request['query_type']
        domain = request['domain']
        length_request = request['length']
    #### \ Request ####

    #### Response ####
    if len(response) == 0:
        timestamp_resp = '0'
        length_response = '0'
        responses = ()
        counts = None
    else:
        timestamp_resp = response['timestamp']
        length_response = response['length']
        responses = response['responses']
        counts = response['counts']
    #### \ Response ####

    return {
        ## Request
        "timestamp_req": timestamp_req,
        "host": host,
        "request_type": request_type,
        "domain": domain, 
        "length_request": length_request, 
        
        ## Request and Response
        "query_id": query_id,
        
        ## Response
        "timestamp_resp": timestamp_resp,
        # in this case, host is always one.one.one.one
        "length_response": length_response, 
        "responses": responses, # also combine the query_type : we did this because it would be really hard to map it accordingly
        "counts": counts
        }



def convert_to_dataframe(bots_data, webclients_data):
    bots = []
    for key in bots_data.keys():
        trace = aggregate_data(bots_data[key])
        if trace != None:
            bots.append(trace)

    webclients = []
    for key in webclients_data.keys():
        trace = aggregate_data(webclients_data[key])
        if trace != None:
            webclients.append(aggregate_data(webclients_data[key]))

    bots_df = pd.DataFrame(bots)
    bots_df['label'] = 'bot'

    webclients_df = pd.DataFrame(webclients)
    webclients_df['label'] = 'human'

    # Combine the two datasets
    combined_df = pd.concat([bots_df, webclients_df], ignore_index=True)

    # Convert categorical features to numerical
    ## Request
    combined_df['timestamp_req'] = combined_df['timestamp_req'].astype('category')
    combined_df['host'] = combined_df['host'].astype('category')
    combined_df['request_type'] = combined_df['request_type'].astype('category')
    combined_df['domain'] = combined_df['domain'].astype('category')
    combined_df['length_request'] = combined_df['length_request'].astype('int64')
    
    ## Request and Response
    # combined_df['query_id'] = combined_df['query_id'].astype('int64')
    
    ## Response
    combined_df['length_response'] = combined_df['length_response'].astype('int64')
    combined_df['responses'] = combined_df['responses'].astype('category')
    combined_df['counts'] = combined_df['counts'].astype('category')

    return combined_df


def encoding_features(combined_df):
    """
    Encode categorical features of the input DataFrame using LabelEncoder.
    
    """
    label_encoder_timestamp = LabelEncoder()
    combined_df['timestamp_encoded'] = label_encoder_timestamp.fit_transform(
        combined_df['timestamp_req'])
    
    label_encoder_host = LabelEncoder()
    combined_df['host_encoded'] = label_encoder_host.fit_transform(
        combined_df['host'])
    
    label_encoder_query_type = LabelEncoder()
    combined_df['query_type_encoded'] = label_encoder_query_type.fit_transform(
        combined_df['query_type'].astype(str))

    label_encoder_domain = LabelEncoder()
    combined_df['domain_encoded'] = label_encoder_domain.fit_transform(
        combined_df['domain'])

    label_encoder_length_request = LabelEncoder()
    combined_df['length_request_encoded'] = label_encoder_length_request.fit_transform(
        combined_df['length_request'])

    label_encoder_length_response = LabelEncoder()
    combined_df['length_response_encoded'] = label_encoder_length_response.fit_transform(
        combined_df['length_response'])

    label_encoder_responses = LabelEncoder()
    combined_df['responses_encoded'] = label_encoder_responses.fit_transform(
            combined_df['responses'])

    label_encoder_counts = LabelEncoder()
    combined_df['counts_encoded'] = label_encoder_counts.fit_transform(
        combined_df['counts'])

    return combined_df



############################################################################################################
# Functions to get new features by combining/aggregating the existing ones
############################################################################################################


def get_all_hosts(aggregated_data):
    """
    Getting all the hosts from the dataset
    """
    
    set_of_hosts = set()
    for i in range(len(aggregated_data)):
        set_of_hosts.add(aggregated_data[i]['host'])

    return set_of_hosts


def get_average_of_timing_for_a_session(list_of_timing_for_a_session):
    list_of_average_of_timing_for_a_session = []
    for key, value in list_of_timing_for_a_session.items():
        difference = value[1] - value[0]
        difference_in_seconds = difference.total_seconds()
    
        #print(f"Average of timing for {key} : {difference_in_seconds}")
        list_of_average_of_timing_for_a_session.append(difference_in_seconds)
        
    print(mean(list_of_average_of_timing_for_a_session))
     
     
     
# def get_average_of_query_length(aggregated_data):
#     """
#     Getting the average of the query length for each host
    
#     """
#     query_length_by_host = {}
#     for data in aggregated_data:
#         host = data['host']
#         if host in query_length_by_host:
#             query_length_by_host[host].append((data['length_request'], data['length_response']))
#         else:
#             query_length_by_host[host] = [(data['length_request'], data['length_response'])]

#     # mean of the request query length for each host



#     average_of_request_length = {key: mean(value[0]) for key, value in query_length_by_host.items()}
#     average_of_response_length = {key: mean(value[1]) for key, value in query_length_by_host.items()}

#     print("Average of request length : ", average_of_request_length)
#     print()
#     print("Average of response length : ", average_of_response_length)
    
#     return average_of_request_length, average_of_response_length

def get_average_of_query_length(aggregated_data):
    """
    Getting the average of the query length for each host
    """
    query_length_by_host = {}
    for data in aggregated_data:
        host = data['host']
        if host in query_length_by_host:
            query_length_by_host[host].append((data['length_request'], data['length_response']))
        else:
            query_length_by_host[host] = [(data['length_request'], data['length_response'])]

    average_of_request_length = {key: mean([int(x[0]) for x in value]) for key, value in query_length_by_host.items()}
    average_of_response_length = {key: mean([int(x[1]) for x in value]) for key, value in query_length_by_host.items()}

    print("Average of request length : ", average_of_request_length) 
    print()
    print("Average of response length : ", average_of_response_length)
    
    ## Bots
    # Requests : =~ 30
    # Response : =~ entre 60 et 70
    ## Webclients
    # Requests : =~ 40
    # Response : =~ pas vraiment de moyenne, c'est full variable


    return average_of_request_length, average_of_response_length

def get_type_of_requests_queried_by_hosts(aggregated_data):
    """
    Par exemple, les bots font que des queries A et AAAA donc ca peut etre intéressant de checker ce pattern
    
    """
    
    pass
   
   
def get_type_of_responses_received_by_hosts(aggregated_data):   
    """
    Maybe the response type is also interesting ?? (response type received by each host)
    """
    
    pass

   
        
def get_timing_of_all_queries(aggregated_data): # NOT A FEATURE, JUST A USEFUL FUNCTION FOR THE TIMINGS
    """
    Getting all the timestamps of all requests and responses for each host
    
    """
    
    timing_of_all_queries = {}

    for data in aggregated_data:
        host = data['host']
        
        timestamp_req = parser.parse_timestamp(data['timestamp_req'])
        if data['timestamp_resp'] == '0': # ATTENTION : whenever the response is not present, we discard the request => IT IS AN ADDITIONAL ASSUMPTION THAT WE MAKE, it can impact the model if the traffic is composed of a lot of requests without responses (and thus the model might behave differently)
            continue
        timestamp_resp = parser.parse_timestamp(data['timestamp_resp'])
        
        if host in timing_of_all_queries:
            timing_of_all_queries[host].append((timestamp_req, timestamp_resp))
        else:
            timing_of_all_queries[host] = [(timestamp_req, timestamp_resp)]
            
    timing_of_all_queries = {key: sorted(value) for key, value in timing_of_all_queries.items()} # We need to sort the timestamps to be sure that the first element is the oldest and the last element is the newest       
    
    return timing_of_all_queries
        
def get_timing_for_a_session(aggregated_data):
    """
    Regroup all the requests and responses for a session and get the timing between the first request and the last response
    
        {1:
        timestamp_aggregate_data1_request
        timestamp_aggregate_datalast_response
        }
    
    """   
    timing_for_a_session = get_timing_of_all_queries(aggregated_data)
    
    list_of_timing_for_a_session = {}
    for key, value in timing_for_a_session.items(): # key = host and value = list of timestamps (beginning with request and ending with response)
        list_of_timing_for_a_session[key] = [value[0][0], value[-1][1]] # value[0][0] : first timestamp_request of the fist timestamp_tuple and value[-1][1] : last timestamp_response of the last timestamp_tuple

    # get_average_of_timing_for_a_session(list_of_timing_for_a_session) # For the report
    
    print(list_of_timing_for_a_session)
    
    return list_of_timing_for_a_session


def get_all_requests_and_responses_for_an_host(aggregated_data): # WILL NOT BE USED DIRECTLY HAS A FEATURE
    """
    Getting all the aggregated data from the host
    
    unamur021 : 
            {
            {QUERY_ID: REQUEST AND RESPONSE AGGREGATED}, 
            {QUERY_ID: REQUEST AND RESPONSE AGGREGATED},
            }, 
    """
    
    requests_and_responses_per_host = {}
    for data in aggregated_data:
        host = data['host']
        if host in requests_and_responses_per_host:
            requests_and_responses_per_host[host][data['query_id']] = data
        else:
            requests_and_responses_per_host[host] = {data['query_id']: data}
    
    
    # beautiful print
    for key, value in requests_and_responses_per_host.items():
        print(f"{key} : \n {value} \n \n")
    

def get_time_between_requests(aggregated_data):
    """
    Prendre la difference des timestamps entre chaque requests/responses d'un host -> donc agréger les données en fonction des hosts et non en fonction du request ID seulement.
    
    En gros, après combien de temps un host fait une nouvelle requête ? 
    
    """
    timing_for_a_session = get_timing_of_all_queries(aggregated_data)  

    # for each adjacent timestamp, compute the difference between them 
    time_between_requests = {}
    for key, value in timing_for_a_session.items():
        time_between_requests[key] = []
        for i in range(len(value)-1):
            difference = value[i+1][0] - value[i][0]
            difference_in_seconds = difference.total_seconds()
            time_between_requests[key].append(difference_in_seconds)
    
    print(time_between_requests)




# def get_number_of_domains_queried_by_hosts(aggregated_data): # maybe intéressant, voir si c'est pas la meme chose que get_number_of_requests_in_a_session
#     """
#     Getting the number of domains queried by each host during a session
    
#     """
    
#     pass



def frequency_of_repeated_requests_in_a_short_time_frame():
    pass



def get_number_of_dots_in_a_domain(aggregated_data):
    """
    This function is used to get the number of dots in the domains queried by each host.
    
    We removed one dot because in every request, the root domain is included.
    
    """
    number_of_dots_domains = {}
    for data in aggregated_data:
        host = data['host']
        if host in number_of_dots_domains:
            number_of_dots_domains[host].append(data['domain'].count("."))
        else:
            number_of_dots_domains[host] = [data['domain'].count(".")]
    
    # beautiful print
    for key, value in number_of_dots_domains.items():
        print(f"{key} : \n {value} \n \n")


    # TODO when we decided the model, we either need to choose one of the 2 options
    # 1. on averaged sur la moyenne du nombres de dots et on passe ça en paramètre pour l'host
    # 2. on donne complétement les données brutes PAR aggrégation de request/response

def get_number_of_requests_in_a_session(aggregated_data): 
    """ 
    Getting the number of requests in a session for each host
    
    """
    get_number_of_requests = {}
    for data in aggregated_data:
        host = data['host']
        if host in get_number_of_requests:
            get_number_of_requests[host] += 1
        else:
            get_number_of_requests[host] = 1
    
    print(get_number_of_requests)
    

def get_number_of_unique_domains(aggregated_data): # and we should also get the ratio of those domains
    """
    Pour chaque host, on regarde les domains qui query et on fait un set de ces domains et puis on fait un len de chaque host
    """

    number_of_unique_domains = {}
    for data in aggregated_data:
        host = data['host']
        if host in number_of_unique_domains:
            number_of_unique_domains[host].add(data['domain'])
        else:
            number_of_unique_domains[host] = {data['domain']}

    # beautiful print
    for key, value in number_of_unique_domains.items():
        print(f"{key} : \n {value} \n \n")

    number_of_unique_domains = {key: len(value) for key, value in number_of_unique_domains.items()}  
        
    print(number_of_unique_domains)

############################################################################################################
# \ Functions to get new features by combining/aggregating the existing ones
############################################################################################################

############################################################################################################
# \ Functions to get new features by combining/aggregating the existing ones
############################################################################################################

def combinations_of_features():
    all_combinations = []
    for r in range(1, len(constants.LIST_OF_FEATURES) + 1):
        combinations = itertools.combinations(constants.LIST_OF_FEATURES, r)
        all_combinations.extend(combinations)

    all_combinations = [list(combination) for combination in all_combinations]

    # print(len(all_combinations))
    # for combination in all_combinations:
    #     print(combination)
    return all_combinations
