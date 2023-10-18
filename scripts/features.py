"""
Goal of the script : Functions to convert the data to a dataframe and encode the features

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder


def convert_to_dataframe(bots_data, webclients_data):
    # Convert to DataFrame
    bots_df = pd.DataFrame(bots_data)
    bots_df['label'] = 'bot'

    webclients_df = pd.DataFrame(webclients_data)
    webclients_df['label'] = 'human'

    # Combine the two datasets
    combined_df = pd.concat([bots_df, webclients_df], ignore_index=True)

    # Convert categorical features to numerical
    combined_df['query_type'] = combined_df['query_type'].astype('category')
    combined_df['domain'] = combined_df['domain'].astype('category')
    combined_df['host'] = combined_df['host'].astype('category')
    combined_df['timestamp'] = combined_df['timestamp'].astype('category')
    combined_df['length'] = combined_df['length'].astype('int64')
    
    return combined_df


def encoding_features(combined_df):
    # Label encode categorical features
    label_encoder_query_type = LabelEncoder()
    combined_df['query_type_encoded'] = label_encoder_query_type.fit_transform(
        combined_df['query_type'].astype(str))

    label_encoder_domain = LabelEncoder()
    combined_df['domain_encoded'] = label_encoder_domain.fit_transform(
        combined_df['domain'])

    label_encoder_host = LabelEncoder()
    combined_df['host_encoded'] = label_encoder_host.fit_transform(
        combined_df['host'])

    label_encoder_timestamp = LabelEncoder()
    combined_df['timestamp_encoded'] = label_encoder_timestamp.fit_transform(
        combined_df['timestamp'])

    label_encoder_length = LabelEncoder()
    combined_df['length_encoded'] = label_encoder_length.fit_transform(
        combined_df['length'])

    return combined_df