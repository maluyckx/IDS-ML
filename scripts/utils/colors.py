"""
Colors class to print colored text in the terminal.

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


class Colors:
    RESET = "\033[0m"

    # Parsing
    GREEN = "\033[92m"
    # Training
    CYAN = "\033[96m"
    # Evaluation
    RED = "\033[91m"
    # Saving and loading the model
    YELLOW = "\033[93m"
    # Classification and accuracy
    PURPLE = "\033[95m"

    # Rates
    # Detection rate
    LIGHTCYAN = "\033[94m"
    # False alarm rate
    LIGHTRED = "\033[91m"
    # False negative rate
    LIGHTPURPLE = "\033[95m"
    # True negative rate
    LIGHTYELLOW = "\033[93m"

    # Human+bot
    GREY = "\033[90m"
