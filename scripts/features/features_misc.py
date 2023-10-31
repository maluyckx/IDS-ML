"""
Goal of the script : Miscellaneous features 



Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


from statistics import mean

def get_average_of_query_length(aggregated_data):
    """
    Getting the average of the query length for each host
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

    # print("Average of request length : ", average_of_request_length) 
    # print()
    # print("Average of response length : ", average_of_response_length)
    
    ## Bots
    # Requests : =~ 30
    # Response : =~ entre 60 et 70
    ## Webclients
    # Requests : =~ 40
    # Response : =~ pas vraiment de moyenne, c'est full variable


    return average_of_request_length, average_of_response_length


def get_type_of_requests_queried_by_hosts(aggregated_data):
    """
    Getting the type of requests queried by each host
    
    Bots : they only do "A" requests
    Webclients : they do "A" and "AAAA" requests
    """
    type_of_requests_queried_by_hosts = {}
    for data in aggregated_data:
        host = data['host']
        if host in type_of_requests_queried_by_hosts:
            type_of_requests_queried_by_hosts[host].update(set(data['request_type']))
        else:
            type_of_requests_queried_by_hosts[host] = set(data['request_type'])
    
    # # beautiful print
    # for key, value in type_of_requests_queried_by_hosts.items():
    #     print(f"{key} : \n {value} \n \n")

    return type_of_requests_queried_by_hosts


def get_type_of_responses_received_by_hosts(aggregated_data):   
    """
    Maybe the response type is also interesting ?? (response type received by each host)
    """
    type_of_responses_received_by_hosts = {}
    for data in aggregated_data:
        host = data['host']
        if host in type_of_responses_received_by_hosts:
            type_of_responses_received_by_hosts[host].update(set(data['responses'].keys()))
        else:
            type_of_responses_received_by_hosts[host] = set(data['responses'].keys())
    
    # beautiful print
    # for key, value in type_of_responses_received_by_hosts.items():
    #     print(f"{key} : \n {value} \n \n")

    return type_of_responses_received_by_hosts



def get_all_requests_and_responses_for_an_host(aggregated_data): # WILL NOT BE USED DIRECTLY AS A FEATURE
    """
    Getting all the aggregated data from the host
    
    unamur021 : 
            {
            {QUERY_ID: REQUEST AND RESPONSE AGGREGATED}, 
            {QUERY_ID: REQUEST AND RESPONSE AGGREGATED},
            }, 
    """
    
    requests_and_responses_per_host = {}
    for data in aggregated_data:
        host = data['host']
        if host in requests_and_responses_per_host:
            requests_and_responses_per_host[host][data['query_id']] = data
        else:
            requests_and_responses_per_host[host] = {data['query_id']: data}
    
    # # beautiful print
    # for key, value in requests_and_responses_per_host.items():
    #     print(f"{key} : \n {value} \n \n")
        
    return requests_and_responses_per_host
    