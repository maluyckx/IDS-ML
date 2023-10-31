"""
Goal of the script : Training the model

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


import argparse
import pathlib
import sys 


#### Importing the utils
import utils.parsing_dns_trace as parser
import utils.constants as constants
import utils.features as features
import utils.colors as colors

#### Importing the algorithms
sys.path.append("algorithms/decision_tree/")
# sys.path.append("algorithms/random_forest/")
# sys.path.append("algorithms/logistic_regression/")
# sys.path.append("algorithms/neural_network/")

# import decision_tree
# import random_forest
# import logistic_regression
# import neural_network

#######################################


def train_model(X_train, y_train, algorithm):
    # if algorithm == "decision_tree":
    #     clf = decision_tree.train_model(X_train, y_train)
    # elif algorithm == "random_forest":
    #     clf = random_forest.train_model(X_train, y_train)
    # elif algorithm == "logistic_regression":
    #     clf = logistic_regression.train_model(X_train, y_train)
    # elif algorithm == "neural_network":
    #     clf = neural_network.train_model(X_train, y_train)
    # else:
    #     print(colors.Colors.RED + "Error: algorithm not found" + colors.Colors.RESET)
    #     sys.exit(1)
    
    # return clf
    
    print(colors.Colors.CYAN + f"####\nTraining the {constants.ALGORITHMS_NAMES[algorithm]} classifier..." + colors.Colors.RESET)
    
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
            random_state=42,
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
    
    elif algorithm == "knn":
        clf = KNeighborsClassifier(
            n_neighbors=5,
            weights="uniform",
            algorithm="auto",
            leaf_size=30,
            p=2,
            metric="minkowski",
            metric_params=None,
            n_jobs=None
        )
        
        # diagrams.diagram_knn(clf, X_train, y_train)
    
    else:
        print("You fucked up with the algorithm")
        exit(0)
    
    
    
    clf.fit(X_train, y_train)

    print(colors.Colors.CYAN + f"{constants.ALGORITHMS_NAMES[algorithm]} classifier trained successfully!\n####\n" + colors.Colors.RESET)
    return clf


def preprocessing(bots, webclients):
    print(colors.Colors.GREEN + f"####\nParsing the bots and webclients datasets..." + colors.Colors.RESET)
    
    ### Parsing the datasets
    bots_data, webclients_data = parser.parse_training_data(bots, webclients)
    
    combined_df = features.convert_to_dataframe_training(bots_data, webclients_data)

    combined_df = features.encoding_features(combined_df)

    X_train = combined_df[constants.LIST_OF_FEATURES]
    y_train = combined_df['label']
    
    print(colors.Colors.GREEN + f"Parsed the bots and webclients datasets successfully!\n####\n" + colors.Colors.RESET)
    
    return X_train, y_train

def main_train(webclients, bots, output):
    ## Preprocessing before training : parsing and encoding the features
    X_train, y_train = preprocessing(bots, webclients)
    
    ## Training the model
    clf = train_model(X_train, y_train, "logistic_regression") # TODO À changer
    
    return clf # going to be used for evaluation
    

def getting_args():
    parser = argparse.ArgumentParser(description="Optional classifier training")
    parser.add_argument("--webclients", required=True, type=pathlib.Path)
    parser.add_argument("--bots", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args()
    webclients = args.webclients
    bots = args.bots
    output = args.output

    return webclients, bots, output

if __name__ == "__main__":
    webclients, bots, output = getting_args()
    main_train(webclients, bots, output)

