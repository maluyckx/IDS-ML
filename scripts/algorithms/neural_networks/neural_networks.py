"""
Goal of the script : Using a neural network to detect bots in a network traffic trace 

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

# ML dependencies
from sklearn.neural_network import MLPClassifier
import pickle

# Personal dependencies
import sys
sys.path.append("../../")
import constants
import parsing_dns_trace as parser
import features

def train_neural_networks(bots_data, webclients_data):
    pass


def eval_neural_networks(path_to_eval_tcpdump1, path_to_eval_tcpdump2):
    pass

def load_saved_neural_networks():
    with open(f"../../../trained_models/neural_networks/{constants.NAME_TRAINED_MODEL_neural_networks}", "wb") as neural_networks_saved_model:
        loaded_clf = pickle.load(neural_networks_saved_model)
    return loaded_clf

def save_neural_networks(clf):
    with open(f"../../../trained_models/neural_networks/{constants.NAME_TRAINED_MODEL_neural_networks}", "wb") as neural_networks_saved_model:
        pickle.dump(clf, neural_networks_saved_model)

def diagram_neural_networks(clf):
    # find a way to make a diagram of the decision tree
    pass


def main_neural_networks():
    # Use a first dataset to train the classifier
    bots_data, webclients_data = parser.parse_training_data(constants.PATH_TO_BOTS_TCPDUMP, constants.PATH_TO_WEBCLIENTS_TCPDUMP)

    # Training the classifier
    clf = train_neural_networks(bots_data, webclients_data)

    # Use a second dataset to test the classifier
    X_test, y_test = eval_neural_networks(
        constants.PATH_TO_EVAL_TCPDUMP1, constants.PATH_TO_EVAL_TCPDUMP2)

    # Test the classifier's accuracy on the test set
    accuracy = clf.score(X_test, y_test)
    print("Accuracy of the model : ", accuracy)

    diagram_neural_networks(clf)
    save_neural_networks(clf)
    
if __name__ == "__main__":
    main_neural_networks()