"""
Goal of the script : Evaluating the model

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

#### Common dependencies
import argparse
import pathlib

#### ML dependencies
from sklearn.metrics import classification_report

#### Importing the utils
import utils.parsing_dns_trace as parser
import utils.constants as constants
import utils.features as features
import utils.colors as colors
import scripts.utils.saving_and_loading as saving_and_loading
import scripts.utils.diagrams.diagrams_algo as diagrams_algo
import scripts.utils.diagrams.diagrams_metrics as diagrams_metrics


#######################################

def result_suspicious_hosts(suspicious_hosts, output_path_to_suspicious_hosts):
    """
    Write the result of the evaluation into a file
    
    Args:
    - suspicious_hosts: a list of suspicious hosts
    - output_path_to_suspicious_hosts: a string representing the path to the output file for suspicious hosts   
    """
    with open(output_path_to_suspicious_hosts, "w") as f:
        for host in suspicious_hosts:
            f.write(host + "\n")


def preprocessing(path_to_eval_dataset, algorithm):
    """
    Preprocesses the evaluation dataset by parsing the data, converting it to a dataframe, encoding the features 
    and returning the preprocessed data.
    
    Args:
    - path_to_eval_dataset: the path to the evaluation dataset.
    - algorithm: the algorithm to be used for classification.
    
    Returns:
    - X_test: the preprocessed feature data for evaluation.
    - y_test: the preprocessed label data for evaluation.
    - hosts_lists: the preprocessed host data for evaluation.
    """
    eval_data = parser.parse_eval_data(path_to_eval_dataset)     
    print(colors.Colors.RED + f"####\nTesting the {constants.ALGORITHMS_NAMES[algorithm]} classifier..." + colors.Colors.RESET)
    
    combined_df = features.convert_to_dataframe_testing(eval_data, path_to_eval_dataset) 

    combined_df = features.encoding_features(combined_df)

    X_test = combined_df[constants.LIST_OF_FEATURES_COMBI4]
    y_test = combined_df['label']
    hosts_lists = combined_df['host']

    return X_test, y_test, hosts_lists


def false_alarm_rate(y_pred, y_test, hosts_lists):
    """
    This function is extremely important for the CORRECT evaluation of the model. We cannot base our evaluation on the accuracy of the model. We need to take into account the false alarm rate and the detection rate.
    
    Detection rate = TP / (TP + FN)
    False alarm rate = FP / (FP + TN)
    False negative rate = FN / (TP + FN)
    True negative rate = TN / (FP + TN)
    
    Args:
    - y_pred: a list of predicted labels
    - y_test: a list of true labels
    - hosts_lists: a list of hosts

    Returns:
    - suspicious_hosts: a list of suspicious hosts
    - hosts: a dictionary containing the true positive, false positive, false negative and true negative hosts
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
    
    print(colors.Colors.RED + f"####\nTotal host : ", len(hosts_lists), colors.Colors.RESET)
    print(colors.Colors.RED + "Number of true positive : ", len(hosts["true positive"]), colors.Colors.RESET)
    print(colors.Colors.RED + "Number of false positive : ", len(hosts["false positive"]), colors.Colors.RESET)
    print(colors.Colors.RED + "Number of false negative : ", len(hosts["false negative"]), colors.Colors.RESET)
    print(colors.Colors.RED + "Number of true negative : ", len(hosts["true negative"]) , colors.Colors.RESET)
    print(colors.Colors.RED + f"####\n" + colors.Colors.RESET)

    return suspicious_hosts, hosts


def determine_threshold(y_pred_proba): # TODO revoir ce commentaire
    """
    This function is used to separate the bots from the 'bots+humans' class by using a threshold.
    We need to pick an 'arbitrary' threshold to separate the 2 classes but we need to be careful not to pick a threshold that is too low or too high.
    
    Args:
    - y_pred_proba: a list of predicted probabilities for each class.

    Returns:
    - human_bot: a list of indices corresponding to the 'bots+humans' class.
    """
    # determine the threshold to separate the bots from the humans
    human_bot = []
    threshold = 0.5
    for i in range(len(y_pred_proba)):
        if abs(y_pred_proba[i][0] - y_pred_proba[i][1]) < threshold:
            print("human+bot : ", y_pred_proba[i])
            human_bot.append(i)

    return human_bot


