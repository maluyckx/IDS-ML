"""
Goal of the script : Script containing the diagrams for the different metrics

The data to create the diagrams are in the files located in the folder : report/results . 

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


import matplotlib.pyplot as plt 
import numpy as np


def set_vertical_xticklabels(ax, feature_combination):
    ax.set_xticks(feature_combination)
    ax.set_xticklabels(feature_combination, rotation='vertical')

def diagram_features_TP_TN_FP_FN(eval_number): # Graph 1 in the report

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


    plt.tight_layout(rect=[0, 0.03, 1, 0.95])


    plt.savefig(f"../../../diagrams/metrics/features_TP_TN_FP_FN/diagram_features_TP_TN_FP_FN_{eval_number}.png")
    

# def diagram_bayesian_detection_rate(eval_number):
#     """
#     2eme : 
#     absisse : combinaisons de features
#     ordonée : bayesian detection rate    : on devrait voir le base-rate fallacy

#     P(D|B) : probabilité de detection sachant que c'est un vrai positif
#     bayesian detection rate
#     P(B|D) : probabilité que ce soit un vrai positif sachant que c'est une detection
#     P(D) : probabilité de detection
#     P(B) : probabilité que ce soit un vrai positif

#     P(B|D) = P(D|B) * P(B) / P(D)
#     P(D) = P(D|B) * P(B) + P(D|neg B) * P(neg B)

#     """

#     feature_combination = ["All features", "Miscellaneous", "Time", "Numbers", "Combination 1", "Combination 2", "Combination 3", "Combination 4"]

#     p_bot = 12/120 # the probability that a host is a bot for eval 1 and eval 2 is the same

#     if eval_number == "eval1":
#         # Bayesian detection rates for each feature
#         detection_rate = [100, 100, 100, 58.33, 100, 100, 100, 100]
#         false_alarm_rates = [11.11, 24.07, 6.48, 4.63, 2.77, 13.88, 10.18, 24.07]
#         bayesian_detection_rates = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0]
#     elif eval_number == "eval2":
#         detection_rate = [25, 0, 66.67, 16.67, 16.67, 33.33, 16.67, 66.67]
#         false_alarm_rates = [15.7, 6.48, 68.52, 6.48, 8.33, 16.67, 9.26, 68.52]
#         bayesian_detection_rates = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0]

#     for i in range(len(bayesian_detection_rates)):
#         bayesian_detection_rates[i] = ((detection_rate[i] * p_bot) / ((detection_rate[i] * p_bot) + (false_alarm_rates[i] * (1 - p_bot)))) * 100

#     fig, ax = plt.subplots(figsize=(21, 16))
#     ax.bar(feature_combination, bayesian_detection_rates, color='skyblue')
#     ax.set_title('Bayesian Detection Rate vs Features', fontsize=20)
#     ax.set_xlabel('Features', fontsize=18)
#     ax.set_ylabel('Bayesian Detection Rate (%)', fontsize=18)
#     ax.set_xticks(feature_combination)
#     ax.set_xticklabels(feature_combination, rotation='vertical', fontsize=16)
#     current_yticks = ax.get_yticks()
#     ax.set_yticklabels(current_yticks, fontsize=16) 

#     plt.savefig(f"../../../diagrams/metrics/bayesian_detection_rate/diagram_features_bayesian_rate_{eval_number}.png")
        
   
   
