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
import itertools # for combinations

# Personal dependencies
import sys

sys.path.append("./features/")
import features_time as features_time
import features_numbers as features_numbers
import features_misc as features_misc


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
    if len(request) == 0: # No request : There is one particular case where we have a response but no corresponding request
    # In eval2_tcpdump.txt : 14:55:35.387285 IP one.one.one.one.domain > unamur138.47506: 10732 NXDomain 0/1/0 (120)
        
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
        responses = {}
        counts = (0,0,0)
    else:
        timestamp_resp = response['timestamp']
        # in this project, host response is always one.one.one.one
        # There is no domain in the response
        length_response = response['length']
        responses = response['responses'] # also combine the query_type : we did this because it would be really hard to map it accordingly
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
        "length_response": length_response, 
        "responses": responses,
        "counts": counts
        }


def get_all_hosts(aggregated_data):
    """
    Getting all the hosts from the dataset
    """

    set_of_hosts = set()
    for i in range(len(aggregated_data)):
        set_of_hosts.add(aggregated_data[i]['host'])

    return set_of_hosts


def generate_features(all_hosts, data):
    """
    Combining the raw features of the datasets to create new, more relevant features.
    
    This function will be called with :
    1) bots datasets 
    2) webclients datasets
    3) evaluation datasets
    """
    ## Features MISC
    average_of_request_length, average_of_response_length = features_misc.get_average_of_query_length(data)
    type_of_requests_queried_by_hosts = features_misc.get_type_of_requests_queried_by_hosts(data)
    type_of_responses_received_by_hosts = features_misc.get_type_of_responses_received_by_hosts(data)

    ## Features TIME
    get_all_timing_for_each = features_time.get_timing_for_a_session(data)
    get_average_time_between_requests = features_time.get_average_time_between_requests(data)
    frequency_of_repeated_requests_in_a_short_time_frame = features_time.frequency_of_repeated_requests_in_a_short_time_frame(data)

    ## Features NUMBERS
    average_number_of_dots_in_a_domain = features_numbers.get_average_number_of_dots_in_a_domain(data)
    number_of_requests_in_a_session = features_numbers.get_number_of_requests_in_a_session(data)
    number_of_unique_domains = features_numbers.get_number_of_unique_domains(data)
    average_counts = features_numbers.get_average_counts(data)

    features = {}

    for host in all_hosts:
        features[host] = {}
        ## Features MISC
        features[host]['average_of_request_length'] = average_of_request_length[host]
        features[host]['average_of_response_length'] = average_of_response_length[host]
        features[host]['type_of_requests_queried_by_hosts'] = tuple(type_of_requests_queried_by_hosts[host]) # Convert in list to be able to use 'category' in the dataframe, see convert_features_to_numerical()
        features[host]['type_of_responses_received_by_hosts'] = tuple(type_of_responses_received_by_hosts[host]) # Convert in list to be able to use 'category' in the dataframe, see convert_features_to_numerical()
        
        ## Features TIME 
        features[host]['average_time_for_a_session'] = get_all_timing_for_each[host]
        features[host]['average_time_between_requests'] = get_average_time_between_requests[host]
        features[host]['frequency_of_repeated_requests_in_a_short_time_frame'] = frequency_of_repeated_requests_in_a_short_time_frame[host]
        
        ## Features NUMBERS
        features[host]['average_number_of_dots_in_a_domain'] = average_number_of_dots_in_a_domain[host]
        features[host]['number_of_requests_in_a_session'] = number_of_requests_in_a_session[host]
        features[host]['number_of_unique_domains'] = number_of_unique_domains[host]
        features[host]['average_counts'] = average_counts[host]

    return features

def removing_hosts_from_features(features):
    """
    Removing the hosts (that are the keys of the feature dictionary) to have a list of features that are not dependent on the host (since the machine learning algorithm should not depend on the host)
    
    """
    return list(features.values())


