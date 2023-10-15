from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

import pandas as pd
import re


def parse_dns_trace(line):
    """Parse a single line from the DNS trace dataset."""
    # Extract timestamp
    timestamp_match = re.search(r"(\d{2}:\d{2}:\d{2}\.\d{6})", line)
    timestamp = timestamp_match.group(1) if timestamp_match else None

    # Extract host name
    host_match = re.search(r"IP (\w+)", line)
    host = host_match.group(1) if host_match else None

    # Extract DNS query type (e.g., A, AAAA)
    query_type_match = re.search(r"\s(A|AAAA)\?", line)
    query_type = query_type_match.group(1) if query_type_match else None

    # Extract domain being queried
    domain_match = re.search(r"\? ([\w\.-]+)\.", line)
    domain = domain_match.group(1) if domain_match else None

    return {"timestamp": timestamp, "host": host, "query_type": query_type, "domain": domain}

# Parse both datasets
bots_data = []
with open("./bots_tcpdump.txt", 'r') as file:
    for line in file:
        parsed_data = parse_dns_trace(line)
        if parsed_data["domain"]:  # Only consider lines with domain information
            bots_data.append(parsed_data)

webclients_data = []
with open("./webclients_tcpdump.txt", 'r') as file:
    for line in file:
        parsed_data = parse_dns_trace(line)
        if parsed_data["domain"]:  # Only consider lines with domain information
            webclients_data.append(parsed_data)

# Convert to DataFrame
bots_df = pd.DataFrame(bots_data)
bots_df['label'] = 'bot'

webclients_df = pd.DataFrame(webclients_data)
webclients_df['label'] = 'human'

# Combine the two datasets
combined_df = pd.concat([bots_df, webclients_df], ignore_index=True)

# Label encode categorical features
le_query_type = LabelEncoder()
combined_df['query_type_encoded'] = le_query_type.fit_transform(combined_df['query_type'].astype(str))

le_domain = LabelEncoder()
combined_df['domain_encoded'] = le_domain.fit_transform(combined_df['domain'])

# Split the data into training and testing sets
X = combined_df[['query_type_encoded', 'domain_encoded']]
y = combined_df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the decision tree classifier
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# Test the classifier's accuracy on the test set
accuracy = clf.score(X_test, y_test)
print(accuracy)
