"""
Goal of the script : Using a decision tree classifier to detect bots in a network traffic trace 

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

# ML dependencies

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pickle

# Graphics dependencies
from sklearn.tree import export_graphviz
import graphviz

# # Personal dependencies
import sys
sys.path.append("../")
import utils.parsing_dns_trace as parser
import utils.constants as constants
import utils.features as features
import utils.colors as colors


def train_model(bots_data, webclients_data, algorithm):
    print(colors.Colors.CYAN +
          f"####\nTraining the {constants.ALGORITHMS_NAMES[algorithm]} classifier..." + colors.Colors.RESET)

    combined_df = features.convert_to_dataframe(bots_data, webclients_data)

    combined_df = features.encoding_features(combined_df)

    X_train = combined_df[constants.LIST_OF_FEATURES]
    y_train = combined_df['label']

    # print("X train : ", X_train)
    # print("y train : ", y_train)

    if algorithm == "decision_tree":
        clf = DecisionTreeClassifier(
            criterion='gini',
            splitter='best',
            max_depth=100,  # completement arbitraire
            min_samples_split=20,  # completement arbitraire
            min_samples_leaf=10,  # completement arbitraire
            min_weight_fraction_leaf=0.0,  # completement arbitraire
            max_features=None,  # use all features
            random_state=None,  # random seed
            max_leaf_nodes=None,  # completement arbitraire
            min_impurity_decrease=0.0,  # completement arbitraire
            class_weight=None,  # use all classes
            ccp_alpha=0.0  # completement arbitraire
        )
    elif algorithm == "logistic_regression":
        clf = LogisticRegression(
            penalty="l2",
            dual=False,
            tol=0.0001,
            C=1,
            fit_intercept=True,
            intercept_scaling=1,
            class_weight=None,
            random_state=None,
            solver="liblinear",
            max_iter=100,
            multi_class="auto",
            verbose=0,
            warm_start=False,
            n_jobs=None,
            l1_ratio=None
        )
    elif algorithm == "random_forest":
        pass
    elif algorithm == "neural_networks":
        pass
    else:
        print("You fucked up with the algortihm")
        exit(0)

    clf.fit(X_train, y_train)

    print(colors.Colors.CYAN +
          f"{constants.ALGORITHMS_NAMES[algorithm]} classifier trained successfully!\n####\n" + colors.Colors.RESET)
    return clf


def eval_model(clf, path_to_eval_tcpdump1, path_to_eval_tcpdump2, algorithm):
    eval_data1, eval_data2 = parser.parse_training_data(
        path_to_eval_tcpdump1, path_to_eval_tcpdump2)

    print(colors.Colors.RED +
          f"####\nTesting the {constants.ALGORITHMS_NAMES[algorithm]} classifier..." + colors.Colors.RESET)
    combined_df = features.convert_to_dataframe(eval_data1, eval_data2)

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

    print(colors.Colors.RED +
          f"{constants.ALGORITHMS_NAMES[algorithm]} classifier tested successfully!\n####\n" + colors.Colors.RESET)


def load_saved_model(algorithm):
    with open(f"../../trained_models/{algorithm}/{constants.NAME_TRAINED_MODEL[algorithm]}", 'rb') as saved_model:
        loaded_clf = pickle.load(saved_model)
    return loaded_clf


def save_trained_model(clf, algorithm):
    with open(f"../../trained_models/{algorithm}/{constants.NAME_TRAINED_MODEL[algorithm]}", "wb") as saved_model:
        pickle.dump(clf, saved_model)


def diagram(clf):
    """dot_data = export_graphviz(clf, out_file=None,
                            feature_names=constants.LIST_OF_FEATURES,
                            class_names=['bot', 'webclient'],
                            filled=True, rounded=True, special_characters=True)

    graph = graphviz.Source(dot_data)
    graph.render("decision_tree")"""
    pass


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

    answer = input("Chose a model to train : ")
    if answer == "1":
        algorithm = "decision_tree"
    elif answer == "2":
        algorithm = "logistic_regression"
    elif answer == "3":
        algorithm = "random_forest"
    elif answer == "4":
        algorithm = "neural_networks"
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

    # Diagram of the decision tree
    diagram(clf)

    # Save the trained classifier
    save_trained_model(clf, algorithm)

    print("#" * 50)


if __name__ == "__main__":
    main()
