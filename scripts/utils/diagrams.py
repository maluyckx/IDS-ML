"""
Goal of the script : Script containing the diagrams for the different algorithms

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

def diagram_decision_tree(clf):
    pass

def diagram_logistic_regression(clf, X, y):
    clf.fit(X, y)

    # Get the regression coefficients and intercept
    beta_0 = clf.intercept_[0]
    beta_1 = clf.coef_[0][0]

    # Create an array of values for your feature
    x_values = np.linspace(X.min(), X.max(), 300)

    # Compute the sigmoid function values for each point
    y_values = 1 / (1 + np.exp(-(beta_0 + beta_1 * x_values)))

    # Plot your data points
    plt.scatter(X, y, color='blue', label='Data points')
    # Plot the logistic regression curve
    plt.plot(x_values, y_values, color='red', label='Logistic Regression Curve')
    plt.legend()
    plt.show()

    # h = .02  # step size in the mesh
    
    # x_min, x_max = X.iloc[:, 0].min() - .5, X.iloc[:, 0].max() + .5
    # y_min, y_max = X.iloc[:, 1].min() - .5, X.iloc[:, 1].max() + .5
    # hello = np.arange(x_min, x_max, h)
    # print(hello)
    # otherhello = np.arange(y_min, y_max, h)
    # print(otherhello.shape)
    # xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h), sparse=True)

    # Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    # Z = Z.reshape(xx.shape)

    # plt.contourf(xx, yy, Z, alpha=0.8)
    # plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', marker='o', linewidth=1)
    # plt.xlabel('Feature 1')
    # plt.ylabel('Feature 2')
    # plt.title('Logistic Regression Decision Boundary')
    # plt.show()

    
    
    

def diagram_knn(clf, x_train, y_train):
    # Because we have more features than 2, we need to reduce the dimensionality of our data to be able to visualize it
    tsne = TSNE(n_components=2, random_state=0)
    X_tsne = tsne.fit_transform(x_train)

    clf.fit(x_train, y_train) # we need to train our model with the original space, the high-dimensional one, and not the data given by t-SNE because this method just helps us to visualize data by reducing it, it is not a preprocessing step. If we train with these data using t-SNE, our model will be biased



    xx, yy = np.meshgrid(np.linspace(X_tsne[:, 0].min() - 1, X_tsne[:, 0].max() + 1, 100),
                        np.linspace(X_tsne[:, 1].min() - 1, X_tsne[:, 1].max() + 1, 100))
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, alpha=0.4)
    plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y_train, cmap=plt.cm.RdYlBu)
    plt.xlabel('t-SNE feature 1')
    plt.ylabel('t-SNE feature 2')
    plt.title('KNN t-SNE')
    plt.show()

def diagram_random_forest(clf):
    pass

def diagram_neural_networks(clf):
    pass





def main_diagrams(algorithm):
    if algorithm == "decision_tree":
        diagram_decision_tree()
        
    elif algorithm == "logistic_regression":
        diagram_logistic_regression()
        
    elif algorithm == "random_forest":
        diagram_random_forest()
    
    elif algorithm == "neural_networks":
        diagram_neural_networks()
        
    elif algorithm == "knn":
        diagram_knn()
    else:
        print("Wrong algorithm")
        exit(0)
       
    
    
if __name__ == "__main__":
    main_diagrams()






