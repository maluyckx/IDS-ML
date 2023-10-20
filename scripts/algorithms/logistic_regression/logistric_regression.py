"""
Goal of the script : Using logistic regression to detect bots in a network traffic trace 

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

# ML dependencies
from sklearn.linear_model import LogisticRegression
import pickle

# Personal dependencies
import sys
sys.path.append("../../")
import constants
import parsing_dns_trace as parser
import features

def train_logistic_regression(bots_data, webclients_data):
    pass


def eval_logistic_regression(path_to_eval_tcpdump1, path_to_eval_tcpdump2):
    pass

def load_saved_logistic_regression():
    with open(f"../../../trained_models/logistic_regression/{constants.NAME_TRAINED_MODEL_logistic_regression}", "wb") as logistic_regression_saved_model:
        loaded_clf = pickle.load(logistic_regression_saved_model)
    return loaded_clf

def save_logistic_regression(clf):
    with open(f"../../../trained_models/logistic_regression/{constants.NAME_TRAINED_MODEL_logistic_regression}", "wb") as logistic_regression_saved_model:
        pickle.dump(clf, logistic_regression_saved_model)

def diagram_logistic_regression(clf):
    # find a way to make a diagram of the decision tree
    pass


def main_logistic_regression():
    # Use a first dataset to train the classifier
    bots_data, webclients_data = parser.parse_training_data(constants.PATH_TO_BOTS_TCPDUMP, constants.PATH_TO_WEBCLIENTS_TCPDUMP)

    # Training the classifier
    clf = train_logistic_regression(bots_data, webclients_data)

    # Use a second dataset to test the classifier
    X_test, y_test = eval_logistic_regression(
        constants.PATH_TO_EVAL_TCPDUMP1, constants.PATH_TO_EVAL_TCPDUMP2)

    # Test the classifier's accuracy on the test set
    accuracy = clf.score(X_test, y_test)
    print("Accuracy of the model : ", accuracy)

    diagram_logistic_regression(clf)
    save_logistic_regression(clf)
    
if __name__ == "__main__":
    main_logistic_regression()
