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



def parse_dns_trace(line):
    """Parse a single line from the DNS trace dataset with additional features."""
    # Extract timestamp
    timestamp_match = re.search(r"(\d{2}:\d{2}:\d{2}\.\d{6})", line)
    timestamp = timestamp_match.group(1) if timestamp_match else None

    # Extract host name
    host_match = re.search(r"IP (\w+)", line)
    host = host_match.group(1) if host_match else None

    # Extract DNS query type (e.g., A, AAAA)
    # Adjusted to also capture the query type in the new format
    query_type_match = re.search(r"\s(A|AAAA)(?=[\s\?])", line)
    query_type = query_type_match.group(1) if query_type_match else None

    # Extract domain being queried
    domain_match = re.search(r"\? ([\w\.-]+)\.", line)
    domain = domain_match.group(1) if domain_match else None

    # Extract length
    length_match = re.search(r"\((\d+)\)$", line)
    length = int(length_match.group(1)) if length_match else None

    # Extract DNS responses
    # Assuming the response format is "A IP_address"
    responses = re.findall(r"(A|AAAA) (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)

    return {
        "timestamp": timestamp,
        "host": host,
        "query_type": query_type,
        "domain": domain,
        "length": length,
        "responses": responses
    }


def parse_training_data(path_to_bots_tcpdump, path_to_webclients_tcpdump):

    # Parse both datasets
    bots_data = []
    with open(path_to_bots_tcpdump, 'r') as file:
        for line in file:
            parsed_data = parse_dns_trace(line)
            if parsed_data["domain"]:  # Only consider lines with domain information
                bots_data.append(parsed_data)

    print(parsed_data)
    
    webclients_data = []
    with open(path_to_webclients_tcpdump, 'r') as file:
        for line in file:
            parsed_data = parse_dns_trace(line)
            if parsed_data["domain"]:  # Only consider lines with domain information
                webclients_data.append(parsed_data)

    return bots_data, webclients_data


def convert_to_dataframe(bots_data, webclients_data):
    # Convert to DataFrame
    bots_df = pd.DataFrame(bots_data)
    bots_df['label'] = 'bot'

    webclients_df = pd.DataFrame(webclients_data)
    webclients_df['label'] = 'human'

    # Combine the two datasets
    combined_df = pd.concat([bots_df, webclients_df], ignore_index=True)

    # Convert categorical features to numerical
    combined_df['query_type'] = combined_df['query_type'].astype('category')
    combined_df['domain'] = combined_df['domain'].astype('category')
    combined_df['host'] = combined_df['host'].astype('category')
    combined_df['timestamp'] = combined_df['timestamp'].astype('category')
    combined_df['length'] = combined_df['length'].astype('int64')
    
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

    label_encoder_length = LabelEncoder()
    combined_df['length_encoded'] = label_encoder_length.fit_transform(
        combined_df['length'])

    return combined_df


def train_decision_tree(combined_df):

    # Split the data into training and testing sets
    list_of_features = ['query_type_encoded',
                        'domain_encoded', 'host_encoded', 'timestamp_encoded', 'length_encoded']
    
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
                        'domain_encoded', 'host_encoded', 'timestamp_encoded', 'length_encoded']

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
