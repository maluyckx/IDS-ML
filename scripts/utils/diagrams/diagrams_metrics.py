"""
Goal of the script : Script containing the diagrams for the different metrics

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


import matplotlib.pyplot as plt 
import numpy as np

# Function to set x-tick labels vertically
def set_vertical_xticklabels(ax, feature_combination):
    ax.set_xticks(feature_combination)
    ax.set_xticklabels(feature_combination, rotation='vertical')

def diagram_features_TP_TN_FP_FN(eval_number): # Graph 1 in the report
    # Define the feature indices

    feature_combination = ["All features", "Miscellaneous", "Time", "Numbers", "Combination 1", "Combination 2", "Combination 3", "Combination 4"]
    
    
    if eval_number == "eval1":
        tp_per_features = [12, 12, 12, 7, 12, 12, 12, 12]
        fp_per_feature = [12, 26, 7, 5, 3, 15, 11, 26]
        fn_per_feature = [0, 0, 0, 5, 0, 0, 0, 0]
        tn_per_feature = [96, 82, 101, 103, 105, 93, 97, 82]
    elif eval_number == "eval2":
        tp_per_features = [3, 0, 8, 2, 2, 4, 2, 8]
        fp_per_feature = [17, 7, 74, 7, 9, 18, 10, 74]
        fn_per_feature = [9, 12, 4, 10, 10, 8, 10, 4]
        tn_per_feature = [91, 101, 34, 101, 99, 90, 98, 34]


    # Create a figure with 4 subplots
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))
    fig.suptitle('Classification outcomes vs. set of features', fontsize=16)

    # True Positive
    axes[0, 0].bar(feature_combination, tp_per_features, color='green')
    axes[0, 0].set_title('True positive vs. Features')
    axes[0, 0].set_xlabel('Feature')
    axes[0, 0].set_ylabel('True positive average Iimpact')
    axes[0, 0].set_xticks(feature_combination)
    set_vertical_xticklabels(axes[0, 0], feature_combination)

    # True Negative
    axes[0, 1].bar(feature_combination, fp_per_feature, color='blue')
    axes[0, 1].set_title('True negative vs. Features')
    axes[0, 1].set_xlabel('Feature')
    axes[0, 1].set_ylabel('True negative average impact')
    axes[0, 1].set_xticks(feature_combination)
    set_vertical_xticklabels(axes[0, 1], feature_combination)

    # False Positive
    axes[1, 0].bar(feature_combination, fn_per_feature, color='red')
    axes[1, 0].set_title('False positive vs. Features')
    axes[1, 0].set_xlabel('Feature')
    axes[1, 0].set_ylabel('False positive average impact')
    axes[1, 0].set_xticks(feature_combination)
    set_vertical_xticklabels(axes[1, 0], feature_combination)

    # False Negative
    axes[1, 1].bar(feature_combination, tn_per_feature, color='orange')
    axes[1, 1].set_title('False negative vs. Features')
    axes[1, 1].set_xlabel('Feature')
    axes[1, 1].set_ylabel('False negative average impact')
    axes[1, 1].set_xticks(feature_combination)
    set_vertical_xticklabels(axes[1, 1], feature_combination)

    # Adjust the layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Show the plots
    plt.savefig(f"../../../diagrams/metrics/1_graph/diagram_features_TP_TN_FP_FN_{eval_number}.png")
    
    
    
# def diagram_bayesian_detection_rate(eval_number): # Graph 2 in the report
#     """
#     2eme : 
# absisse : combinaisons de features
# ordonée : bayesian detection rate    : on devrait voir le base-rate fallacy

#     P(D|B) : probabilité de detection sachant que c'est un vrai positif
#     bayesian detection rate
#     P(B|D) : probabilité que ce soit un vrai positif sachant que c'est une detection
#     P(D) : probabilité de detection
#     P(B) : probabilité que ce soit un vrai positif
    
#     P(B|D) = P(D|B) * P(B) / P(D)
#     P(D) = P(D|B) * P(B) + P(D|neg B) * P(neg B)
    
#     """

#     feature_combination = ["All features", "Miscellaneous", "Time", "Numbers", "Combination 1", "Combination 2", "Combination 3", "Combination 4"]

#     # p_bot = 

#     if eval_number == "eval1":
#         # Bayesian detection rates for each feature
#         detection_rates = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0]
#         false_positive_rates = [11.11, 24.07, 6.48, 4.63, 2.77, 13.88, 10.18, 24.07]
#         bayesian_detection_rates = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0]


#     elif eval_number == "eval2":
#         bayesian_detection_rates = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0]

#     # for i in range(len(bayesian_detection_rates)):
#     #     detection_rates[i] * 

#     # Create a bar plot
#     plt.figure(figsize=(10, 6))
#     plt.bar(feature_combination, bayesian_detection_rates, color='skyblue')

#     # Set the title and labels
#     plt.title('Bayesian Detection Rate vs Features')
#     plt.xlabel('Features')
#     plt.ylabel('Bayesian Detection Rate (%)')

#     plt.savefig(f"../../../diagrams/metrics/2_graph/diagram_features_bayesian_rate_{eval_number}.png")

    
def diagram_accuracy_false_alarm_rate(eval_number): # Graph 3 in the report
    """
    3eme graphe : 
absisse : deux columns pour represnter une combination de features (premiere column = accuracy et deuxieme column = false alarm rate)
ordonné : 0 à 100%
    
    """
    feature_combination = ["All features", "Miscellaneous", "Time", "Numbers", "Combination 1", "Combination 2", "Combination 3", "Combination 4"]


    if eval_number == "eval1":
        accuracy_rates = [90, 78.3, 94.16, 91.66, 97.5, 97.5, 90.83, 78.33]
        false_alarm_rates = [11.11, 24.07, 6.48, 4.63, 2.77, 13.88, 10.18, 24.07]
    elif eval_number == "eval2":
        accuracy_rates = [78.3, 84.16, 35.0, 85.83, 84.17, 78.33, 83.33, 35.0]
        false_alarm_rates = [15.7, 6.48, 68.52, 6.48, 8.33, 16.67, 9.26, 68.52]
  
    # Set up the plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Define the width of a bar and positions
    bar_width = 0.35
    indices = np.arange(len(feature_combination))

    # Plotting both accuracy and false alarm rates
    bar1 = ax.bar(indices, accuracy_rates, bar_width, label='Accuracy', color='blue')
    bar2 = ax.bar(indices + bar_width, false_alarm_rates, bar_width, label='False Alarm', color='red')

    # Set the title and labels
    ax.set_title('Accuracy and False alarm rates by feature')
    ax.set_xlabel('Features')
    ax.set_ylabel('False alarm rates (%)')
    ax.set_xticks(indices + bar_width / 2)
    ax.set_xticklabels(feature_combination)
    ax.legend()

    plt.savefig(f"../../../diagrams/metrics/3_graph/diagram_features_accuracy_false_alarm_rate_{eval_number}.png")
    
def main_diagrams_metrics():
    
    for element in ["eval1", "eval2"]:
        diagram_features_TP_TN_FP_FN(element)
        # diagram_bayesian_detection_rate(element)
        diagram_accuracy_false_alarm_rate(element)
        




if __name__ == "__main__":
    main_diagrams_metrics()
