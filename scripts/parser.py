"""
Goal of the script : Parsing the data

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub ?
"""

import re
import pandas as pd

# Define regular expressions for data extraction
timestamp_pattern = r"(\d+:\d+:\d+\.\d+)"
source_ip_pattern = r"IP (\S+) >"
destination_ip_pattern = r"> (\S+):"
query_details_pattern = r"\d+\+ (\S+)\? (\S+)\. (\(\d+\))"

def parse_data(data):
    """Parse and structure the DNS traffic data."""
    timestamps, source_ips, destination_ips, query_types, query_details = [], [], [], [], []

    lines = data.strip().split('\n')
    for line in lines:
        timestamp = re.search(timestamp_pattern, line).group(1)
        source_ip = re.search(source_ip_pattern, line).group(1)
        destination_ip = re.search(destination_ip_pattern, line).group(1)
        query_match = re.search(query_details_pattern, line)
        if query_match:
            query_type = query_match.group(1)
            query_detail = query_match.group(2)
        else:
            query_type = query_detail = None

        timestamps.append(timestamp)
        source_ips.append(source_ip)
        destination_ips.append(destination_ip)
        query_types.append(query_type)
        query_details.append(query_detail)

    return timestamps, source_ips, destination_ips, query_types, query_details

def preprocess_data(df):
    """Preprocess the structured data."""
    # Data Preprocessing (Cleaning, Encoding, etc.) can be done here.
    return df

def label_data(df, label):
    """Label the data as 'human' or 'bot'."""
    num_samples = len(df)
    labels = [label] * num_samples
    df['Label'] = labels
    return df

if __name__ == "__main__":
    # Read data from training files
    with open("../training_datasets/tcpdumps/bots_tcpdump.txt", "r") as file:
        bots_data = file.read()

    with open("../training_datasets/tcpdumps/webclients_tcpdump.txt", "r") as file:
        webclients_data = file.read()
    # Parse and structure the data from both files
    bots_timestamps, bots_source_ips, bots_destination_ips, bots_query_types, bots_query_details = parse_data(bots_data)
    webclients_timestamps, webclients_source_ips, webclients_destination_ips, webclients_query_types, webclients_query_details = parse_data(webclients_data)

    # Create DataFrames to store the structured data
    bots_data_dict = {
        'Timestamp': bots_timestamps,
        'Source IP': bots_source_ips,
        'Destination IP': bots_destination_ips,
        'Query Type': bots_query_types,
        'Query Details': bots_query_details
    }

    webclients_data_dict = {
        'Timestamp': webclients_timestamps,
        'Source IP': webclients_source_ips,
        'Destination IP': webclients_destination_ips,
        'Query Type': webclients_query_types,
        'Query Details': webclients_query_details
    }

    # Preprocess the data
    bots_df = pd.DataFrame(bots_data_dict)
    webclients_df = pd.DataFrame(webclients_data_dict)

    bots_df = preprocess_data(bots_df)
    webclients_df = preprocess_data(webclients_df)

    # Label the data
    bots_df = label_data(bots_df, label="bot")
    webclients_df = label_data(webclients_df, label="human")

    # Combine the data from both files into a single DataFrame
    combined_df = pd.concat([bots_df, webclients_df], ignore_index=True)

    # Display the structured and labeled data
    print(combined_df)




