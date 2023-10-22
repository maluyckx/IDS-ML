"""
Goal of the script : Using a random forest to detect bots in a network traffic trace 

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

# ML dependencies
from sklearn.ensemble import RandomForestClassifier
import pickle

# Personal dependencies
import sys
sys.path.append("../../")
import scripts.utils.constants as constants
import parsing_dns_trace as parser
import scripts.utils.features as features

def train_random_forest(bots_data, webclients_data):
    pass


def eval_random_forest(path_to_eval_tcpdump1, path_to_eval_tcpdump2):
    pass

def load_saved_random_forest():
    with open(f"../../../trained_models/random_forest/{constants.NAME_TRAINED_MODEL_random_forest}", "wb") as random_forest_saved_model:
        loaded_clf = pickle.load(random_forest_saved_model)
    return loaded_clf

def save_random_forest(clf):
    with open(f"../../../trained_models/random_forest/{constants.NAME_TRAINED_MODEL_random_forest}", "wb") as random_forest_saved_model:
        pickle.dump(clf, random_forest_saved_model)

def diagram_random_forest(clf):
    # find a way to make a diagram of the decision tree
    pass


def main_random_forest():
    # Use a first dataset to train the classifier
    bots_data, webclients_data = parser.parse_training_data(constants.PATH_TO_BOTS_TCPDUMP, constants.PATH_TO_WEBCLIENTS_TCPDUMP)

    # Training the classifier
    clf = train_random_forest(bots_data, webclients_data)

    # Use a second dataset to test the classifier
    X_test, y_test = eval_random_forest(
        constants.PATH_TO_EVAL_TCPDUMP1, constants.PATH_TO_EVAL_TCPDUMP2)

    # Test the classifier's accuracy on the test set
    accuracy = clf.score(X_test, y_test)
    print("Accuracy of the model : ", accuracy)

    diagram_random_forest(clf)
    save_random_forest(clf)
    
if __name__ == "__main__":
    main_random_forest()