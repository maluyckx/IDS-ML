"""
Goal of the script : Parsing the DNS trace datasets

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""

import re

from datetime import timedelta

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

def extract_query_id(line):
    """Extract request ID from a single line of the DNS trace dataset."""
    id_match = re.search(r": (\d+)", line)
    return int(id_match.group(1)) if id_match else None

def extract_counts(line):
    """Extract counts from a single line of the DNS trace dataset."""
    count_match = re.search(r"(\d+)/(\d+)/(\d+)", line)
    return tuple(int(count) for count in count_match.groups()) if count_match else None

def parse_dns_trace(line):
    """Parse a single line from the DNS trace dataset with additional features."""
    return {
        "timestamp": extract_timestamp(line),
        # Protocol is not needed in our analysis since for all lines it is 'IP'
        "host": extract_hostname(line),
        # Destination address is not needed in our analysis since for all lines it is 'one.one.one.one.domain'
        "query_id": extract_query_id(line),
        "query_type": extract_dns_query_type(line),
        "domain": extract_domain_being_queried(line), # only for the request
        "length": extract_length(line),
        "responses": extract_DNS_response(line), # only for the response
        "counts": extract_counts(line), # only for the response
    }

def parse_timestamp(ts):
    hours, minutes, seconds = ts.strip().split(':')
    seconds, microseconds = seconds.split('.')
    return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), microseconds=int(microseconds))


def parsing_file(lines):
    """Pair DNS lines based on their IDs using the adjusted parser."""
    paired_data = {}
    
    for line in lines:
        parsed_line = parse_dns_trace(line)
        
        # Check if ID is present and valid
        trace_id = parsed_line.get("query_id")
        if trace_id is None:
            continue

        # Initialize dictionary for the ID if not present
        if trace_id not in paired_data:
            paired_data[trace_id] = {"request": {}, "response": {}}  # Initialize dictionary for the ID
        elif paired_data[trace_id]["request"] != {} and paired_data[trace_id]["response"] != {}:
            timestamp_req = parse_timestamp(paired_data[trace_id]["request"]["timestamp"])
            timestamp_resp = parse_timestamp(paired_data[trace_id]["response"]["timestamp"])
            difference = abs(timestamp_resp - timestamp_req)
            if difference <= timedelta(seconds=1):
                pass
            else:
                i = 1
                trace_id = f"{trace_id}_{i}"
                while trace_id in paired_data:
                    trace_id = trace_id.replace(f"_{i}", f"_{i+1}")
                    i += 1
                paired_data[trace_id] = {"request": {}, "response": {}}
                
        # Determine if the line is a request or response based on the domain (if "one" or not)
        if parsed_line["host"] == "one":
            trace_type = "response"
        else:
            trace_type = "request"

        paired_data[trace_id][trace_type] = parsed_line

    return paired_data

def parse_training_data(path_to_bots_tcpdump, path_to_webclients_tcpdump):
    print("####\nParsing the DNS line datasets...")
    # Parse both datasets
    bots_data = {}
    with open(path_to_bots_tcpdump, 'r') as bot_file:
        bots_data = parsing_file(bot_file)
    
    webclients_data = []
    with open(path_to_webclients_tcpdump, 'r') as webclient_file:
        webclients_data = parsing_file(webclient_file)

    print("Parsing completed!\n####\n")
    return bots_data, webclients_data
