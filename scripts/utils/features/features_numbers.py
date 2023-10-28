"""
Goal of the script : All the features related to getting a discrete number

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


def get_number_of_dots_in_a_domain(aggregated_data):
    """
    This function is used to get the number of dots in the domains queried by each host.
    
    We removed one dot because in every request, the root domain is included.
    
    """
    number_of_dots_domains = {}
    for data in aggregated_data:
        host = data['host']
        if host in number_of_dots_domains:
            number_of_dots_domains[host].append(data['domain'].count("."))
        else:
            number_of_dots_domains[host] = [data['domain'].count(".")]
    
    # beautiful print
    for key, value in number_of_dots_domains.items():
        print(f"{key} : \n {value} \n \n")


    # TODO when we decided the model, we either need to choose one of the 2 options
    # 1. on averaged sur la moyenne du nombres de dots et on passe ça en paramètre pour l'host
    # 2. on donne complétement les données brutes PAR aggrégation de request/response

def get_number_of_requests_in_a_session(aggregated_data): 
    """ 
    Getting the number of requests in a session for each host
    
    """
    get_number_of_requests = {}
    for data in aggregated_data:
        host = data['host']
        if host in get_number_of_requests:
            get_number_of_requests[host] += 1
        else:
            get_number_of_requests[host] = 1
    
    print(get_number_of_requests)
    

def get_number_of_unique_domains(aggregated_data): # and we should also get the ratio of those domains
    """
    Pour chaque host, on regarde les domains qui query et on fait un set de ces domains et puis on fait un len de chaque host
    """

    number_of_unique_domains = {}
    for data in aggregated_data:
        host = data['host']
        if host in number_of_unique_domains:
            number_of_unique_domains[host].add(data['domain'])
        else:
            number_of_unique_domains[host] = {data['domain']}

    # beautiful print
    for key, value in number_of_unique_domains.items():
        print(f"{key} : \n {value} \n \n")

    number_of_unique_domains = {key: len(value) for key, value in number_of_unique_domains.items()}  
        
    print(number_of_unique_domains)