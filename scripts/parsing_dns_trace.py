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
    query_type_match = re.search(r"\s(A|AAAA)(?=[\s\?])", line)
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
    return re.findall(r"(A|AAAA) (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)

def parse_dns_trace(line):
    """Parse a single line from the DNS trace dataset with additional features."""

    timestamp = extract_timestamp(line)
    host = extract_hostname(line)
    query_type = extract_dns_query_type(line)
    domain = extract_domain_being_queried(line)
    length = extract_length(line)
    responses = extract_DNS_response(line)

    return {
        "timestamp": timestamp,
        "host": host,
        "query_type": query_type,
        "domain": domain,
        "length": length,
        "responses": responses
    }


