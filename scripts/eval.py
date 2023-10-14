import argparse
import pathlib


# Command from the pdf : python eval.py --trained_model path/to/trained_model --dataset path/to/dataset --output path/to/suspicious.txt



parser = argparse.ArgumentParser(description="Dataset evaluation")
parser.add_argument("--dataset", required=True, type=pathlib.Path)
parser.add_argument("--trained_model", type=pathlib.Path)
parser.add_argument("--output", required=True, type=pathlib.Path)

if __name__ == "__main__":

    args = parser.parse_args()
    raise NotImplementedError
