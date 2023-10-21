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

# Personal dependencies
import sys
sys.path.append("../../")
import constants

def aggregate_data(data):
    # Aggregate data
    # {18712: {'request': {'timestamp': '13:22:44.546969', 'host': 'unamur021', 'query_type': 'A', 'domain': 'kumparan.com', 'length': 30, 'responses': [], 'counts': None, 'query_id': 18712}, 'response': {'timestamp': '13:22:44.580851', 'host': 'one', 'query_type': 'A', 'domain': None, 'length': 62, 'responses': [('A', '104.18.130.231'), ('A', '104.18.129.231')], 'counts': (2, 0, 0), 'query_id': 18712}}}
    request = data['request']
    response = data['response']

    if len(request) == 0: # TODO: double check -> no request : There is one particular case where we have a response but no corresponding request
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

    if len(response) == 0:
        length_response = '0'
        responses = ()
        counts = None
    else:
        length_response = response['length']
        responses = response['responses']
        counts = response['counts']

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