def diagram_bayesian_detection_rate(eval_number):
    """
    2eme : 
    absisse : combinaisons de features
    ordonée : bayesian detection rate    : on devrait voir le base-rate fallacy

    P(D|B) : probabilité de detection sachant que c'est un vrai positif
    bayesian detection rate
    P(B|D) : probabilité que ce soit un vrai positif sachant que c'est une detection
    P(D) : probabilité de detection
    P(B) : probabilité que ce soit un vrai positif

    P(B|D) = P(D|B) * P(B) / P(D)
    P(D) = P(D|B) * P(B) + P(D|neg B) * P(neg B)

    """

    feature_combination = ["All features", "Miscellaneous", "Time", "Numbers", "Combination 1", "Combination 2", "Combination 3", "Combination 4"]

    p_bot = 12/120 # the probability that a host is a bot for eval 1 and eval 2 is the same

    if eval_number == "eval1":
        detection_rate = [100, 100, 100, 58.33, 100, 100, 100, 100]
        false_alarm_rates = [11.11, 24.07, 6.48, 4.63, 2.77, 13.88, 10.18, 24.07]
        bayesian_detection_rates = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0]
    elif eval_number == "eval2":
        detection_rate = [25, 0, 66.67, 16.67, 16.67, 33.33, 16.67, 66.67]
        false_alarm_rates = [15.7, 6.48, 68.52, 6.48, 8.33, 16.67, 9.26, 68.52]
        bayesian_detection_rates = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0]

    for i in range(len(bayesian_detection_rates)):
        bayesian_detection_rates[i] = ((detection_rate[i] * p_bot) / ((detection_rate[i] * p_bot) + (false_alarm_rates[i] * (1 - p_bot)))) * 100

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(feature_combination, bayesian_detection_rates, color='skyblue')
    ax.set_title('Bayesian Detection Rate vs Features')
    ax.set_xlabel('Features')
    ax.set_ylabel('Bayesian Detection Rate (%)')
    ax.set_xticks(feature_combination)

    plt.savefig(f"../../../diagrams/metrics/bayesian_detection_rate/diagram_features_bayesian_rate_{eval_number}.png")
   
        
        
def diagram_accuracy_false_alarm_rate(eval_number): # Graph 3 in the report
    """
    Fait avec algo logistic regression
        
    """
    feature_combination = ["All features", "Miscellaneous", "Time", "Numbers", "Combination 1", "Combination 2", "Combination 3", "Combination 4"]


    if eval_number == "eval1":
        accuracy_rates = [90, 78.3, 94.16, 91.66, 97.5, 97.5, 90.83, 78.33]
        false_alarm_rates = [11.11, 24.07, 6.48, 4.63, 2.77, 13.88, 10.18, 24.07]
        detection_rate = [100, 100, 100, 58.33, 100, 100, 100, 100]
    elif eval_number == "eval2":
        accuracy_rates = [78.3, 84.16, 35.0, 85.83, 84.17, 78.33, 83.33, 35.0]
        false_alarm_rates = [15.7, 6.48, 68.52, 6.48, 8.33, 16.67, 9.26, 68.52]
        detection_rate = [25, 0, 66.67, 16.67, 16.67, 33.33, 16.67, 66.67]

    fig, ax = plt.subplots(figsize=(12, 6))


    bar_width = 0.23
    indices = np.arange(len(feature_combination))

    bar1 = ax.bar(indices, accuracy_rates, bar_width, label='Accuracy', color='blue')
    bar2 = ax.bar(indices + bar_width, false_alarm_rates, bar_width, label='False Alarm', color='red')
    bar3 = ax.bar(indices + bar_width*2, detection_rate, bar_width, label='Detection Rate', color='green')

    ax.set_title('Accuracy and False alarm rates by feature')
    ax.set_xlabel('Features')
    ax.set_ylabel('Percentage')
    ax.set_xticks(indices + bar_width)
    ax.set_xticklabels(feature_combination)
    ax.legend()

    plt.savefig(f"../../../diagrams/metrics/accuracy_false_alarm_rate/diagram_features_accuracy_false_alarm_rate_{eval_number}.png")
    
def main_diagrams_metrics():
    
    for element in ["eval1", "eval2"]:
        diagram_features_TP_TN_FP_FN(element)
        diagram_bayesian_detection_rate(element)
        diagram_accuracy_false_alarm_rate(element)
        


if __name__ == "__main__":
    main_diagrams_metrics()
