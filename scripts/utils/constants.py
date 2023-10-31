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
PATH_TO_BOTS_TCPDUMP = "../training_datasets/tcpdumps/bots_tcpdump.txt"
PATH_TO_WEBCLIENTS_TCPDUMP = "../training_datasets/tcpdumps/webclients_tcpdump.txt"

## Path to evaluation datasets for algos
PATH_TO_EVAL_TCPDUMP1 = "../evaluation_datasets/tcpdumps/eval1_tcpdump.txt"
PATH_TO_EVAL_TCPDUMP2 = "../evaluation_datasets/tcpdumps/eval2_tcpdump.txt"

## List of features
# LIST_OF_FEATURES = [
#                     # 'timestamp_encoded',
#                     # 'host_encoded',
#                     'query_type_encoded', 
#                     'domain_encoded', 
#                     'length_request_encoded', 
#                     'length_response_encoded', 
#                     'responses_encoded', 
#                     'counts_encoded'
#                     ]

LIST_OF_FEATURES = [
   
                    ## Features MISC
                    # "average_of_request_length",
                    # "average_of_response_length",
                    # # "type_of_requests_queried_by_hosts",
                    # # "type_of_responses_received_by_hosts",
                    
                    ## Features TIME 
                    # "average_time_for_a_session",
                    # "average_time_between_requests",
                    # "frequency_of_repeated_requests_in_a_short_time_frame",
                    
                    ## Features NUMBERS
                    # "average_number_of_dots_in_a_domain",
                    "number_of_requests_in_a_session",
                    # "number_of_unique_domains",
                    # "average_counts",
                    ]

NOT_A_RESSOURCE_RECORD = "not_a_ressource_record_constant"
AUTHORITATIVE_SERVER_RESPONSE = "authoritative_server_response_constant"
NON_EXISTENT_DOMAIN_ERROR = "non_existent_domain_error_constant"
SERVFAIL_ERROR = "servfail_error_constant"



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
PATH_TO_SUSPICIOUS_HOSTS_EVAL1 = "../suspicious_hosts/eval1_tcpdump/suspicious_hosts.txt"
PATH_TO_SUSPICIOUS_HOSTS_EVAL2 = "../suspicious_hosts/eval2_tcpdump/suspicious_hosts.txt"

