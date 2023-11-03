"""
Goal of the script : Script containing the diagrams for the different metrics

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


def diagram_features_TP_TN_FP_FN():
    # Define the feature indices

    feature_combination = ["All features", "Miscellaneous", "Time", "Numbers", "Combination 1", "Combination 2", "Combination 3", "Combination 4"]
    tp_per_features = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    tn_avg_per_feature = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    fp_avg_per_feature = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    fn_avg_per_feature = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    # Create a figure with 4 subplots
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(14, 10))
    fig.suptitle('Classification outcomes vs. set of features', fontsize=16)

    # True Positive
    axes[0, 0].bar(feature_combination, tp_avg_per_feature, color='green')
    axes[0, 0].set_title('True Positive vs. Features')
    axes[0, 0].set_xlabel('Feature')
    axes[0, 0].set_ylabel('True Positive Average Impact')
    axes[0, 0].set_xticks(feature_indices)

    # True Negative
    axes[0, 1].bar(feature_combination, tn_avg_per_feature, color='blue')
    axes[0, 1].set_title('True Negative vs. Features')
    axes[0, 1].set_xlabel('Feature')
    axes[0, 1].set_ylabel('True Negative Average Impact')
    axes[0, 1].set_xticks(feature_indices)

    # False Positive
    axes[1, 0].bar(feature_combination, fp_avg_per_feature, color='red')
    axes[1, 0].set_title('False Positive vs. Features')
    axes[1, 0].set_xlabel('Feature')
    axes[1, 0].set_ylabel('False Positive Average Impact')
    axes[1, 0].set_xticks(feature_indices)

    # False Negative
    axes[1, 1].bar(feature_combination, fn_avg_per_feature, color='orange')
    axes[1, 1].set_title('False Negative vs. Features')
    axes[1, 1].set_xlabel('Feature')
    axes[1, 1].set_ylabel('False Negative Average Impact')
    axes[1, 1].set_xticks(feature_indices)

    # Adjust the layout
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Show the plots
    plt.show()

def main_diagrams_metrics():
    pass




if __name__ == "__main__":
    main_diagrams_metrics()
