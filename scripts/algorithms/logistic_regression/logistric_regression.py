"""
Goal of the script : Using logistic regression to detect bots in a network traffic trace 

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

# ML dependencies
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pickle

# Personal dependencies
import sys
sys.path.append("../../")
import constants
import parsing_dns_trace as parser
import features
import colors

def train_logistic_regression(bots_data, webclients_data):
    print(colors.Colors.CYAN + "####\nTraining the logistic regression classifier..." + colors.Colors.RESET)

    combined_df = features.convert_to_dataframe(bots_data, webclients_data)

    combined_df = features.encoding_features(combined_df)

    X_train = combined_df[constants.LIST_OF_FEATURES]
    y_train = combined_df['label']
    
    # Train the logistic regression classifier
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
    clf.fit(X_train, y_train)
    
    print(colors.Colors.CYAN + "Logistic regression classifier trained successfully!\n####\n" + colors.Colors.RESET)
    return clf


def eval_logistic_regression(clf, path_to_eval_tcpdump1, path_to_eval_tcpdump2):
    eval_data1, eval_data2 = parser.parse_training_data(path_to_eval_tcpdump1, path_to_eval_tcpdump2)
    
    print(colors.Colors.RED + "####\nTesting the logistic regression classifier..."  + colors.Colors.RESET)
    combined_df = features.convert_to_dataframe(eval_data1, eval_data2)
    combined_df = features.encoding_features(combined_df)

    X_test = combined_df[constants.LIST_OF_FEATURES]
    y_test = combined_df['label']


    # Test the classifier's accuracy on the test set
    y_pred = clf.predict(X_test)
    accuracy = clf.score(X_test, y_test)
    print("LOGISTIC REGRESSION : Accuracy of the model : ", accuracy)

    classification = classification_report(y_true=y_test, y_pred=y_pred, target_names=['human', 'bot'])
    print(colors.Colors.YELLOW + "Classification report : \n", classification + colors.Colors.RESET)

    print(colors.Colors.RED + "Logistic regression classifier tested successfully!\n####\n" + colors.Colors.RESET)

def load_saved_logistic_regression():
    with open(f"../../../trained_models/logistic_regression/{constants.NAME_TRAINED_MODEL_LOGISTIC_REGRESSION}", "wb") as logistic_regression_saved_model:
        loaded_clf = pickle.load(logistic_regression_saved_model)
    return loaded_clf

def save_logistic_regression(clf):
    with open(f"../../../trained_models/logistic_regression/{constants.NAME_TRAINED_MODEL_LOGISTIC_REGRESSION}", "wb") as logistic_regression_saved_model:
        pickle.dump(clf, logistic_regression_saved_model)

def diagram_logistic_regression(clf):
    # find a way to make a diagram of the decision tree
    pass


def main_logistic_regression():
    # Use a first dataset to train the classifier
    bots_data, webclients_data = parser.parse_training_data(constants.PATH_TO_BOTS_TCPDUMP, constants.PATH_TO_WEBCLIENTS_TCPDUMP)

    # Training the classifier
    clf = train_logistic_regression(bots_data, webclients_data)

    # Use a second dataset to test the classifier
    eval_logistic_regression(clf, constants.PATH_TO_EVAL_TCPDUMP1, constants.PATH_TO_EVAL_TCPDUMP2)

    # Diagram of logistic regression
    diagram_logistic_regression(clf)
    
    # Save the trained classifier
    save_logistic_regression(clf)
    
if __name__ == "__main__":
    main_logistic_regression()
