"""
Goal of the script : Training the model

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub ?
"""


import argparse
import pathlib



parser = argparse.ArgumentParser(description="Optional classifier training")
parser.add_argument("--webclients", required=True, type=pathlib.Path)
parser.add_argument("--bots", required=True, type=pathlib.Path)
parser.add_argument("--output", required=True, type=pathlib.Path)

if __name__ == "__main__":

    args = parser.parse_args()
    raise NotImplementedError
