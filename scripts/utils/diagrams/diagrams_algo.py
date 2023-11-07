"""
Goal of the script : Script containing the code to create the diagrams for the different algorithms.

The data to create the diagrams are in the files located in the folder : report/results.

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

import numpy as np
import matplotlib.pyplot as plt


def diagram_algo_comparison_bot(eval_number):
    """
    Generates a bar chart comparing the precision, recall and F1-score of different algorithms for bot detection.

    Args:
        - eval_number: evaluation number. It can be either "eval1" or "eval2".

    """

    algorithms = ["Logistic regression", "Decision tree",
                  "KNN", "Neural networks", "Random forest"]

    if eval_number == "eval1":
        precision = [80, 100, 54.54, 33.33, 52.17]
        recall = [100, 100, 100, 100, 100]
        f1_score = [88.89, 100, 70.58, 50, 68.57]
    elif eval_number == "eval2":
        precision = [18.18, 10, 10, 14.51, 13.88]
        recall = [16.66, 100, 8.33, 75, 41.66]
        f1_score = [17.39, 18.18, 9.09, 24.32, 20.83]

    fig, ax = plt.subplots(figsize=(12, 6))

    bar_width = 0.23
    indices = np.arange(len(algorithms))

    bar1 = ax.bar(indices, precision, bar_width,
                  label='Precision', color='blue')
    bar2 = ax.bar(indices + bar_width, recall,
                  bar_width, label='recall', color='red')
    bar3 = ax.bar(indices + bar_width*2, f1_score,
                  bar_width, label='F1-score', color='green')

    ax.set_title(f'Metrics by algorithm for bot detection for {eval_number}')
    ax.set_xlabel('Algorithm')
    ax.set_ylabel('Percentage')
    ax.set_xticks(indices + bar_width)
    ax.set_xticklabels(algorithms)
    ax.legend()

    plt.savefig(
        f"../../../diagrams/algos/diagram_bot_metrics_algo_{eval_number}.png")


def diagram_algo_comparison_human(eval_number):
    """
    Generates a bar chart comparing the precision, recall and F1-score of different algorithms for human detection.

    Args:
        - eval_number: evaluation number. It can be either "eval1" or "eval2".

    """
    algorithms = ["Logistic regression", "Decision tree",
                  "KNN", "Neural networks", "Random forest"]

    if eval_number == "eval1":
        precision = [100, 100, 100, 100, 100]
        recall = [97.22, 100, 90.74, 77.77, 89.81]
        f1_score = [98.59, 100, 95.14, 87.5, 94.63]
    elif eval_number == "eval2":
        precision = [90.82, 0, 90, 94.82, 91.66]
        recall = [91.66, 0, 91, 50.92, 71.29]
        f1_score = [91.24, 0, 90.8, 66.26, 80.2]

    fig, ax = plt.subplots(figsize=(12, 6))

    bar_width = 0.23
    indices = np.arange(len(algorithms))

    bar1 = ax.bar(indices, precision, bar_width,
                  label='Precision', color='blue')
    bar2 = ax.bar(indices + bar_width, recall,
                  bar_width, label='recall', color='red')
    bar3 = ax.bar(indices + bar_width*2, f1_score,
                  bar_width, label='F1-score', color='green')

    ax.set_title(f'Metrics by algorithm for human detection for {eval_number}')
    ax.set_xlabel('Algorithm')
    ax.set_ylabel('Percentage')
    ax.set_xticks(indices + bar_width)
    ax.set_xticklabels(algorithms)
    ax.legend()

    plt.savefig(
        f"../../../diagrams/algos/diagram_human_metrics_algo_{eval_number}.png")


def main_diagrams_algo():
    """
    This function generates comparison diagrams for algorithm performance on evaluation datasets.
    """
    diagram_algo_comparison_bot("eval1")
    diagram_algo_comparison_bot("eval2")

    diagram_algo_comparison_human("eval1")
    diagram_algo_comparison_human("eval2")


if __name__ == "__main__":
    main_diagrams_algo()
