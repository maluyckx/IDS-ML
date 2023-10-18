"""
Goal of the script : Using a decision tree classifier to detect bots in a network traffic trace 

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

import pandas as pd
import re

import sys
sys.path.append("../../")
import constants
import parsing_dns_trace as parser
import features

import pickle

def train_decision_tree(combined_df):
    print("####\nTraining the decision tree classifier...")
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
    print("Decision tree classifier trained successfully!\n####\n")
    return clf, X_test, y_test


def testing_eval(path_to_eval_tcpdump1, path_to_eval_tcpdump2):
    print("####\nTesting the decision tree classifier...")
    eval_data1, eval_data2 = parser.parse_training_data(
        path_to_eval_tcpdump1, path_to_eval_tcpdump2)

    combined_df = features.convert_to_dataframe(eval_data1, eval_data2)

    combined_df = features.encoding_features(combined_df)

    list_of_features = ['query_type_encoded',
                        'domain_encoded', 'host_encoded', 'timestamp_encoded', 'length_encoded']

    X_test = combined_df[list_of_features]
    y_test = combined_df['label']

    print("Decision tree classifier tested successfully!\n####\n")
    return X_test, y_test

def load_saved_decision_tree():
    with open('trained_model.pkl', 'rb') as file:
        loaded_clf = pickle.load(file)
    return loaded_clf

def save_decision_tree(clf):
    with open(f"../../../trained_models/decision_tree/{constants.NAME_TRAINED_MODEL_DECISION_TREE}", "wb") as file:
        pickle.dump(clf, file)

def diagram_decision_tree(clf):
    # find a way to make a diagram of the decision tree
    pass


def main_decision_tree():
    # Use a first dataset to train the classifier
    bots_data, webclients_data = parser.parse_training_data(
        constants.PATH_TO_BOTS_TCPDUMP, constants.PATH_TO_WEBCLIENTS_TCPDUMP)

    combined_df = features.convert_to_dataframe(bots_data, webclients_data)

    combined_df = features.encoding_features(combined_df)

    clf, X_test, y_test = train_decision_tree(combined_df)

    # Using another dataset to test the classifier
    X_test, y_test = testing_eval(
        constants.PATH_TO_EVAL_TCPDUMP1, constants.PATH_TO_EVAL_TCPDUMP2)

    save_decision_tree(clf)
    diagram_decision_tree(clf)
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
