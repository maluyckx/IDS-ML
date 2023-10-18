"""
Goal of the script : Training the model

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub ?
"""


import argparse
import pathlib


def main_train(webclients, bots, output):
    pass



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

