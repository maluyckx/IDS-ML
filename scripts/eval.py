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

    X_test = combined_df[constants.LIST_OF_FEATURES_COMBI4]
    y_test = combined_df['label']
    hosts_lists = combined_df['host']

    return X_test, y_test, hosts_lists


def false_alarm_rate(y_pred, y_test, hosts_lists): # TODO : relire cette fonction après avoir lu les articles 
    """
    This function is extremely important for the CORRECT evaluation of the model. We cannot base our evaluation on the accuracy of the model. We need to take into account the false alarm rate and the detection rate.
    
    Detection rate = TP / (TP + FN)
    False alarm rate = FP / (FP + TN)
    False negative rate = FN / (TP + FN)
    True negative rate = TN / (FP + TN)
    """   

    hosts = {"true positive": [], "false positive": [], "false negative": [], "true negative": []}
    
    suspicious_hosts = []
    for i in range(len(y_test)):
        if y_pred[i] == y_test[i] and y_pred[i] == "bot": # Detection rate
            hosts["true positive"].append(hosts_lists[i])
            suspicious_hosts.append(hosts_lists[i])
            print(colors.Colors.LIGHTCYAN + hosts_lists[i] + " : true positive" + colors.Colors.RESET)
            
        elif y_pred[i] != y_test[i] and y_pred[i] == "bot": # False alarm rate
            hosts["false positive"].append(hosts_lists[i])
            suspicious_hosts.append(hosts_lists[i])
            print(colors.Colors.LIGHTRED + hosts_lists[i] + " : false positive" + colors.Colors.RESET)
            
        elif y_pred[i] == y_test[i] and y_pred[i] == "human":
            hosts["true negative"].append(hosts_lists[i])
            print(colors.Colors.LIGHTYELLOW + hosts_lists[i] + " : true negative" + colors.Colors.RESET)
            
        elif y_pred[i] != y_test[i] and y_pred[i] == "human": 
            hosts["false negative"].append(hosts_lists[i])
            print(colors.Colors.LIGHTPURPLE + hosts_lists[i] + " : false negative" + colors.Colors.RESET)
                

    print(colors.Colors.RED + f"####\nFalse alarm rate and detection rate..." + colors.Colors.RESET) 
    print(colors.Colors.RED + f"Detection rate : {len(hosts['true positive']) / (len(hosts['true positive']) + len(hosts['false negative'])) * 100} %" + colors.Colors.RESET)
    print(colors.Colors.RED + f"False alarm rate : {len(hosts['false positive']) / (len(hosts['false positive']) + len(hosts['true negative'])) * 100} %" + colors.Colors.RESET)
    print(colors.Colors.RED + f"False negative rate : {len(hosts['false negative']) / (len(hosts['true positive']) + len(hosts['false negative'])) * 100} %" + colors.Colors.RESET)
    print(colors.Colors.RED + f"True negative rate : {len(hosts['true negative']) / (len(hosts['false positive']) + len(hosts['true negative'])) * 100} %" + colors.Colors.RESET)

    print(colors.Colors.RED + f"Accuracy : {(len(hosts['true positive']) + len(hosts['true negative'])) / (len(hosts['true positive']) + len(hosts['false positive']) + len(hosts['true negative']) + len(hosts['false negative'])) * 100} %" + colors.Colors.RESET)
    print(colors.Colors.RED + f"####\n" + colors.Colors.RESET)
    
    print("true positive : ", len(hosts["true positive"]))
    print("false positive : ", len(hosts["false positive"]))
    print("false negative : ", len(hosts["false negative"]))
    print("true negative : ", len(hosts["true negative"]))

    return suspicious_hosts


def determine_threshold(y_pred_proba):
    """
    This function is used to separate the bots from the 'bots+humans' class.
    
    We need to pick an arbitrary threshold to separate the 2 classes but we need to be careful not to pick a threshold that is too low or too high.
    
    """
    # determine the threshold to separate the bots from the humans
    threshold = 0.2
    for i in range(len(y_pred_proba)):
        if abs(y_pred_proba[i][0] - y_pred_proba[i][1]) < threshold:
            print("human+bot : ", y_pred_proba[i])

def eval_model(clf, eval_dataset, algorithm, output_path_to_suspicious_hosts):
    
    X_test, y_test, hosts_lists = preprocessing(eval_dataset, algorithm)
    # Test the classifier's accuracy on the test set
    y_pred_proba = clf.predict_proba(X_test)
    print(y_pred_proba)
    y_pred = clf.predict(X_test)

    print(colors.Colors.RED + f"{constants.ALGORITHMS_NAMES[algorithm]} classifier tested successfully!\n####\n" + colors.Colors.RESET)
    
    determine_threshold(y_pred_proba)

    suspicious_hosts = false_alarm_rate(y_pred, y_test, hosts_lists)
    result_suspicious_hosts(suspicious_hosts, output_path_to_suspicious_hosts)

    # Classification report contains the precision, recall, f1-score and support that will be used for the diagrams
    classification = classification_report(y_true=y_test, y_pred=y_pred, target_names=['bot', 'human'], output_dict=True) 
    print(colors.Colors.PURPLE + "Classification report : \n", classification, colors.Colors.RESET)

    precision = classification['weighted avg']['precision']
    recall = classification['weighted avg']['recall']
    f1_score = classification['weighted avg']['f1-score']
    support = classification['weighted avg']['support']

    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1-Score: {f1_score}")
    print(f"Support: {support}")

    

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
