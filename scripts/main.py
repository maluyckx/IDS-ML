"""
Goal of the script : Launching the training of the model and the evaluation of the dataset

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

import scripts.eval_IDS as eval_IDS
import scripts.train_IDS as train_IDS


def main():
    train_IDS.main_train()
    eval_IDS.main_eval()
    
def getting_args():
    # Full de paramètres a demander en args ici
    pass


if __name__ == "__main__":
    main()


