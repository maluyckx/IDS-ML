"""
Goal of the script : Script containing the diagrams for the different metrics

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


import matplotlib.pyplot as plt 

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
        tp_per_features = [0, 0, 0, 0, 0, 0, 0, 0]
        fp_per_feature = [0, 0, 0, 0, 0, 0, 0, 0]
        fn_per_feature = [0, 0, 0, 0, 0, 0, 0, 0]
        tn_per_feature = [0, 0, 0, 0, 0, 0, 0, 0]


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
    
    
    
def diagram_bayesian_detection_rate(eval_number): # Graph 2 in the report
    """
    2eme : 
absisse : combinaisons de features
ordonée : bayesian detection rate    : on devrait voir le base-rate fallacy
    
    """
    pass
    
    
def diagram_accuracy_false_alarm_rate(eval_number): # Graph 3 in the report
    """
    3eme graphe : 
absisse : deux columns pour represnter une combination de features (premiere column = accuracy et deuxieme column = false alarm rate)
ordonné : 0 à 100%
    
    """
    
    
    pass
    
    
def diagram_roc_curve(eval_number): # Graph 4 in the report
    # we should not do it in my opinion
    pass
    
    
def main_diagrams_metrics():
    
    for element in ["eval1", "eval2"]:
        diagram_features_TP_TN_FP_FN(element)
        diagram_bayesian_detection_rate(element)
        diagram_accuracy_false_alarm_rate(element)
        




if __name__ == "__main__":
    main_diagrams_metrics()
