"""
Goal of the script : Saving and loading the trained model for future use

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


import pickle

import utils.constants as constants
import utils.colors as colors


def load_saved_model(algorithm):
    print(colors.Colors.YELLOW + f"Trying to load the saved model...\n####\n" + colors.Colors.RESET)
    
    with open(f"../../trained_models/{algorithm}/{constants.NAME_TRAINED_MODEL[algorithm]}", 'rb') as saved_model:
        loaded_clf = pickle.load(saved_model)
        
    print(colors.Colors.YELLOW + f"Load the model successfully!\n####\n" + colors.Colors.RESET)
    return loaded_clf


def save_trained_model(clf, algorithm, output_path_saved_model):
    print(colors.Colors.YELLOW + f"Trying to save the model...\n####\n" + colors.Colors.RESET)
    with open(output_path_saved_model, "wb") as saved_model: # f"../../trained_models/{algorithm}/{constants.NAME_TRAINED_MODEL[algorithm]}"
        pickle.dump(clf, saved_model)
        
    print(colors.Colors.YELLOW + f"Saving the model successfully !\n####\n" + colors.Colors.RESET)