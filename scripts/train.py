import argparse
import pathlib


# Command from the pdf : python train.py --webclients path/to/webclients_tcpdump.txt --bots path/to/bots_tcpdump.txt --output path/to/trained_model


parser = argparse.ArgumentParser(description="Optional classifier training")
parser.add_argument("--webclients", required=True, type=pathlib.Path)
parser.add_argument("--bots", required=True, type=pathlib.Path)
parser.add_argument("--output", required=True, type=pathlib.Path)

if __name__ == "__main__":

    args = parser.parse_args()
    raise NotImplementedError
