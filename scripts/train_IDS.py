"""
Goal of the script : Training the model

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


import argparse
import pathlib
import sys 


#### Importing the utils
import utils.parsing_dns_trace as parser
import utils.constants as constants
import utils.features as features

#### Importing the algorithms
sys.path.append("algorithms/decision_tree/")
# sys.path.append("algorithms/random_forest/")
# sys.path.append("algorithms/logistic_regression/")
# sys.path.append("algorithms/neural_network/")

# import decision_tree
# import random_forest
# import logistic_regression
# import neural_network

#######################################

def train_decision_tree(webclients, bots, output):
    # decision_tree.test_print()
    pass



def train_random_forest(webclients, bots, output):
    pass



def train_logistic_regression(webclients, bots, output):
    pass



def train_neural_network(webclients, bots, output):
    pass






def preprocessing(bots, webclients):
    ### Parsing the datasets
    bots_data, webclients_data = parser.parse_training_data(bots, webclients)
    
    combined_df = features.convert_to_dataframe(bots_data, webclients_data)

    combined_df = features.encoding_features(combined_df)

    X_train = combined_df[constants.LIST_OF_FEATURES]
    y_train = combined_df['label']

def main_train(webclients, bots, output):
    ## Preprocessing before training : parsing and encoding the features
    preprocessing(bots, webclients)
    
    
    ### Decision Tree
    train_decision_tree(webclients, bots, output)
    
    ### Random Forest
    # train_random_forest(webclients, bots, output)
    
    ### Logistic Regression
    # train_logistic_regression(webclients, bots, output)
    
    ### Neural Network
    # train_neural_network(webclients, bots, output)
    
    

def getting_args():
    parser = argparse.ArgumentParser(description="Optional classifier training")
    parser.add_argument("--webclients", required=True, type=pathlib.Path)
    parser.add_argument("--bots", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args()
    webclients = args.webclients
    bots = args.bots
    output = args.output

    return webclients, bots, output

if __name__ == "__main__":
    webclients, bots, output = getting_args()
    main_train(webclients, bots, output)

