"""
Goal of the script : All the features related to getting a discrete number

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

from statistics import mean 


def get_average_number_of_dots_in_a_domain(aggregated_data):
    """
    Calculates the average number of dots in a domain for each host in the aggregated data.

    Args:
        - aggregated_data: a list of dictionaries containing the aggregated data.

    Returns:
        - number_of_dots_domains: a dictionary where the keys are the hosts and the values are the average number of dots in a domain for that host.
    """
    number_of_dots_domains = {}
    for data in aggregated_data:
        host = data['host']
        if host in number_of_dots_domains:
            number_of_dots_domains[host].append(data['domain'].count("."))
        else:
            number_of_dots_domains[host] = [data['domain'].count(".")]
    
    for key, value in number_of_dots_domains.items():
        number_of_dots_domains[key] = mean(value)

    return number_of_dots_domains

def get_number_of_requests_in_a_session(aggregated_data): 
    """ 
    Returns a dictionary containing the number of requests made in a session by each host in the aggregated data.

    Args:
        - aggregated_data: a list of dictionaries containing the aggregated data.
        
    Returns:
        - number_of_requests_in_a_session: a dictionary containing the number of requests made in a session by each host in the aggregated data.
    """
    get_number_of_requests = {}
    for data in aggregated_data:
        host = data['host']
        if host in get_number_of_requests:
            get_number_of_requests[host] += 1
        else:
            get_number_of_requests[host] = 1
    
    # print(mean(get_number_of_requests.values()))

    return get_number_of_requests
    

def get_number_of_unique_domains(aggregated_data): 
    """
    Getting the number of unique domains queried by each host. For each host, we look at the domains that they query and we make a set of these domains and then we take the length of each host.
    
    Args:
        - aggregated_data: a list of dictionaries containing the aggregated data.
        
    Returns:
        - number_of_unique_domains: a dictionary containing the number of unique domains queried by each host.
    """

    number_of_unique_domains = {}
    for data in aggregated_data:
        host = data['host']
        if host in number_of_unique_domains:
            number_of_unique_domains[host].add(data['domain'])
        else:
            number_of_unique_domains[host] = {data['domain']}

    number_of_unique_domains = {key: len(value) for key, value in number_of_unique_domains.items()}  
    
    return number_of_unique_domains
    
    
def get_average_counts(aggregated_data):
    """
    Getting the average of counts for each host.
    
    Args:
        - aggregated_data: a list of dictionaries containing the aggregated data.
        
    Returns:
        - average_counts: a dictionary containing the average of counts for each host.
    """
    average_counts = {}
    for data in aggregated_data:
        host = data['host']
        if host in average_counts:
            average_counts[host].append(data['counts'])
        else:
            average_counts[host] = [data['counts']]      
        
    average_counts = {key: (sum([x[0] for x in value])/len(value)) for key, value in average_counts.items()}
    
    return average_counts