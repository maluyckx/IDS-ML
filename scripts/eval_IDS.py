"""
Goal of the script : Evaluating the model

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

import argparse
import pathlib

import scripts.utils.constants as constants


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


def writing_suspicious_hosts(suspicious_hosts):
    with open(f"{constants.PATH_TO_SUSPICIOUS_HOSTS}", "w") as f:
        for host in suspicious_hosts:
            f.write(host + "\n")


def main_eval(dataset, trained_model, output):
    pass


def getting_args():
    parser = argparse.ArgumentParser(description="Dataset evaluation")
    parser.add_argument("--dataset", required=True, type=pathlib.Path)
    parser.add_argument("--trained_model", type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args()
    
    dataset = args.dataset
    trained_model = args.trained_model
    output = args.output
    
    return dataset, trained_model, output

if __name__ == "__main__":
    dataset, trained_model, output = getting_args()
    main_eval(dataset, trained_model, output)
