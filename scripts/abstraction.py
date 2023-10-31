"""
Goal of the script : Using a decision tree classifier to detect bots in a network traffic trace 

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""



# Graphics dependencies
from sklearn.tree import export_graphviz
import graphviz
import numpy as np

# # Personal dependencies
import sys
sys.path.append("./utils/")
import utils.parsing_dns_trace as parser
import utils.constants as constants
import utils.features as features
import utils.colors as colors
import utils.diagrams as diagrams


def eval_model(clf, path_to_eval_tcpdump1, path_to_eval_tcpdump2, algorithm):
    
    eval1_data = parser.parse_eval_data(path_to_eval_tcpdump1)
    #eval2_data = parser.parse_eval_data(path_to_eval_tcpdump2)
    
    print(colors.Colors.RED + f"####\nTesting the {constants.ALGORITHMS_NAMES[algorithm]} classifier..." + colors.Colors.RESET)
    
    combined_df = features.convert_to_dataframe_testing(eval_data1, eval_data2)

    combined_df = features.encoding_features(combined_df)

    X_test = combined_df[constants.LIST_OF_FEATURES]
    y_test = combined_df['label']

    # Test the classifier's accuracy on the test set
    y_pred = clf.predict(X_test)
    accuracy = clf.score(X_test, y_test)
    print("Accuracy of the model : ", accuracy)

    classification = classification_report(
        y_true=y_test, y_pred=y_pred, target_names=['human', 'bot'])
    print(colors.Colors.YELLOW + "Classification report : \n",
          classification + colors.Colors.RESET)

    diagrams.diagram_logistic_regression(clf, X_test, y_test)
    
    print(colors.Colors.RED +
          f"{constants.ALGORITHMS_NAMES[algorithm]} classifier tested successfully!\n####\n" + colors.Colors.RESET)






def main():

    # Ask if the user wants to load a trained model
    # If yes, load the model
    # If no, train a new model
    # If the user enters a wrong input, ask again
    # while True:
    #     answer = input("Do you want to load a trained model ? (y/n) ")
    #     if answer == "y":
    #         clf = load_saved_model()
    #         break
    #     elif answer == "n":
    #         clf = train_model()
    #         break
    #     else:
    #         print("Wrong input, please try again")
    #         continue

    # List the different models to chose
    print("#" * 50)
    print("List of available models : ")
    print("1. Decision tree")
    print("2. Logistic regression")
    print("3. Random forest")
    print("4. Neural networks")
    print("5. KNN")

    answer = input("Choose a model to train : ")
    if answer == "1":
        algorithm = "decision_tree"
    elif answer == "2":
        algorithm = "logistic_regression"
    elif answer == "3":
        algorithm = "random_forest"
    elif answer == "4":
        algorithm = "neural_networks"
    elif answer == "5":
        algorithm = "knn"
    else:
        print("Wrong input, please try again")
        exit(0)

    # Use a first dataset to train the classifier
    bots_data, webclients_data = parser.parse_training_data(
        constants.PATH_TO_BOTS_TCPDUMP, constants.PATH_TO_WEBCLIENTS_TCPDUMP)

    # Training the classifier
    clf = train_model(bots_data, webclients_data, algorithm)

    # Use a second dataset to test the classifier
    eval_model(clf, constants.PATH_TO_EVAL_TCPDUMP1,
               constants.PATH_TO_EVAL_TCPDUMP2, algorithm)


    # degeulasse mais j'ai pas le temps de faire mieux
    # if algorithm == "decision_tree":
    #     diagram.diagram_decision_tree(clf)

    # elif algorithm == "logistic_regression":
    #     pass
    
    # elif algorithm == "knn":
    #     diagrams.diagram_knn(clf)
        
    # elif algorithm == "random_forest":
    #     pass
    
    # elif algorithm == "neural_networks":
    #     pass

    # Save the trained classifier
    save_trained_model(clf, algorithm)

    print("#" * 50)


if __name__ == "__main__":
    main()
