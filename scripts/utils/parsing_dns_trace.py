"""
Goal of the script : Parsing the DNS trace datasets

Authors : 
    - LUYCKX Marco 496283
    - BOUHNINE Ayoub 500048
"""


import re
from datetime import timedelta

import colors



##### \ BEGINNING OF RAW FEATURES / ##### 

def extract_timestamp(line):
    """Extract timestamp from a single line of the DNS trace dataset."""
    timestamp_match = re.search(r"(\d{2}:\d{2}:\d{2}\.\d{6})", line)
    return timestamp_match.group(1) if timestamp_match else None

def extract_hostname(line):
    """Extract hostname from a single line of the DNS trace dataset."""
    hostname_match = re.search(r"IP (\w+)", line)
    return hostname_match.group(1) if hostname_match else None

# def extract_dns_query_type(line):
#     """Extract DNS query type from a single line of the DNS trace dataset."""
#     query_type_match = re.search(r"\s(A|AAAA|NXDomain|CNAME|ServFail)(?=[\s\?])", line) # TODO: checker CNAME 
#     return query_type_match.group(1) if query_type_match else None





# def extract_dns_query_type(line):
#     """Extract DNS query type from a single line of the DNS trace dataset."""
#     query_type_match = re.search(r"\s(A|AAAA|NXDomain|CNAME|ServFail)(?=[\s\?])", line)

#     if query_type_match == None:
#         return None, None

#     query_type = query_type_match.group(1)

#     # Depending on the type of query, we will extract the domain differently
#     if query_type == "A" : 
#         query_type_match = re.search(r"\sA\??\s(\S+)", line)
#         list_of_domains = []
        
#         count_match = extract_counts(line)
#         if not(count_match == None):
#             answers = count_match[0]
#             authority = count_match[1]
#             additional = count_match[2]
            
#             if int(answers) == 0:
#                 print("No answer WTF")
#                 exit(0)
#             else : 
#                 query_in_list_format = line.split()
#                 for i in range(len(query_in_list_format)):
#                     if query_in_list_format[i] == "A" :
#                         list_of_domains.append(query_in_list_format[i+1])
        
    
#     elif query_type == "AAAA":
#         pass

#     elif query_type == "NXDomain":
#         pass

#     elif query_type == "CNAME":
#         pass
#     elif query_type == "ServFail":
#         pass
    
#     else :
#         print("Error : the query type is not A, AAAA, NXDomain, CNAME or ServFail")
#         exit(1)


def extract_dns_query_type(line):
    """Extract DNS query type from a single line of the DNS trace dataset."""
    # query_type_match = re.search(r"\s(A|AAAA|NXDomain|CNAME|ServFail)(?=[\s\?])", line) # TODO: checker CNAME 
    possible_query_types = ["A", "AAAA", "NXDomain", "CNAME", "ServFail"]
    pattern_to_find = r'\b(?:' + '|'.join(re.escape(word) for word in possible_query_types) + r')\b'
    query_type_match = re.findall(pattern_to_find, line) # TODO: checker CNAME 
    print(query_type_match)
    return query_type_match if query_type_match else None
    
    # """Extract all DNS query types and their associated domains from a single line of the DNS trace dataset."""
    # types = ["A", "AAAA", "NXDomain", "CNAME", "ServFail"]
    # results = {}

    # # Extract counts
    # count_match = extract_counts(line)
    # if not count_match:
    #     return None

    # answers, _, _ = count_match
    # if answers == 0: # will always be (0, 1, 0)
    #     #print("No answer for the query")
    #     print(line)
    #     return None

    # # Use the split line to extract domains for each query type based on the count of answers
    # query_in_list_format = line.split()
    
    # for t in types:
    #     list_of_domains = []
    #     for i in range(len(query_in_list_format)):
    #         if query_in_list_format[i] == t:
    #             domain = query_in_list_format[i + 1].rstrip(",?")
    #             list_of_domains.append(domain)
    #             answers -= 1
    #             if answers == 0:
    #                 break
    #     if list_of_domains:
    #         results[t] = list_of_domains
    # print(results)
    # return results



    #     domain_match = re.search(r"\s" + query_type + r"\??\s(\S+)", line)
    #     domain = domain_match.group(1).rstrip(",?") if domain_match else None
    #     print(f"Query type : {query_type} | Domain : {domain}")
    #     return query_type, domain
    # return None, None
    

    

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


##### \ END OF RAW FEATURES / ##### 

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
    
    # compteur = 0
    
    for line in lines:
        # if compteur > 200:
        #      exit(0)
        parsed_line = parse_dns_trace(line)

        # print(parsed_line.get("query_type"))
        # compteur += 1
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
    print(colors.Colors.GREEN + "####\nParsing the DNS line datasets..." + colors.Colors.RESET)
    
    # Parse both datasets
    bots_data = {}
    with open(path_to_bots_tcpdump, 'r') as bot_file:
        bots_data = parsing_file(bot_file)
    
    print("######SWITCH BOT FROM HUMAN######")
    webclients_data = []
    with open(path_to_webclients_tcpdump, 'r') as webclient_file:
        webclients_data = parsing_file(webclient_file)

    print(colors.Colors.GREEN + "Parsing completed!\n####\n" + colors.Colors.RESET)
    return bots_data, webclients_data


def parsing_cleaning_testing_data(list_of_test_datasets):
    # Y'a des flags de TCP dans le fichier de test, faut qu'on parse les données qui sont pas du DNS 
    # Example de eval 1 : 11:12:37.412776 IP one.one.one.one.domain > unamur036.39802: Flags [S.], seq 3634935584, ack 3866216491, win 65535, options [mss 1452,nop,nop,sackOK,nop,wscale 10], length 0
    for i in list_of_test_datasets:
        pass



def get_timing_for_a_session():
    pass


def  get_number_of_unique_domains(): # and we should also get the ratio of those domains
    pass


def frequency_of_repeated_requests_in_a_short_time_frame():
    pass



if __name__ == "__main__":
    parse_training_data("../../training_datasets/tcpdumps/bots_tcpdump.txt", "../../training_datasets/tcpdumps/webclients_tcpdump.txt")



    # parsing_cleaning_testing_data(["../../testing_datasets/tcpdumps/eval1_tcpdump.txt", "../../testing_datasets/tcpdumps/eval2_tcpdump.txt"])
    