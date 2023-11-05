"""
Goal of the script : Parsing the DNS trace datasets

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


import re
from datetime import timedelta

# Personal dependencies
import sys
sys.path.append("./features/")
import features_time as features_time
import features_numbers as features_numbers
import features_misc as features_misc

sys.path.append("./utils/")
import colors
import constants
import features


#########################################
##### \ BEGINNING OF RAW FEATURES / ##### 
"""
Taken example for the comments in the next functions from the DNS trace dataset : 
Request  : 13:22:44.546969 IP unamur021.55771 > one.one.one.one.domain: 18712+ A? kumparan.com. (30)
Response : 13:22:44.580851 IP one.one.one.one.domain > unamur021.55771: 18712 2/0/0 A 104.18.130.231, A 104.18.129.231 (62)
"""

def extract_timestamp(line):
    """
    Extract timestamp from a single line of the DNS trace dataset.
    Request  : 13:22:44.546969 
    Response : 13:22:44.580851
    """
    timestamp_match = re.search(r"(\d{2}:\d{2}:\d{2}\.\d{6})", line)
    return timestamp_match.group(1) if timestamp_match else None

# No need to extract protocol since it is always IP

def extract_hostname(line):
    """
    Extract hostname from a single line of the DNS trace dataset.
    Request  : unamur021 
    Response : one
    
    The 'one' is the response will be used later to determine if the line is a request or a response
    """
    hostname_match = re.search(r"IP (\w+)", line)
    return hostname_match.group(1) if hostname_match else None


# Request  : No need to extract the port since it is randomly generated
# Response : No need to extract the port since it is always 53 (.domain)

def extract_query_id(line):
    """
    Extract request ID from a single line of the DNS trace dataset.
    Request  : 18712(+)
    Response : 18712
    """
    id_match = re.search(r": (\d+)", line)
    return int(id_match.group(1)) if id_match else None


def extract_dns_query_type(line):
    """
    Extract DNS query type from a single line of the DNS trace dataset.
    Request  : A
    Response : A A
    """
    possible_query_types = ["A", "AAAA", "NXDomain", "CNAME", "ServFail"]
    pattern_to_find = r'\b(?:' + '|'.join(re.escape(word) for word in possible_query_types) + r')\b'
    query_type_match = re.findall(pattern_to_find, line)
    return query_type_match if query_type_match else None
        

def extract_domain_being_queried(line):
    """
    Extract domain from a single line of the DNS trace dataset.
    Request  : kumparan.com
    Response : None
    """
    domain_match = re.search(r"\? ([\w\.-]+)\.", line)
    return domain_match.group(1) if domain_match else None


def extract_length(line):
    """
    Extract length from a single line of the DNS trace dataset.
    Request : (30)
    Response : (62)
    """
    length_match = re.search(r"\((\d+)\)$", line)
    return int(length_match.group(1)) if length_match else None


def extract_DNS_response(line):
    """
    Extract DNS response from a single line of the DNS trace dataset.
    Request : None
    Response : 104.18.130.231, 104.18.129.231
    """
    
    is_response_var = is_response(line)
    if not(is_response_var):
        return None
    
    types = ["A", "AAAA", "NXDomain", "CNAME", "ServFail"]
    results = {}
    query_type = extract_dns_query_type(line)

    count_match = extract_counts(line)
    if not count_match:
        return None

    answers, _, _ = count_match
    if answers == 0: # will always be (0, 1, 0)        
        if query_type == None:
            results[constants.NOT_A_RESSOURCE_RECORD] = [constants.AUTHORITATIVE_SERVER_RESPONSE]
        elif query_type[0] == "NXDomain":
            results["NXDomain"] = [constants.NON_EXISTENT_DOMAIN_ERROR]
        elif query_type[0] == "ServFail":
            results["ServFail"] = [constants.SERVFAIL_ERROR]
        else:
            print("You should investigate for this RR type since it is not handled yet !")
            # exit(0)
        return results


    # Use the split line to extract domains for each query type based on the count of answers
    query_in_list_format = line.split()
    
    for t in types:
        list_of_domains = []
        for i in range(len(query_in_list_format)):
            if query_in_list_format[i] == t:
                domain = query_in_list_format[i + 1].rstrip(",?")
                list_of_domains.append(domain)
                answers -= 1
                if answers == 0:
                    break
        if list_of_domains:
            results[t] = list_of_domains

    return results
    


def extract_counts(line):
    """
    Extract counts from a single line of the DNS trace dataset.
    Request : None
    Response : (2, 0, 0)
    """
    count_match = re.search(r"(\d+)/(\d+)/(\d+)", line)
    return tuple(int(count) for count in count_match.groups()) if count_match else None


#####   \   END OF RAW FEATURES  /  ##### 
#########################################


def parse_dns_trace(line):
    """
    Parse a single line from the DNS trace dataset with additional features.
    
    Args:
        - line: the line to parse.
        
    Returns:
        - A dictionary containing the parsed data.
    """
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


def is_response(line):
    """
    Check if a line is a response.
    
    Args:
        - line: the line to check.
    
    Returns:
        - True if the line is a response, False otherwise.
    """
    return extract_hostname(line) == "one"

def parse_timestamp(ts):
    """
    Parse a timestamp from the DNS trace dataset.
    
    Args:
        - ts: the timestamp string.
        
    Returns:
        - A timedelta object representing the timestamp.
    """
    hours, minutes, seconds = ts.strip().split(':')
    seconds, microseconds = seconds.split('.')
    return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds), microseconds=int(microseconds))

def parsing_file(lines):
    """
    Pair DNS lines based on their IDs using the adjusted parser.
    
    Args:
        - lines: the lines of the DNS trace dataset.
    
    Returns:
        - paired_data: a dictionary containing the parsed data.
    """
    paired_data = {}
    
    for line in lines:
        parsed_line = parse_dns_trace(line)

        trace_id = parsed_line.get("query_id")
        if trace_id is None: # There is some TCP flags in the file, we need to remove it since that is not DNS queries
            continue

        # Initialize dictionary for the ID if not present
        if trace_id not in paired_data:
            paired_data[trace_id] = {"request": {}, "response": {}}  # Initialize dictionary for the ID
            
        elif paired_data[trace_id]["request"] != {} and paired_data[trace_id]["response"] != {}:
            timestamp_req = parse_timestamp(paired_data[trace_id]["request"]["timestamp"])
            timestamp_resp = parse_timestamp(paired_data[trace_id]["response"]["timestamp"])
            difference = abs(timestamp_resp - timestamp_req)
            if difference > timedelta(seconds=1):
                i = 1
                trace_id = f"{trace_id}_{i}"
                while trace_id in paired_data:
                    trace_id = trace_id.replace(f"_{i}", f"_{i+1}")
                    i += 1
                paired_data[trace_id] = {"request": {}, "response": {}}
                
        # Determine if the line is a request or response based on the domain (if "one" or not)       
        trace_type = "response" if is_response(line) else "request"

        paired_data[trace_id][trace_type] = parsed_line

    return paired_data

def parse_training_data(path_to_bots_tcpdump, path_to_webclients_tcpdump):
    """
    Parse the DNS training datasets.

    Args:
        - path_to_bots_tcpdump: the path to the tcpdump file containing the bots data.
        - path_to_webclients_tcpdump: the path to the tcpdump file containing the webclients data.

    Returns:
        - bots_data: a dictionary containing the parsed data for the bots.
        - webclients_data: a dictionary containing the parsed data for the webclients.
    """
    print(colors.Colors.GREEN + "####\nParsing the DNS line TRAINING datasets..." + colors.Colors.RESET)
    
    # Parse both datasets
    bots_data = {}
    with open(path_to_bots_tcpdump, 'r') as bot_file:
        bots_data = parsing_file(bot_file)
    
    webclients_data = []
    with open(path_to_webclients_tcpdump, 'r') as webclient_file:
        webclients_data = parsing_file(webclient_file)

    print(colors.Colors.GREEN + "Parsing TRAINING datasets completed!\n####" + colors.Colors.RESET)
    return bots_data, webclients_data


def parse_eval_data(path_to_eval_tcpdump):
    """
    Parse the DNS evaluation dataset.

    Args:
    - path_to_eval_tcpdump: the path to the evaluation tcpdump file.

    Returns:
    - eval_data: a dictionary containing the parsed data.
    """
    print(colors.Colors.GREEN + "####\nParsing the DNS line EVALUATION dataset..." + colors.Colors.RESET)
    
    # Parse both datasets
    eval_data = {}
    with open(path_to_eval_tcpdump, 'r') as eval_file:
        eval_data = parsing_file(eval_file)

    print(colors.Colors.GREEN + "Parsing EVALUATION dataset completed!\n####\n" + colors.Colors.RESET)
    return eval_data

if __name__ == "__main__":
    bots_data, webclients_data = parse_training_data("../../training_datasets/tcpdumps/bots_tcpdump.txt", "../../training_datasets/tcpdumps/webclients_tcpdump.txt")

    