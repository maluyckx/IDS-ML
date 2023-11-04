"""
Goal of the script : Training the model

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


import argparse
import pathlib
import sys 

#### ML dependencies
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


#### Importing the utils
import utils.parsing_dns_trace as parser
import utils.constants as constants
import utils.features as features
import utils.colors as colors

import scripts.utils.saving_and_loading as saving_and_loading


def train_model(X_train, y_train, algorithm):   
    """
    Train a classifier on the given training data using the specified algorithm.

    Args:
        X_train: Training data.
        y_train: Training labels.
        algorithm: The name of the algorithm to use for training.
            - decision_tree
            - logistic_regression
            - random_forest
            - neural_networks
            - knn
            - naive_bayes

    Returns:
        The trained classifier.
    """
     
    print(colors.Colors.CYAN + f"####\nTraining the {constants.ALGORITHMS_NAMES[algorithm]} classifier..." + colors.Colors.RESET)
    
    if algorithm == "decision_tree":
            clf = DecisionTreeClassifier(
                criterion='gini',
                splitter='best',
                max_depth=None,  
                min_samples_split=2,  
                min_samples_leaf=1,  #
                min_weight_fraction_leaf=0,  
                max_features=None, 
                random_state=None,  
                max_leaf_nodes=None,  
                min_impurity_decrease=0.0, 
                class_weight=None, 
                ccp_alpha=0 
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
        clf = RandomForestClassifier(
            n_estimators=100,
            criterion="gini",
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            min_weight_fraction_leaf=0,
            max_features="sqrt",
            max_leaf_nodes=None,
            min_impurity_decrease=0,
            bootstrap=True,
            oob_score=False,
            n_jobs=None,
            random_state=None,
            verbose=0,
            warm_start=False,
            class_weight=None,
            ccp_alpha=0,
            max_samples=None
        )       
        
    elif algorithm == "neural_networks":
        clf = MLPClassifier(
            activation="relu",
            solver="adam",
            alpha=0.0001,
            batch_size="auto",
            learning_rate="constant",
            learning_rate_init=0.001,
            power_t=0.5,
            max_iter=200,
            shuffle=True,
            random_state=None,
            tol=0.0001,
            verbose=False,
            warm_start=False,
            momentum=0.9,
            nesterovs_momentum=True,
            early_stopping=False,
            validation_fraction=0.1,
            beta_1=0.9,
            beta_2=0.999,
            epsilon=1e-08,
            n_iter_no_change=10,
            max_fun=15000
        )
          
        
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

    elif algorithm == "naive_bayes":
        clf = GaussianNB()
    else:
        print("The algorithm provided is not supported")
        exit(0)
    
    
    clf.fit(X_train, y_train)

    print(colors.Colors.CYAN + f"{constants.ALGORITHMS_NAMES[algorithm]} classifier trained successfully!\n####\n" + colors.Colors.RESET)
    return clf


def preprocessing(bots, webclients):
    """
    Preprocesses the bots and webclients datasets by parsing the data, converting it to a dataframe, encoding the features and returning the training data and labels.
    
    Args:
    bots: Path to the bots dataset.
    webclients: Path to the webclients dataset.
    
    Returns:
    X_train: Training data.
    y_train: Training labels.
    """
    
    print(colors.Colors.GREEN + f"####\nParsing the bots and webclients datasets..." + colors.Colors.RESET)
    
    ### Parsing the datasets
    bots_data, webclients_data = parser.parse_training_data(bots, webclients)
    
    combined_df = features.convert_to_dataframe_training(bots_data, webclients_data)
    combined_df = features.encoding_features(combined_df)

    X_train = combined_df[constants.LIST_OF_FEATURES_COMBI1]
    y_train = combined_df['label']
    
    print(colors.Colors.GREEN + f"Parsed the bots and webclients datasets successfully!\n####\n" + colors.Colors.RESET)
        
    return X_train, y_train

def main_train(webclients, bots, algorithm, output_path_saved_model):
    """
    Train a machine learning model to detect bots based on webclient data.

    Args:
        webclients: Path to the webclients dataset.
        bots: Path to the bots dataset.
        algorithm: Machine learning algorithm to use for training.
        output_path_saved_model: Path to save the trained model.

    Returns:
        Trained machine learning model.
    """
    
    ## Preprocessing before training : parsing and encoding the features
    X_train, y_train = preprocessing(bots, webclients)

    ## Generating the tsne
    visualization_tsne(X_train, y_train)
    
    ## Training the model
    clf = train_model(X_train, y_train, algorithm) 
    
    ## Saving the model
    saving_and_loading.save_trained_model(clf, algorithm, output_path_saved_model)
    
    return clf

def visualization_tsne(X, y, perplexity=30):
    """
    Visualize the data using t-SNE.

    Args:
    X: The data to visualize.
    y: The labels of the data.
    perplexity: The perplexity parameter for t-SNE.
    """    
    tsne = TSNE(n_components=2, random_state=42, perplexity=perplexity)
    X_tsne = tsne.fit_transform(X)

    colors = []
    for i in y:
        if i == "bot":
            colors.append("red")
        elif i == "human":
            colors.append("blue")

    plt.figure(figsize=(10, 5))
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=colors)
    plt.colorbar()  # Shows the color scale.
    plt.title('t-SNE visualization of the data')
    plt.savefig(f"./visualization_tsne_dataset.png")
    

def getting_args():
    """
    Parse command line arguments for classifier training.

    Returns:
    webclients: Path to webclients dataset.
    bots: Path to bots dataset.
    algo: Algorithm to use for training. Default is logistic_regression.
    output_path_to_saved_model: Path to save the trained model.
    """
    
    parser = argparse.ArgumentParser(description="Optional classifier training")
    parser.add_argument("--webclients", required=True, type=pathlib.Path)
    parser.add_argument("--bots", required=True, type=pathlib.Path)
    parser.add_argument("--algo", required=False, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args()
    webclients = str(args.webclients)
    bots = str(args.bots)
    algo = str(args.algo)
    output_path_to_saved_model = str(args.output)
    
    if algo != "decision_tree" and algo != "logistic_regression" and algo != "neural_networks" and algo != "random_forest" and algo != "knn" and algo != "naive_bayes":
        print("Wrong algorithm : supported algorithm are `decision_tree`, `logistic_regression`, `neural_networks` or `random_forest` or `knn` or `naive_bayes`")
        print("The script will continue with the default algorithm : logistic_regression")
        algo = "logistic_regression"
        output_path_to_saved_model = "../trained_models/decision_tree/trained_model_decision_tree.pkl"

    return webclients, bots, algo, output_path_to_saved_model

if __name__ == "__main__":
    webclients, bots, algo, output_path_saved_model = getting_args()
    clf = main_train(webclients, bots, algo, output_path_saved_model)