def convert_features_to_numerical(combined_df):
    """
    Convert the features to numerical values to be able to use them in the machine learning algorithms.
    
    Example of combined_df :
    {
    'average_of_request_length': 28.3, 
    
    'average_of_response_length': 55.5, 
    
    'type_of_requests_queried_by_hosts': ['A'], 
    
    'type_of_responses_received_by_hosts': ['A'],
    
    'average_time_for_a_session': datetime.timedelta(seconds=940, microseconds=805515), 
    
    'average_time_between_requests': 49.515360578947366, 
    
    'frequency_of_repeated_requests_in_a_short_time_frame': 0, 
    
    'average_number_of_dots_in_a_domain': 1.15,
    
    'number_of_requests_in_a_session': 20,
    
    'number_of_unique_domains': 20, 
    
    'average_counts': 1.7
    }
    """
    
    ## Features MISC
    combined_df['average_of_request_length'] = combined_df['average_of_request_length'].astype('float64')
    combined_df['average_of_response_length'] = combined_df['average_of_response_length'].astype('float64')
    combined_df['type_of_requests_queried_by_hosts'] = combined_df['type_of_requests_queried_by_hosts']
    combined_df['type_of_responses_received_by_hosts'] = combined_df['type_of_responses_received_by_hosts']
    
    ## Features TIME
    combined_df['average_time_for_a_session'] = combined_df['average_time_for_a_session'].astype('float64')
    combined_df['average_time_between_requests'] = combined_df['average_time_between_requests'].astype('float64')
    combined_df['frequency_of_repeated_requests_in_a_short_time_frame'] = combined_df['frequency_of_repeated_requests_in_a_short_time_frame'].astype('float64')
    
    ## Features NUMBERS
    combined_df['average_number_of_dots_in_a_domain'] = combined_df['average_number_of_dots_in_a_domain'].astype('float64')
    combined_df['number_of_requests_in_a_session'] = combined_df['number_of_requests_in_a_session'].astype('float64')
    combined_df['number_of_unique_domains'] = combined_df['number_of_unique_domains'].astype('float64')
    combined_df['average_counts'] = combined_df['average_counts'].astype('float64')
    
    return combined_df


def encoding_features(combined_df):
    """
    Encode categorical features of the input DataFrame using LabelEncoder.    
    """

    ### Create a label encoder objects
    ## Features MISC
    label_encoder_average_of_request_length = LabelEncoder()
    label_encoder_average_of_response_length = LabelEncoder()
    label_encoder_type_of_requests_queried_by_hosts = LabelEncoder()
    label_encoder_type_of_responses_received_by_hosts = LabelEncoder()
    ## Features TIME
    label_encoder_average_time_for_a_session = LabelEncoder()
    label_encoder_average_time_between_requests = LabelEncoder()
    label_encoder_frequency_of_repeated_requests_in_a_short_time_frame = LabelEncoder()
    ## Features NUMBERS
    label_encoder_average_number_of_dots_in_a_domain = LabelEncoder()
    label_encoder_number_of_requests_in_a_session = LabelEncoder()
    label_encoder_number_of_unique_domains = LabelEncoder()
    label_encoder_average_counts = LabelEncoder()
    
    ### Fit the label encoder objects
    ## Features MISC
    combined_df['average_of_request_length_encoded'] = label_encoder_average_of_request_length.fit_transform(combined_df['average_of_request_length'])
    combined_df['average_of_response_length_encoded'] = label_encoder_average_of_response_length.fit_transform(combined_df['average_of_response_length'])
    combined_df['type_of_requests_queried_by_hosts_encoded'] = label_encoder_type_of_requests_queried_by_hosts.fit_transform(combined_df['type_of_requests_queried_by_hosts'])
    combined_df['type_of_responses_received_by_hosts_encoded'] = label_encoder_type_of_responses_received_by_hosts.fit_transform(combined_df['type_of_responses_received_by_hosts'])
    ## Features TIME
    combined_df['average_time_for_a_session_encoded'] = label_encoder_average_time_for_a_session.fit_transform(combined_df['average_time_for_a_session'])
    combined_df['average_time_between_requests_encoded'] = label_encoder_average_time_between_requests.fit_transform(combined_df['average_time_between_requests'])
    combined_df['frequency_of_repeated_requests_in_a_short_time_frame_encoded'] = label_encoder_frequency_of_repeated_requests_in_a_short_time_frame.fit_transform(combined_df['frequency_of_repeated_requests_in_a_short_time_frame'])
    ## Features NUMBERS
    combined_df['average_number_of_dots_in_a_domain_encoded'] = label_encoder_average_number_of_dots_in_a_domain.fit_transform(combined_df['average_number_of_dots_in_a_domain'])
    combined_df['number_of_requests_in_a_session_encoded'] = label_encoder_number_of_requests_in_a_session.fit_transform(combined_df['number_of_requests_in_a_session'])
    combined_df['number_of_unique_domains_encoded'] = label_encoder_number_of_unique_domains.fit_transform(combined_df['number_of_unique_domains'])
    combined_df['average_counts_encoded'] = label_encoder_average_counts.fit_transform(combined_df['average_counts'])

    return combined_df


