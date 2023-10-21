"""
Goal of the script : Using a decision tree classifier to detect bots in a network traffic trace 

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

# ML dependencies
from sklearn.tree import DecisionTreeClassifier
import pickle

# Graphics dependencies
from sklearn.tree import export_graphviz
import graphviz

# Personal dependencies
import sys
sys.path.append("../../")
import constants
import parsing_dns_trace as parser
import features

def train_decision_tree(bots_data, webclients_data):
    print("####\nTraining the decision tree classifier...")

    combined_df = features.convert_to_dataframe(bots_data, webclients_data)

    combined_df = features.encoding_features(combined_df)

    X_train = combined_df[constants.LIST_OF_FEATURES]
    y_train = combined_df['label']

    # Train the decision tree classifier
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    
    print("Decision tree classifier trained successfully!\n####\n")
    return clf


def eval_decision_tree(path_to_eval_tcpdump1, path_to_eval_tcpdump2):
    print("####\nTesting the decision tree classifier...")
    eval_data1, eval_data2 = parser.parse_training_data(
        path_to_eval_tcpdump1, path_to_eval_tcpdump2)

    combined_df = features.convert_to_dataframe(eval_data1, eval_data2)

    combined_df = features.encoding_features(combined_df)

    X_test = combined_df[constants.LIST_OF_FEATURES]
    y_test = combined_df['label']

    print("Decision tree classifier tested successfully!\n####\n")
    return X_test, y_test

def load_saved_decision_tree():
    with open(f"../../../trained_models/decision_tree/{constants.NAME_TRAINED_MODEL_DECISION_TREE}", 'rb') as decision_tree_saved_model:
        loaded_clf = pickle.load(decision_tree_saved_model)
    return loaded_clf

def save_decision_tree(clf):
    with open(f"../../../trained_models/decision_tree/{constants.NAME_TRAINED_MODEL_DECISION_TREE}", "wb") as decision_tree_saved_model:
        pickle.dump(clf, decision_tree_saved_model)

def diagram_decision_tree(clf):
    
    ## COULD NOT BE TESTED YET
   """dot_data = export_graphviz(clf, out_file=None,
                            feature_names=constants.LIST_OF_FEATURES,
                            class_names=['bot', 'webclient'],
                            filled=True, rounded=True, special_characters=True)

    graph = graphviz.Source(dot_data)
    graph.render("decision_tree")"""



def main_decision_tree():
    # Use a first dataset to train the classifier
    bots_data, webclients_data = parser.parse_training_data(constants.PATH_TO_BOTS_TCPDUMP, constants.PATH_TO_WEBCLIENTS_TCPDUMP)

    # Training the classifier
    clf = train_decision_tree(bots_data, webclients_data)

    # Use a second dataset to test the classifier
    X_test, y_test = eval_decision_tree(
        constants.PATH_TO_EVAL_TCPDUMP1, constants.PATH_TO_EVAL_TCPDUMP2)

    # Test the classifier's accuracy on the test set
    accuracy = clf.score(X_test, y_test)
    print("Accuracy of the model : ", accuracy)

    diagram_decision_tree(clf)
    save_decision_tree(clf)
    
if __name__ == "__main__":
    main_decision_tree()
