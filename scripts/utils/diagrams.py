"""
Goal of the script : Using a decision tree classifier to detect bots in a network traffic trace 

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

def diagram_decision_tree(clf):
    pass

def diagram_logistic_regression(clf):
    pass

def diagram_knn(clf, x_train, y_train):
    # Because we have more features than 2, we need to reduce the dimensionality of our data to be able to visualize it
    tsne = TSNE(n_components=2, random_state=0)
    print("la")
    print("ca met 15 ans ici, je sais pas pourquoi")
    X_tsne = tsne.fit_transform(x_train)
    print("ici")
    clf.fit(x_train, y_train) # we need to train our model with the original space, the high-dimensional one, and not the data given by t-SNE because this method just helps us to visualize data by reducing it, it is not a preprocessing step. If we train with these data using t-SNE, our model will be biased
    print("ici")


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





def main_diagrams():
    # Decision Tree
    # diagram_decision_tree()
    
    # Logistic Regression
    # diagram_logistic_regression()
    
    # KNN
    diagram_knn()
    
    # Random Forest
    # diagram_random_forest()
    
    # Neural Networks
    # diagram_neural_networks()
    
    
    
if __name__ == "__main__":
    main_diagrams()






