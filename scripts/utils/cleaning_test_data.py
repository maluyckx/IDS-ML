"""
Goal of the script : Cleaning the test data

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""




def cleaning_test_datasets(list_of_test_datasets):
    # Y'a des flags de TCP dans le fichier de test, faut qu'on parse les données qui sont pas du DNS 
    # Example de eval 1 : 11:12:37.412776 IP one.one.one.one.domain > unamur036.39802: Flags [S.], seq 3634935584, ack 3866216491, win 65535, options [mss 1452,nop,nop,sackOK,nop,wscale 10], length 0
    for i in list_of_test_datasets:
        pass




if __name__ == "__main__":
    
    # mettre les deux datasets ici
    
    cleaning_test_datasets()