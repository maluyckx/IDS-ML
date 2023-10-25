"""
All the constants used in the project

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

## List of algorithms
ALGORITHMS_NAMES = {
                    "decision_tree" : "Decision tree", 
                    "logistic_regression" : "Logistic regression", 
                    "random_forest" : "Random forest", 
                    "neural_networks":"Neural networks",
                    "knn" : "KNN",
                    }


## Path to training datasets for algos
PATH_TO_BOTS_TCPDUMP = "../../training_datasets/tcpdumps/bots_tcpdump.txt"
PATH_TO_WEBCLIENTS_TCPDUMP = "../../training_datasets/tcpdumps/webclients_tcpdump.txt"

## Path to evaluation datasets for algos
PATH_TO_EVAL_TCPDUMP1 = "../../evaluation_datasets/tcpdumps/eval1_tcpdump.txt"
PATH_TO_EVAL_TCPDUMP2 = "../../evaluation_datasets/tcpdumps/eval2_tcpdump.txt"

## List of features
LIST_OF_FEATURES = [
                    # 'timestamp_encoded',
                    # 'host_encoded',
                    'query_type_encoded', 
                    'domain_encoded', 
                    'length_request_encoded', 
                    'length_response_encoded', 
                    'responses_encoded', 
                    'counts_encoded'
                    ]





## Name for the trained models
NAME_TRAINED_MODEL_DECISION_TREE = "trained_model_decision_tree.pkl"
NAME_TRAINED_MODEL_RANDOM_FOREST = "trained_model_random_forest.pkl"
NAME_TRAINED_MODEL_LOGISTIC_REGRESSION = "trained_model_logistic_regression.pkl"
NAME_TRAINED_MODEL_NEURAL_NETWORK = "trained_model_neural_network.pkl"

## Dictionary to math the name of the trained model with the name of the algorithm
NAME_TRAINED_MODEL = {
    "decision_tree" : NAME_TRAINED_MODEL_DECISION_TREE,
    "random_forest" : NAME_TRAINED_MODEL_RANDOM_FOREST,
    "logistic_regression" : NAME_TRAINED_MODEL_LOGISTIC_REGRESSION,
    "neural_networks" : NAME_TRAINED_MODEL_NEURAL_NETWORK
}


## Path to botlists
PATH_TO_BOTLISTS = "../evaluation_datasets/botlists/"

## Path to suspicious hosts file
PATH_TO_SUSPICIOUS_HOSTS = "../suspicious_hosts/suspicious_hosts.txt"
