"""
Goal of the script : Using a decision tree classifier to detect bots in a network traffic trace 

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

import pandas as pd
import re

import sys
sys.path.append("../../")
import constants
import parsing_dns_trace as parser

# import for testing
import time

def parsing_file(traces):
    """Pair DNS traces based on their IDs using the adjusted parser."""
    paired_data = {}
    
    for trace in traces:
        parsed_trace = parser.parse_dns_trace(trace)
        
        # Check if ID is present and valid
        trace_id = parsed_trace.get("request_id")
        if trace_id is None:
            continue

        # Initialize dictionary for the ID if not present
        if trace_id not in paired_data:
            paired_data[trace_id] = {"request": {}, "response": {}}  # Initialize dictionary for the ID

        # Determine if the trace is a request or response based on the domain (if "one" or not)
        if parsed_trace["host"] == "one":
            trace_type = "response"
        else:
            trace_type = "request"

        paired_data[trace_id][trace_type] = parsed_trace

        # if no request at the end, delete the ID
        if trace_type == 'request' and paired_data[trace_id]['response'] == {}:
            del paired_data[trace_id]

    return paired_data


def parse_training_data(path_to_bots_tcpdump, path_to_webclients_tcpdump):
    # Parse both datasets
    bots_data = {}
    with open(path_to_bots_tcpdump, 'r') as file:
        bots_data = parsing_file(file)
    
    webclients_data = []
    with open(path_to_webclients_tcpdump, 'r') as file:
        webclients_data = parsing_file(file)

    return bots_data, webclients_data


def aggregate_data(data):
    # Aggregate data
    # {18712: {'request': {'timestamp': '13:22:44.546969', 'host': 'unamur021', 'query_type': 'A', 'domain': 'kumparan.com', 'length': 30, 'responses': [], 'counts': None, 'request_id': 18712}, 'response': {'timestamp': '13:22:44.580851', 'host': 'one', 'query_type': 'A', 'domain': None, 'length': 62, 'responses': [('A', '104.18.130.231'), ('A', '104.18.129.231')], 'counts': (2, 0, 0), 'request_id': 18712}}}

    # TODO: double check -> no responses

    request = data['request']
    response = data['response']

    print(data)
    print(request)
    print(response)

    timestamp = request['timestamp']
    host = request['host']
    query_type = request['query_type']
    domain = request['domain']
    length_request = request['length']

    if len(response) == 0:
        length_response = 0
        responses = ()
        counts = None
    else:
        length_response = response['length']
        responses = response['responses']
        counts = response['counts']

    return {"timestamp": timestamp, "host": host, "query_type": query_type, "domain": domain, "length_request": length_request,"length_response": length_response,"responses": responses,"counts": counts}


def convert_to_dataframe(bots_data, webclients_data):
    # Convert to DataFrame

    bots = []

    for key in bots_data.keys():
        bots.append(aggregate_data(bots_data[key]))

    webclients = []
    
    for key in webclients_data.keys():
        webclients.append(aggregate_data(webclients_data[key]))

    bots_df = pd.DataFrame(bots)
    bots_df['label'] = 'bot'

    print(bots_df)

    webclients_df = pd.DataFrame(webclients)
    webclients_df['label'] = 'human'

    # Combine the two datasets
    combined_df = pd.concat([bots_df, webclients_df], ignore_index=True)

    # Convert categorical features to numerical
    combined_df['query_type'] = combined_df['query_type'].astype('category')
    combined_df['domain'] = combined_df['domain'].astype('category')
    combined_df['host'] = combined_df['host'].astype('category')
    combined_df['timestamp'] = combined_df['timestamp'].astype('category')
    combined_df['length_request'] = combined_df['length_request'].astype('int64')
    combined_df['length_response'] = combined_df['length_response'].astype('int64')
    combined_df['responses'] = combined_df['responses'].astype('category')
    combined_df['counts'] = combined_df['counts'].astype('category')
    
    return combined_df


def encoding_features(combined_df):
    # Label encode categorical features
    label_encoder_query_type = LabelEncoder()
    combined_df['query_type_encoded'] = label_encoder_query_type.fit_transform(
        combined_df['query_type'].astype(str))

    label_encoder_domain = LabelEncoder()
    combined_df['domain_encoded'] = label_encoder_domain.fit_transform(
        combined_df['domain'])

    label_encoder_host = LabelEncoder()
    combined_df['host_encoded'] = label_encoder_host.fit_transform(
        combined_df['host'])

    label_encoder_timestamp = LabelEncoder()
    combined_df['timestamp_encoded'] = label_encoder_timestamp.fit_transform(
        combined_df['timestamp'])

    label_encoder_length_request = LabelEncoder()
    combined_df['length_request_encoded'] = label_encoder_length_request.fit_transform(
        combined_df['length_request'])

    label_encoder_length_response = LabelEncoder()
    combined_df['length_response_encoded'] = label_encoder_length_response.fit_transform(
        combined_df['length_response'])
    
    label_encoder_responses = LabelEncoder()
    combined_df['responses_encoded'] = label_encoder_responses.fit_transform(
        combined_df['responses'])

    return combined_df


def train_decision_tree(combined_df):

    # Split the data into training and testing sets
    list_of_features = ['query_type_encoded',
                        'domain_encoded', 'host_encoded', 'timestamp_encoded', 'length_request_encoded', 'length_response_encoded', 'responses_encoded']
    
    X = combined_df[list_of_features]
    y = combined_df['label']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # Train the decision tree classifier
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    # clf.fit(X, y)

    return clf, X_test, y_test


def testing_eval(path_to_test_tcpdump, path_to_test_tcpdump2,  clf):

    eval_data1, eval_data2 = parse_training_data(
        path_to_test_tcpdump, path_to_test_tcpdump2)

    combined_df = convert_to_dataframe(eval_data1, eval_data2)

    combined_df = encoding_features(combined_df)

    list_of_features = ['query_type_encoded',
                        'domain_encoded', 'host_encoded', 'timestamp_encoded', 'length_request_encoded', 'length_response_encoded', 'responses_encoded']

    X_test = combined_df[list_of_features]
    y_test = combined_df['label']

    return X_test, y_test


def main_decision_tree():
    # Use a first dataset to train the classifier
    bots_data, webclients_data = parse_training_data(
        constants.PATH_TO_BOTS_TCPDUMP, constants.PATH_TO_WEBCLIENTS_TCPDUMP)

    combined_df = convert_to_dataframe(bots_data, webclients_data)

    combined_df = encoding_features(combined_df)

    clf, X_test, y_test = train_decision_tree(combined_df)

    # Using another dataset to test the classifier
    X_test, y_test = testing_eval(
        constants.PATH_TO_EVAL_TCPDUMP1, constants.PATH_TO_EVAL_TCPDUMP2, clf)

    # Test the classifier's accuracy on the test set
    accuracy = clf.score(X_test, y_test)
    print("Accuracy of the model : ", accuracy)

    # Predict the labels of new and unseen data from X_test and y_test
    y_pred = clf.predict(X_test)
    # print("Prediction :", y_pred.tolist())
    # print("Prediction :", y_test.tolist())

    # # Count the number of 'human' and the number of 'bot' predictions
    # print("Number of 'human' predictions :", y_test.tolist().count('human'))
    # print("Number of 'bot' predictions :", y_test.tolist().count('bot'))


if __name__ == "__main__":
    main_decision_tree()
