"""
Goal of the script : Launching the training of the model and the evaluation of the dataset at the same time.

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""
import argparse
import pathlib

import eval as eval
import scripts.train as train

    
def getting_args():
    """
    Parse the command line arguments for training and evaluating the model.

    Returns:
    webclients: Path to the webclients dataset.
    bots: Path to the bots dataset.
    algo: Algorithm to use for training the model. Default is 'logistic_regression'.
    trained_model: Path to the trained model to evaluate.
    eval_dataset: Path to the dataset to evaluate.
    output_path_to_suspicious_hosts: Path to the output file containing the suspicious hosts.
    """
    parser = argparse.ArgumentParser(description="Main script for training and evaluating the model")    
    
    ## Arguments for train_IDS.py   
    parser.add_argument("--webclients", required=True, type=pathlib.Path)
    parser.add_argument("--bots", required=True, type=pathlib.Path)
    parser.add_argument("--algo", required=False, type=pathlib.Path)
    
    ## Arguments for eval_IDS.py
    parser.add_argument("--trained_model", type=pathlib.Path)
    parser.add_argument("--dataset", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    
    args = parser.parse_args()
    
    ## Assigning the arguments to variables for train.py
    webclients = str(args.webclients)
    bots = str(args.bots)
    algo = str(args.algo)
    
    if algo != "decision_tree" and algo != "logistic_regression" and algo != "neural_networks" and algo != "random_forest" and algo != "knn" and algo != "naive_bayes":
        print("Wrong algorithm : supported algorithm are `decision_tree`, `logistic_regression`, `neural_networks` or `random_forest` or `knn` or 'naive_bayes'")
        print("The script will continue with the default algorithm : logistic_regression")
        algo = "logistic_regression"

    ## Assigning the arguments to variables for eval.py
    trained_model = str(args.trained_model) 
    eval_dataset = str(args.dataset)
    output_path_to_suspicious_hosts = str(args.output)
    
    return webclients, bots, algo, trained_model, eval_dataset, output_path_to_suspicious_hosts


def main():
    """
    This function is the entry point of the program when you want to train and evaluate the model. 
    It retrieves the necessary arguments and calls the main_train and main_eval functions.
    """
    webclients, bots, algo, trained_model, eval_dataset, output_path_to_suspicious_hosts = getting_args()

    train.main_train(webclients, bots, algo, trained_model)
    eval.main_eval(trained_model, eval_dataset, output_path_to_suspicious_hosts)

if __name__ == "__main__":
    main()


