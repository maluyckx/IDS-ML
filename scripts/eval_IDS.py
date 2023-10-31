"""
Goal of the script : Evaluating the model

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

import argparse
import pathlib

import utils.constants as constants
import utils.saving_model as saving_model

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


def writing_suspicious_hosts(suspicious_hosts):
    with open(f"{constants.PATH_TO_SUSPICIOUS_HOSTS}", "w") as f:
        for host in suspicious_hosts:
            f.write(host + "\n")


def main_eval(trained_model, dataset, output):
    ## Load the model
    loaded_clf = saving_model.load_saved_model(trained_model)
    


def getting_args():
    parser = argparse.ArgumentParser(description="Dataset evaluation")
    parser.add_argument("--trained_model", type=pathlib.Path)
    parser.add_argument("--dataset", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args()
    
    trained_model = args.trained_model
    dataset = args.dataset
    output = args.output
    
    return trained_model, dataset, output

if __name__ == "__main__":
    trained_model, dataset, output = getting_args()
    main_eval(trained_model, dataset, output)
