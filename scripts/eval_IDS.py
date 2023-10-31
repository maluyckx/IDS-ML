"""
Goal of the script : Evaluating the model

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

#### Common dependencies
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
import utils.diagrams as diagrams


#######################################

def result_suspicious_hosts(suspicious_hosts, output_path_to_suspicious_hosts):
    """
    Write the result of the evaluation into a file
    """
    with open(output_path_to_suspicious_hosts, "w") as f:
        for host in suspicious_hosts:
            f.write(host + "\n")


def preprocessing(path_to_eval_dataset, algorithm):
    eval_data = parser.parse_eval_data(path_to_eval_dataset)     
    print(colors.Colors.RED + f"####\nTesting the {constants.ALGORITHMS_NAMES[algorithm]} classifier..." + colors.Colors.RESET)
    
    combined_df = features.convert_to_dataframe_testing(eval_data, path_to_eval_dataset) 

    combined_df = features.encoding_features(combined_df)

    X_test = combined_df[constants.LIST_OF_FEATURES]
    y_test = combined_df['label']
    hosts_lists = combined_df['host']

    return X_test, y_test, hosts_lists

def eval_model(clf, eval_dataset, algorithm, output_path_to_suspicious_hosts):
    
    X_test, y_test, hosts_lists = preprocessing(eval_dataset, algorithm)

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
    result_suspicious_hosts(suspicious_hosts, output_path_to_suspicious_hosts)

    print(colors.Colors.RED + f"{constants.ALGORITHMS_NAMES[algorithm]} classifier tested successfully!\n####\n" + colors.Colors.RESET)



    # check the accuracy
    accuracy = np.mean(y_pred == y_test)
    print(colors.Colors.PURPLE + f"Accuracy of the model : {accuracy}" + colors.Colors.RESET)
    classification = classification_report(y_true=y_test, y_pred=y_pred, target_names=['human', 'bot'])
    print(colors.Colors.PURPLE + "Classification report : \n", classification + colors.Colors.RESET)

    

def main_eval(trained_model, eval_dataset, output_path_to_suspicious_hosts):
    ## Load the model
    loaded_clf = saving_model.load_saved_model(trained_model)

    # extract algorithm name from the path
    algorithm = str(trained_model).split("/")[2]

    ## evaluate the model
    eval_model(loaded_clf, eval_dataset, algorithm, output_path_to_suspicious_hosts)
    
    ## Diagrams
    # diagrams.main_diagrams(algorithm)


def getting_args():
    parser = argparse.ArgumentParser(description="Dataset evaluation")
    parser.add_argument("--trained_model", type=pathlib.Path)
    parser.add_argument("--dataset", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args()
    
    trained_model = args.trained_model
    eval_dataset = args.dataset
    output_path_to_suspicious_hosts = args.output
    
    return trained_model, eval_dataset, output_path_to_suspicious_hosts

if __name__ == "__main__":
    trained_model, eval_dataset, output_path_to_suspicious_hosts = getting_args()
    main_eval(trained_model, eval_dataset, output_path_to_suspicious_hosts)
