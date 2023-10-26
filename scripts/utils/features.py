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
        timestamp = request['timestamp']
        host = request['host']
        query_type = request['query_type']
        domain = request['domain']
        length_request = request['length']
    #### \ Request ####

    #### Response ####
    if len(response) == 0:
        length_response = '0'
        responses = ()
        counts = None
    else:
        length_response = response['length']
        responses = response['responses']
        counts = response['counts']
    #### \ Response ####

    return {
        "timestamp": timestamp,
        "host": host,
        "query_type": query_type,
        "domain": domain, 
        "length_request": length_request, 
        "length_response": length_response, 
        "responses": responses, 
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
    combined_df['timestamp'] = combined_df['timestamp'].astype('category')
    combined_df['host'] = combined_df['host'].astype('category')
    combined_df['query_type'] = combined_df['query_type'].astype('category')
    combined_df['domain'] = combined_df['domain'].astype('category')
    combined_df['length_request'] = combined_df['length_request'].astype(
        'int64')
    combined_df['length_response'] = combined_df['length_response'].astype(
        'int64')
    combined_df['responses'] = combined_df['responses'].astype('category')
    combined_df['counts'] = combined_df['counts'].astype('category')

    return combined_df


def encoding_features(combined_df):
    # Label encode categorical features
    label_encoder_timestamp = LabelEncoder()
    combined_df['timestamp_encoded'] = label_encoder_timestamp.fit_transform(
        combined_df['timestamp'])
    
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
        
        
def get_timing_for_a_session(aggregated_data):
    """
    Regroup all the requests and responses for a session and get the timing between the first request and the last response
    
        {1:
        timestamp_aggregate_data1_request
        timestamp_aggregate_datalast_response
        }
    
    """   
    timing_for_a_session = {}

    for data in aggregated_data:
        host = data['host']
        if host in timing_for_a_session:
            timing_for_a_session[host].append(parser.parse_timestamp(data['timestamp']))
        else:
            timing_for_a_session[host] = [parser.parse_timestamp(data['timestamp'])]
            
    timing_for_a_session = {key: sorted(value) for key, value in timing_for_a_session.items()} # We need to sort the timestamps to be sure that the first element is the oldest and the last element is the newest   
        
    list_of_timing_for_a_session = {}
    for key, value in timing_for_a_session.items(): # key = host and value = list of timestamps (beginning with request and ending with response)
        list_of_timing_for_a_session[key] = [value[0], value[-1]]

    # get_average_of_timing_for_a_session(list_of_timing_for_a_session) # For the report
    
    return list_of_timing_for_a_session


def get_all_requests_and_responses_for_an_host(): # host can be either bot and human
    """
    Getting all the aggregated data from the host
    
        {1:
        [aggregate_data_request1
        aggregate_data_response1],
        
        [aggregate_data_request2,
        aggregate_data_response2]
        etc
        }
    
    
    """
    pass

def get_time_between_requests(aggregated_data):
    """
    Prendre la difference des timstamps entre chaque requests/responses d'un host -> donc agréger les données en fonction des hosts et non en fonction du request ID seulement.
    """
    pass



# def get_number_of_queries_in_a_session(aggregated_data):
#     pass

def get_number_of_dots_in_a_domain(aggregated_data):
    pass



def get_number_of_requests_in_a_session(aggregated_data): 
    """ 
    Getting the nu
    
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

def frequency_of_repeated_requests_in_a_short_time_frame():
    pass

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
