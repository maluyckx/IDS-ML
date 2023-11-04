"""
Goal of the script : Create miscellaneous features

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


from statistics import mean

def get_average_of_query_length(aggregated_data):
    """
    Getting the average of the query length for each host.
    
    Args:
        - aggregated_data: a list of dictionaries containing the aggregated data.
        
    Returns:
        - average_of_query_length: a dictionary containing the average of the query length for each host.
        
    For the report : 
        ## Bots
        Requests : =~ 30
        Response : =~ between 60 et 70
        ## Webclients
        Requests : =~ 40
        Response : =~ not really an average, varies a lot
    """
    query_length_by_host = {}
    for data in aggregated_data:
        host = data['host']
        if host in query_length_by_host:
            query_length_by_host[host].append((data['length_request'], data['length_response']))
        else:
            query_length_by_host[host] = [(data['length_request'], data['length_response'])]

    average_of_request_length = {key: mean([int(x[0]) for x in value]) for key, value in query_length_by_host.items()}
    average_of_response_length = {key: mean([int(x[1]) for x in value]) for key, value in query_length_by_host.items()}

    return average_of_request_length, average_of_response_length


def get_type_of_requests_queried_by_hosts(aggregated_data):
    """
    This function takes in a list of aggregated data and returns a dictionary where the keys are the hosts and the values are the set of request types queried by the respective hosts.

    Args:
        - aggregated_data: a list of dictionaries containing the aggregated data.

    Returns:
        - type_of_requests_queried_by_hosts: a dictionary where the keys are the hosts and the values are the set of request types queried by the respective hosts.
    
    Observation for the training datasets : 
        - Bots : they only do "A" requests
        - Webclients : they do "A" and "AAAA" requests
    """
    type_of_requests_queried_by_hosts = {}
    for data in aggregated_data:
        host = data['host']
        if host in type_of_requests_queried_by_hosts:
            type_of_requests_queried_by_hosts[host].update(set(data['request_type']))
        else:
            type_of_requests_queried_by_hosts[host] = set(data['request_type'])
    
    return type_of_requests_queried_by_hosts


def get_type_of_responses_received_by_hosts(aggregated_data):   
    """
    Getting the type of responses received by each host.
    
    Args:
        - aggregated_data: a list of dictionaries containing the aggregated data.
        
    Returns:
        - type_of_responses_received_by_hosts: a dictionary where the keys are the hosts and the values are the set of response types received by the respective hosts.
    """
    type_of_responses_received_by_hosts = {}
    for data in aggregated_data:
        host = data['host']
        if host in type_of_responses_received_by_hosts:
            type_of_responses_received_by_hosts[host].update(set(data['responses'].keys()))
        else:
            type_of_responses_received_by_hosts[host] = set(data['responses'].keys())
    
    return type_of_responses_received_by_hosts



def get_all_requests_and_responses_for_an_host(aggregated_data): # WILL NOT BE USED DIRECTLY AS A FEATURE
    """
    Getting all the requests and responses for each host.
    
    Args:
        - aggregated_data: a list of dictionaries containing the aggregated data.
        
    Returns:
        - requests_and_responses_per_host: a dictionary where the keys are the hosts and the values are the set of requests and responses for the respective hosts.
    """
    
    requests_and_responses_per_host = {}
    for data in aggregated_data:
        host = data['host']
        if host in requests_and_responses_per_host:
            requests_and_responses_per_host[host][data['query_id']] = data
        else:
            requests_and_responses_per_host[host] = {data['query_id']: data}
        
    return requests_and_responses_per_host
    