#######################################
## Training part
#######################################

def convert_to_dataframe_training(bots_data, webclients_data):
    
    ## Aggregate the data ##
    bots = []
    for key in bots_data.keys():
        trace = aggregate_data(bots_data[key])
        if trace != None:
            bots.append(trace)

    webclients = []
    for key in webclients_data.keys():
        trace = aggregate_data(webclients_data[key])
        if trace != None:
            webclients.append(trace)
    ## \ Aggregate the data ##

    ## Combine raw features to create relevant features ##
    all_bot_hosts = get_all_hosts(bots)
    all_webclients_hosts = get_all_hosts(webclients) 

    bots_features = generate_features(all_bot_hosts, bots)
    webclients_features = generate_features(all_webclients_hosts, webclients)
    
    bots_features = removing_hosts_from_features(bots_features)
    webclients_features = removing_hosts_from_features(webclients_features)
    ## \ Combine raw features to create relevant features ##
    
    ## Label the data ##
    bots_features_df = pd.DataFrame(bots_features)
    bots_features_df['label'] = 'bot'

    webclients_features_df = pd.DataFrame(webclients_features)
    webclients_features_df['label'] = 'human'
    ## \ Label the data ##

    ## Combine the two datasets ##
    combined_df = pd.DataFrame(bots_features_df)
    combined_df = combined_df.append(pd.DataFrame(webclients_features_df), ignore_index=True)
    ## \ Combine the two datasets ##
    
    ## Convert the features to numerical values ##
    combined_df = convert_features_to_numerical(combined_df)
    ## \ Convert the features to numerical values ##

    return combined_df

#######################################
##  \ Training part
#######################################


#######################################
## Evaluation part
#######################################

def read_botlist(path_to_botlist):
    """
    Read the botlist from the file
    """
    botlist = []
    with open(path_to_botlist, 'r') as file:
        for line in file:
            botlist.append(line.strip())
    return botlist

def get_associated_botlist(path_to_eval_dataset):
    """
    Get the botlist associated to the evaluation data
    """
    filename = str(path_to_eval_dataset).split('/')[-1]
    eval_data = filename.split('_')[0]
    return constants.PATH_TO_BOTLISTS + eval_data + "_botlist.txt"


def convert_to_dataframe_testing(eval_data, path_to_eval_dataset):
    eval_list = []
    for key in eval_data.keys():
        trace = aggregate_data(eval_data[key])
        if trace != None:
            eval_list.append(trace)

    all_eval_hosts = get_all_hosts(eval_list)

    # Evaluation phase : read the real labels for the evaluation data
    botlist = read_botlist(get_associated_botlist(path_to_eval_dataset))

    # Generate features for the evaluation data
    eval_features = generate_features(all_eval_hosts, eval_list)

    for host in all_eval_hosts:
        eval_features[host]['host'] = host
    eval_features = removing_hosts_from_features(eval_features)

    # Find the label for each host
    for i in range(len(eval_features)):
        if eval_features[i]['host'] in botlist:
            eval_features[i]['label'] = 'bot'
        else:
            eval_features[i]['label'] = 'human'
    bots_features_df = pd.DataFrame(eval_features)

    combined_df = convert_features_to_numerical(bots_features_df)

    return combined_df

#######################################
## \ Evaluation part
#######################################


#######################################
# Functions to get new features by combining/aggregating the existing ones
#######################################

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
