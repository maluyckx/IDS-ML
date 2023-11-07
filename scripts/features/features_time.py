"""
Goal of the script : All the features related to time

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

# Common dependencies
from statistics import mean
import datetime

# Personal dependencies
import sys
sys.path.append("../")
import utils.parsing_dns_trace as parser

# def get_average_of_timing_for_a_session(list_of_timing_for_a_session): # NOT A FEATURE, JUST FOR THE REPORT
#     list_of_average_of_timing_for_a_session = []
#     for key, value in list_of_timing_for_a_session.items():
#         difference = value[1] - value[0]
#         difference_in_seconds = difference.total_seconds()

#         #print(f"Average of timing for {key} : {difference_in_seconds}")
#         list_of_average_of_timing_for_a_session.append(difference_in_seconds)

#     print(mean(list_of_average_of_timing_for_a_session))


def get_timing_of_all_queries(aggregated_data):
    """
    Creating a dictionary containing all the timestamps of all requests and responses for each host.

    Args:
        - aggregated_data: list of dictionaries containing the aggregated data.

    Returns:
        - timing_of_all_queries: dictionary containing all the timestamps of all requests and responsess for each host.
    """

    timing_of_all_queries = {}

    for data in aggregated_data:
        host = data['host']
        timestamp_req = parser.parse_timestamp(data['timestamp_req'])
        # ATTENTION : whenever the response is not present, we discard the request => IT IS AN ADDITIONAL ASSUMPTION THAT WE MAKE, it can impact the model if the traffic is composed of a lot of requests without responses (and thus the model might behave differently)
        if data['timestamp_resp'] == '0':
            continue
        timestamp_resp = parser.parse_timestamp(data['timestamp_resp'])

        if host in timing_of_all_queries:
            timing_of_all_queries[host].append((timestamp_req, timestamp_resp))
        else:
            timing_of_all_queries[host] = [(timestamp_req, timestamp_resp)]

    # We need to sort the timestamps to be sure that the first element is the oldest and the last element is the newest
    timing_of_all_queries = {key: sorted(
        value) for key, value in timing_of_all_queries.items()}

    return timing_of_all_queries


def get_timing_for_a_session(aggregated_data):
    """
    Regroup all the requests and responses for a session and get the timing between the first request and the last response

    Args:
        - aggregated_data: dictionary containing the aggregated data for each session.

    Returns:
        - list_of_timing_for_a_session: dictionary containing the timing for each session.
    """
    timing_for_a_session = get_timing_of_all_queries(aggregated_data)

    list_of_timing_for_a_session = {}
    # key = host and value = list of timestamps (beginning with request and ending with response)
    for key, value in timing_for_a_session.items():
        # value[0][0] : first timestamp_request of the fist timestamp_tuple and value[-1][1] : last timestamp_response of the last timestamp_tuple
        list_of_timing_for_a_session[key] = (
            abs(value[-1][1] - value[0][0])).total_seconds()

    # print(mean(list_of_timing_for_a_session.values())) # Not a feature, just for the report

    return list_of_timing_for_a_session


def get_average_time_between_requests(aggregated_data):
    """
    Getting the average time between each request for each host. We are taking the difference between the timestamps of each request and response and then we are taking the mean of all the differences for each host.
    It kind of answers the question : "After how much time does a host make a new request ?"

    Args:
        - aggregated_data: list of dictionaries containing the aggregated data.

    Returns:
        - average_time_between_requests: dictionary containing the average time between each request for each host.
    """
    timing_for_a_session = get_timing_of_all_queries(aggregated_data)

    # for each adjacent timestamp, compute the difference between them
    average_time_between_requests = {}
    for key, value in timing_for_a_session.items():
        average_time_between_requests[key] = []
        for i in range(len(value)-1):
            difference = value[i+1][0] - value[i][0]
            difference_in_seconds = difference.total_seconds()
            average_time_between_requests[key].append(difference_in_seconds)

    # Calculate the mean of the list of differences for each host
    for key, value in average_time_between_requests.items():
        average_time_between_requests[key] = mean(value)

    return average_time_between_requests


def frequency_of_repeated_requests_in_a_short_time_frame(aggregated_data):
    """
    Getting the frequency of repeated requests for the same domain in a short time frame for each host.

    Args:
        - aggregated_data: list of dictionaries containing the aggregated data.

    Returns:
        - frequency_of_repeated_requests_in_a_short_time_frame: dictionary containing the frequency of repeated requests for the same domain in a short time frame for each host.
    """
    list_of_time_frames = [datetime.timedelta(seconds=10)]  # in seconds
    frequency_of_repeated_requests_in_a_short_time_frame = {}
    for data in aggregated_data:
        host = data['host']
        if host in frequency_of_repeated_requests_in_a_short_time_frame:
            if data['domain'] in frequency_of_repeated_requests_in_a_short_time_frame[host]:
                for time_frame in list_of_time_frames:
                    timestamp_next_request = parser.parse_timestamp(
                        data['timestamp_req'])
                    timestamp_latest_request = parser.parse_timestamp(
                        frequency_of_repeated_requests_in_a_short_time_frame[host][data['domain']][-1][-1])
                    if timestamp_next_request - timestamp_latest_request <= time_frame:
                        frequency_of_repeated_requests_in_a_short_time_frame[host][data['domain']][-1].append(
                            data['timestamp_req'])
                    else:
                        # check if there is already two lists inside, if it is the case, take the longest list and remove the other one
                        # if there is only one list, just append the new list
                        # in any case we append the new list
                        if len(frequency_of_repeated_requests_in_a_short_time_frame[host][data['domain']]) == 2:
                            if len(frequency_of_repeated_requests_in_a_short_time_frame[host][data['domain']][0]) > len(frequency_of_repeated_requests_in_a_short_time_frame[host][data['domain']][1]):
                                frequency_of_repeated_requests_in_a_short_time_frame[host][data['domain']].pop(
                                )
                            else:
                                frequency_of_repeated_requests_in_a_short_time_frame[host][data['domain']].pop(
                                    0)
                        frequency_of_repeated_requests_in_a_short_time_frame[host][data['domain']].append([
                                                                                                          data['timestamp_req']])
            else:
                frequency_of_repeated_requests_in_a_short_time_frame[host][data['domain']] = [
                    [data['timestamp_req']]]
        else:
            frequency_of_repeated_requests_in_a_short_time_frame[host] = {
                data['domain']: [[data['timestamp_req']]]}

    # taking the length of the longest timestamp list for each domain of each host (key)
    # for each host, we take the mean of the longest timestamp list for each domain
    for key, value in frequency_of_repeated_requests_in_a_short_time_frame.items():
        for domain in value:
            if len(value[domain]) == 1:
                value[domain] = 0
            else:
                if len(value[domain][0]) > len(value[domain][1]):
                    value[domain] = len(value[domain][0])
                else:
                    value[domain] = len(value[domain][1])

        frequency_of_repeated_requests_in_a_short_time_frame[key] = mean(
            value.values())

    return frequency_of_repeated_requests_in_a_short_time_frame