def print_classification_report(y_pred, y_test):
    """
    Prints the classification report for the given predicted and true labels.
    
    Args:
    - y_pred: predicted labels
    - y_test: true labels
    """
    classification = classification_report(y_true=y_test, y_pred=y_pred, target_names=['bot', 'human'], output_dict=True)    
    
    print(colors.Colors.PURPLE + f"#### Classification report : \n" + colors.Colors.RESET) 

    print(colors.Colors.PURPLE + "## Bot : \n")
    print(f"Precision: {classification['bot']['precision']}")
    print(f"Recall: {classification['bot']['recall']}")
    print(f"F1-Score: {classification['bot']['f1-score']}")
    print(f"Support: {classification['bot']['support']} \n", colors.Colors.RESET)
    
    print(colors.Colors.PURPLE + "## Human : \n" )
    print(f"Precision: {classification['human']['precision']}")
    print(f"Recall: {classification['human']['recall']}")
    print(f"F1-Score: {classification['human']['f1-score']}")
    print(f"Support: {classification['human']['support']} \n", colors.Colors.RESET)
    
    # print(colors.Colors.PURPLE + "## Human + Bot : \n" )
    # print(f"Precision: {classification['human_bot']['precision']}")
    # print(f"Recall: {classification['human_bot']['recall']}")
    # print(f"F1-Score: {classification['human_bot']['f1-score']}")
    # print(f"Support: {classification['human_bot']['support']} \n", colors.Colors.RESET)
    
    print(colors.Colors.PURPLE + "## Weighted avg : \n")
    print(f"Precision: {classification['weighted avg']['precision']}")
    print(f"Recall: {classification['weighted avg']['recall']}")
    print(f"F1-Score: {classification['weighted avg']['f1-score']}")
    print(f"Support: {classification['weighted avg']['support']}", colors.Colors.RESET)
    
    print(colors.Colors.PURPLE + f"####\n" + colors.Colors.RESET)


def eval_model(clf, eval_dataset, algorithm, output_path_to_suspicious_hosts):
    """
    Evaluate a classifier on a given dataset and return the classifier, the predicted labels and the true labels.

    Args:
    - clf: a classifier object
    - eval_dataset: a dataset to evaluate the classifier on
    - algorithm: an integer representing the algorithm used for classification
    - output_path_to_suspicious_hosts: a string representing the path to the output file for suspicious hosts

    Returns:
    - clf: a classifier object of the trained model
    - y_pred: a list of predicted labels
    - y_test: a list of true labels
    """
    
    X_test, y_test, hosts_lists = preprocessing(eval_dataset, algorithm)
    # Test the classifier's accuracy on the test set
    y_pred_proba = clf.predict_proba(X_test)
    y_pred = clf.predict(X_test)

    print(colors.Colors.RED + f"{constants.ALGORITHMS_NAMES[algorithm]} classifier tested successfully!\n####\n" + colors.Colors.RESET)
    
    human_bot = determine_threshold(y_pred_proba)


    suspicious_hosts, hosts = false_alarm_rate(y_pred, y_test, hosts_lists)
    result_suspicious_hosts(suspicious_hosts, output_path_to_suspicious_hosts)

    # Classification report contains the precision, recall, f1-score and support that will be used for the diagrams
    print_classification_report(y_pred, y_test)

    # Post processing
    for index in human_bot:
        y_pred[index] = "human+bot" 
    return clf, y_pred, y_test
    

def main_eval(trained_model, eval_dataset, output_path_to_suspicious_hosts):
    """
    Evaluate a trained model on a given dataset and generate diagrams.

    Args:
        trained_model: Path to the trained model file.
        eval_dataset: Path to the evaluation dataset file.
        output_path_to_suspicious_hosts: Path to the output file where the suspicious hosts will be saved.

    """
    ## Load the model
    loaded_clf = saving_and_loading.load_saved_model(trained_model)

    # extract algorithm name from the path
    algorithm = str(trained_model).split("/")[2]

    ## evaluate the model
    clf, y_pred, y_test = eval_model(loaded_clf, eval_dataset, algorithm, output_path_to_suspicious_hosts)
    
    ## Diagrams
    # Those functions need to be called by hand, they only serve for the report
    # diagrams_algo.main_diagrams_algo(algorithm)
    # diagrams_metrics.main_diagrams_metrics(y_pred, y_test, algorithm)

def getting_args():
    """
    Parse command line arguments for dataset evaluation.

    Returns:
    trained_model: path to trained model
    eval_dataset: path to evaluation dataset
    output_path_to_suspicious_hosts: path to output file for suspicious hosts
    """
    parser = argparse.ArgumentParser(description="Dataset evaluation")
    parser.add_argument("--trained_model", type=pathlib.Path)
    parser.add_argument("--dataset", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args()
    
    trained_model = str(args.trained_model)
    eval_dataset = str(args.dataset)
    output_path_to_suspicious_hosts = str(args.output)
    
    return trained_model, eval_dataset, output_path_to_suspicious_hosts

if __name__ == "__main__":
    trained_model, eval_dataset, output_path_to_suspicious_hosts = getting_args()
    main_eval(trained_model, eval_dataset, output_path_to_suspicious_hosts)
