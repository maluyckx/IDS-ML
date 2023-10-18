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
    counts_match = re.search(r"(\d+)/(\d+)/(\d+)", line)
    return tuple(map(int, counts_match.groups())) if counts_match else None



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

