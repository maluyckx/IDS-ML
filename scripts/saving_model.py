"""
Goal of the script : Using a decision tree classifier to detect bots in a network traffic trace 

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


import pickle

import utils.constants as constants



def load_saved_model(algorithm):
    with open(f"../../trained_models/{algorithm}/{constants.NAME_TRAINED_MODEL[algorithm]}", 'rb') as saved_model:
        loaded_clf = pickle.load(saved_model)
    return loaded_clf


def save_trained_model(clf, algorithm):
    with open(f"../../trained_models/{algorithm}/{constants.NAME_TRAINED_MODEL[algorithm]}", "wb") as saved_model:
        pickle.dump(clf, saved_model)