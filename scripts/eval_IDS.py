"""
Goal of the script : Evaluating the model

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

import argparse
import pathlib
import numpy as np

#### ML dependencies
from sklearn.metrics import classification_report

#### Importing the utils
import utils.parsing_dns_trace as parser
import utils.constants as constants
import utils.features as features
import utils.colors as colors

import utils.saving_model as saving_model
#######################################

def get_botlists():
    botlist1 = []
    with open(f"{constants.PATH_TO_BOTLISTS}eval1_botlist.txt", "r") as f:
        for line in f:
            botlist1.append(line.strip())
    
    botlist2 = []
    with open(f"{constants.PATH_TO_BOTLISTS}eval2_botlist.txt", "r") as f:
        for line in f:
            botlist2.append(line.strip())
            
    return botlist1, botlist2


def get_botlist():
    """
    Read the botlist file and return a list of bots
    """
    bots = []
    with open("../../evaluation_datasets/botlists/eval1_botlist.txt", "r") as botlist:
        for line in botlist:
            bots.append(line.strip())
    return bots

def result_suspicious_hosts(suspicious_hosts):
    """
    Write the result of the evaluation into a file
    """
    with open(f"{constants.PATH_TO_SUSPICIOUS_HOSTS_EVAL1}", "w") as f:
        for host in suspicious_hosts:
            f.write(host + "\n")


def preprocessing(path_to_eval_tcpdump1, algorithm):
    eval1_data = parser.parse_eval_data(path_to_eval_tcpdump1)
    #eval2_data = parser.parse_eval_data(path_to_eval_tcpdump2)
    
    print(colors.Colors.RED + f"####\nTesting the {constants.ALGORITHMS_NAMES[algorithm]} classifier..." + colors.Colors.RESET)
    
    combined_df = features.convert_to_dataframe_testing(eval1_data) #, eval_data2)

    combined_df = features.encoding_features(combined_df)

    X_test = combined_df[constants.LIST_OF_FEATURES]
    y_test = combined_df['label']
    hosts_lists = combined_df['host']

    return X_test, y_test, hosts_lists

def eval_model(clf, path_to_eval_tcpdump1, algorithm): # path_to_eval_tcpdump2,
    
    X_test, y_test, hosts_lists = preprocessing(path_to_eval_tcpdump1, algorithm)

    # Test the classifier's accuracy on the test set
    y_pred = clf.predict(X_test)

    suspicious_hosts = []

    # check all the hosts that were classified as bots
    for i in range(len(y_test)):
        if y_pred[i] in y_test[i] and y_pred[i] == "bot":
            print(hosts_lists[i] + " : true positive")
            suspicious_hosts.append(hosts_lists[i])
        elif y_pred[i] not in y_test[i] and y_pred[i] == "bot":
            print(hosts_lists[i] + " : false positive")
            suspicious_hosts.append(hosts_lists[i])
    
    # write the result into a file in suspicious_hosts.txt
    result_suspicious_hosts(suspicious_hosts)


    # check the accuracy
    accuracy = np.mean(y_pred == y_test)
    print("Accuracy of the model : ", accuracy)

    classification = classification_report(
        y_true=y_test, y_pred=y_pred, target_names=['human', 'bot'])
    print(colors.Colors.YELLOW + "Classification report : \n",
          classification + colors.Colors.RESET)

   # diagrams.diagram_logistic_regression(clf, X_test, y_test)
    
    print(colors.Colors.RED +
          f"{constants.ALGORITHMS_NAMES[algorithm]} classifier tested successfully!\n####\n" + colors.Colors.RESET)




def main_eval(trained_model, dataset, output):
    ## Load the model
    loaded_clf = saving_model.load_saved_model(trained_model)

    # extract algorithm name from the path
    # ../trained_models/logistic_regression/trained_model_logistic_regression.pkl
    algorithm = str(trained_model).split("/")[2]

    ## evaluate the model
    eval_model(loaded_clf, constants.PATH_TO_EVAL_TCPDUMP1, algorithm)
    


def getting_args():
    parser = argparse.ArgumentParser(description="Dataset evaluation")
    parser.add_argument("--trained_model", type=pathlib.Path)
    parser.add_argument("--dataset", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args()
    
    trained_model = str(args.trained_model) # TODO: need to be checked (dunno if we will leave this to str())
    dataset = args.dataset
    output = args.output
    
    return trained_model, dataset, output

if __name__ == "__main__":
    trained_model, dataset, output = getting_args()
    main_eval(trained_model, dataset, output)
