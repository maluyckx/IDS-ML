"""
Goal of the script : Launching the training of the model and the evaluation of the dataset

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""
import argparse
import pathlib

import scripts.eval_IDS as eval_IDS
import scripts.train_IDS as train_IDS

import constants

def main():
    getting_args()
    
    train_IDS.main_train()
    eval_IDS.main_eval()
    
def getting_args():
    ## Train IDS
    parser = argparse.ArgumentParser(description="Optional classifier training")
    parser.add_argument("--webclients", required=True, type=pathlib.Path)
    parser.add_argument("--bots", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    
    ## Eval IDS
    parser = argparse.ArgumentParser(description="Dataset evaluation")
    parser.add_argument("--dataset", required=True, type=pathlib.Path)
    parser.add_argument("--trained_model", type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    
    args = parser.parse_args()
    
    webclients = args.webclients
    bots = args.bots
    output = args.output

    dataset = args.dataset
    trained_model = args.trained_model
    output = args.output
    
    return webclients, bots, output, dataset, trained_model, output


if __name__ == "__main__":
    main()


