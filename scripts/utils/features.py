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
        responses = {}
        counts = (0,0,0)
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


def get_all_hosts(aggregated_data):
    """
    Getting all the hosts from the dataset
    """

    set_of_hosts = set()
    for i in range(len(aggregated_data)):
        set_of_hosts.add(aggregated_data[i]['host'])

    return set_of_hosts



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
            webclients.append(trace)

    all_bot_hosts = get_all_hosts(bots)
    all_webclients_hosts = get_all_hosts(webclients) 
    
    
    ## Features MISC
    #
    average_of_request_length_bots, average_of_response_length_bots = features_misc.get_average_of_query_length(bots)
    average_of_request_length_webclients, average_of_response_length_webclients = features_misc.get_average_of_query_length(webclients)
    #
    type_of_requests_queried_by_hosts_bots = features_misc.get_type_of_requests_queried_by_hosts(bots)
    type_of_requests_queried_by_hosts_webclients = features_misc.get_type_of_requests_queried_by_hosts(webclients)
    #
    type_of_responses_received_by_hosts_bots = features_misc.get_type_of_responses_received_by_hosts(bots)
    type_of_responses_received_by_hosts_webclients = features_misc.get_type_of_responses_received_by_hosts(webclients)
    #
    
    ## Features TIME
    get_all_timing_for_each_bots = features_time.get_timing_for_a_session(bots)
    get_all_timing_for_each_webclients = features_time.get_timing_for_a_session(webclients)
    #
    get_time_between_requests_bots = features_time.get_time_between_requests(bots)
    get_time_between_requests_webclients = features_time.get_time_between_requests(webclients)
    #
    frequency_of_repeated_requests_in_a_short_time_frame_bots = features_time.frequency_of_repeated_requests_in_a_short_time_frame(bots)
    frequency_of_repeated_requests_in_a_short_time_frame_webclients = features_time.frequency_of_repeated_requests_in_a_short_time_frame(webclients)
    #

    ## Features NUMBERS
    number_of_dots_in_a_domain_bots = features_numbers.get_number_of_dots_in_a_domain(bots)
    number_of_dots_in_a_domain_webclients = features_numbers.get_number_of_dots_in_a_domain(webclients)
    #
    number_of_requests_in_a_session_bots = features_numbers.get_number_of_requests_in_a_session(bots)
    number_of_requests_in_a_session_webclients = features_numbers.get_number_of_requests_in_a_session(webclients)
    #
    number_of_unique_domains_bots = features_numbers.get_number_of_unique_domains(bots)
    number_of_unique_domains_webclients = features_numbers.get_number_of_unique_domains(webclients)
    #
    average_counts_bots = features_numbers.get_average_counts(bots)
    average_counts_webclients = features_numbers.get_average_counts(webclients)
    #

    bots_features = {}
    webclients_features = {}
    
    for host in all_bot_hosts:
        bots_features[host] = {}
        ## Features MISC
        bots_features[host]['average_of_request_length'] = average_of_request_length_bots[host]
        bots_features[host]['average_of_response_length'] = average_of_response_length_bots[host]
        bots_features[host]['type_of_requests_queried_by_hosts'] = type_of_requests_queried_by_hosts_bots[host]
        bots_features[host]['type_of_responses_received_by_hosts'] = type_of_responses_received_by_hosts_bots[host]
        
        ## Features TIME 
        bots_features[host]['average_time_for_a_session'] = get_all_timing_for_each_bots[host]
        bots_features[host]['time_between_requests'] = get_time_between_requests_bots[host]
        bots_features[host]['frequency_of_repeated_requests_in_a_short_time_frame'] = frequency_of_repeated_requests_in_a_short_time_frame_bots[host]
        
        ## Features NUMBERS
        bots_features[host]['number_of_dots_in_a_domain'] = number_of_dots_in_a_domain_bots[host]
        bots_features[host]['number_of_requests_in_a_session'] = number_of_requests_in_a_session_bots[host]
        bots_features[host]['number_of_unique_domains'] = number_of_unique_domains_bots[host]
        bots_features[host]['average_counts'] = average_counts_bots[host]

    for host in all_webclients_hosts:
        webclients_features[host] = {}
        ## Features MISC
        webclients_features[host]['average_of_request_length'] = average_of_request_length_webclients[host]
        webclients_features[host]['average_of_response_length'] = average_of_response_length_webclients[host]
        webclients_features[host]['type_of_requests_queried_by_hosts'] = type_of_requests_queried_by_hosts_webclients[host]
        webclients_features[host]['type_of_responses_received_by_hosts'] = type_of_responses_received_by_hosts_webclients[host]
        
        ## Features TIME 
        webclients_features[host]['average_time_for_a_session'] = get_all_timing_for_each_webclients[host]
        webclients_features[host]['time_between_requests'] = get_time_between_requests_webclients[host]
        webclients_features[host]['frequency_of_repeated_requests_in_a_short_time_frame'] = frequency_of_repeated_requests_in_a_short_time_frame_webclients[host]
        
        ## Features NUMBERS
        webclients_features[host]['number_of_dots_in_a_domain'] = number_of_dots_in_a_domain_webclients[host]
        webclients_features[host]['number_of_requests_in_a_session'] = number_of_requests_in_a_session_webclients[host]
        webclients_features[host]['number_of_unique_domains'] = number_of_unique_domains_webclients[host]
        webclients_features[host]['average_counts'] = average_counts_webclients[host]   
        
    print(bots_features)
    print(webclients_features)


    #####################################
    # ## Features MISC
    # "average_of_request_length",
    # "average_of_response_length",
    # "type_of_requests_queried_by_hosts",
    # "type_of_responses_received_by_hosts",
    
    # ## Features TIME 
    # "average_time_for_a_session",
    # "time_between_requests",
    # "frequency_of_repeated_requests_in_a_short_time_frame",
    
    # ## Features NUMBERS
    # "number_of_dots_in_a_domain",
    # "number_of_requests_in_a_session",
    # "number_of_unique_domains"
    # "average_counts"
    # #####################################

    
    
    
    
    
    # bots_df = pd.DataFrame(bots)
    # bots_df['label'] = 'bot'

    # webclients_df = pd.DataFrame(webclients)
    # webclients_df['label'] = 'human'



    

    # # --------------

    # # Combine the two datasets
    # combined_df = pd.concat([bots_df, webclients_df], ignore_index=True)

    # # Convert categorical features to numerical
    # ## Request
    # combined_df['timestamp_req'] = combined_df['timestamp_req'].astype('category')
    # combined_df['host'] = combined_df['host'].astype('category')
    # combined_df['request_type'] = combined_df['request_type'].astype('category')
    # combined_df['domain'] = combined_df['domain'].astype('category')
    # combined_df['length_request'] = combined_df['length_request'].astype('int64')
    
    # ## Request and Response
    # # combined_df['query_id'] = combined_df['query_id'].astype('int64')
    
    # ## Response
    # combined_df['length_response'] = combined_df['length_response'].astype('int64')
    # combined_df['responses'] = combined_df['responses'].astype('category')
    # combined_df['counts'] = combined_df['counts'].astype('category')

    # return combined_df


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
