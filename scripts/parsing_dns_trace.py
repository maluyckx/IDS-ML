"""
Goal of the script : Parsing the DNS trace datasets

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

import re


def extract_timestamp(line):
    """Extract timestamp from a single line of the DNS trace dataset."""
    timestamp_match = re.search(r"(\d{2}:\d{2}:\d{2}\.\d{6})", line)
    return timestamp_match.group(1) if timestamp_match else None

def extract_hostname(line):
    """Extract hostname from a single line of the DNS trace dataset."""
    hostname_match = re.search(r"IP (\w+)", line)
    return hostname_match.group(1) if hostname_match else None

def extract_dns_query_type(line):
    """Extract DNS query type from a single line of the DNS trace dataset."""
    query_type_match = re.search(r"\s(A|AAAA|NXDomain|CNAME)(?=[\s\?])", line) # TODO: checker CNAME
    return query_type_match.group(1) if query_type_match else None

def extract_domain_being_queried(line):
    """Extract domain from a single line of the DNS trace dataset."""
    domain_match = re.search(r"\? ([\w\.-]+)\.", line)
    return domain_match.group(1) if domain_match else None

def extract_length(line):
    """Extract length from a single line of the DNS trace dataset."""
    length_match = re.search(r"\((\d+)\)$", line)
    return int(length_match.group(1)) if length_match else None

def extract_DNS_response(line):
    """Extract DNS response from a single line of the DNS trace dataset."""
    return tuple(re.findall(r"(A|AAAA) (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line))

def extract_request_id(line):
    """Extract request ID from a single line of the DNS trace dataset."""
    id_match = re.search(r": (\d+)", line)
    return int(id_match.group(1)) if id_match else None

def extract_counts(line):
    """Extract counts from a single line of the DNS trace dataset."""
    count_match = re.search(r"(\d+)/(\d+)/(\d+)", line)
    return tuple(int(count) for count in count_match.groups()) if count_match else None

def parse_dns_trace(line):
    """Parse a single line from the DNS trace dataset with additional features."""

    timestamp = extract_timestamp(line)
    host = extract_hostname(line)
    query_type = extract_dns_query_type(line)
    domain = extract_domain_being_queried(line)
    length = extract_length(line)
    responses = extract_DNS_response(line)
    counts = extract_counts(line)
    request_id = extract_request_id(line)

    return {
        "timestamp": timestamp,
        "host": host,
        "query_type": query_type,
        "domain": domain,
        "length": length,
        "responses": responses,
        "counts": counts,
        "request_id": request_id
    }

def parsing_file(traces):
    """Pair DNS traces based on their IDs using the adjusted parser."""
    paired_data = {}
    
    for trace in traces:
        parsed_trace = parse_dns_trace(trace)
        
        # Check if ID is present and valid
        trace_id = parsed_trace.get("request_id")
        if trace_id is None:
            continue

        # Initialize dictionary for the ID if not present
        if trace_id not in paired_data:
            paired_data[trace_id] = {"request": {}, "response": {}}  # Initialize dictionary for the ID

        # Determine if the trace is a request or response based on the domain (if "one" or not)
        if parsed_trace["host"] == "one":
            trace_type = "response"
        else:
            trace_type = "request"

        paired_data[trace_id][trace_type] = parsed_trace

        # if no request at the end, delete the ID
        if trace_type == 'request' and paired_data[trace_id]['response'] == {}:
            del paired_data[trace_id]

    return paired_data

def parse_training_data(path_to_bots_tcpdump, path_to_webclients_tcpdump):
    print("####\nParsing the DNS trace datasets...")
    # Parse both datasets
    bots_data = {}
    with open(path_to_bots_tcpdump, 'r') as file:
        bots_data = parsing_file(file)
    
    webclients_data = []
    with open(path_to_webclients_tcpdump, 'r') as file:
        webclients_data = parsing_file(file)

    print("Parsing completed!\n####\n")
    return bots_data, webclients_data
