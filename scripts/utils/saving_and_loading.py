"""
Goal of the script : Saving and loading the trained model for future use

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


import pickle

import utils.colors as colors


def load_saved_model(path_saved_model):
    """
    Load a saved model from a given path.

    Args:
        path_saved_model: The path to the saved model.

    Returns:
        The loaded model.
    """
    print(colors.Colors.YELLOW + f"####\nTrying to load the saved model..." + colors.Colors.RESET)
    
    with open(path_saved_model, 'rb') as saved_model:
        loaded_clf = pickle.load(saved_model)
        
    print(colors.Colors.YELLOW + f"Loaded the model successfully!\n####\n" + colors.Colors.RESET)
    return loaded_clf


def save_trained_model(clf, algorithm, output_path_saved_model):
    """
    Save a trained model to a binary file using pickle.

    Args:
        clf: A trained model object.
        algorithm: A string representing the name of the algorithm used to train the model.
        output_path_saved_model: A string representing the path where the trained model will be saved.
    """
    print(colors.Colors.YELLOW + f"####\nTrying to save the model..." + colors.Colors.RESET)
    with open(output_path_saved_model, "wb") as saved_model: # f"../../trained_models/{algorithm}/{constants.NAME_TRAINED_MODEL[algorithm]}"
        pickle.dump(clf, saved_model)
        
    print(colors.Colors.YELLOW + f"Successfully saved the model !\n####" + colors.Colors.RESET)