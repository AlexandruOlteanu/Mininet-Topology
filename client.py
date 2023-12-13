#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import sys
import argparse
import requests_cache
import threading
from concurrent.futures import ThreadPoolExecutor

# ANSI color escape codes
ANSI_RED     = '\033[31m'
ANSI_GREEN   = '\033[32m'
ANSI_YELLOW  = '\033[33m'
ANSI_BLUE    = '\033[34m'
ANSI_MAGENTA = '\033[35m'
ANSI_CLR     = '\033[0m'
ANSI_BOLD    = '\033[1m'
ANSI_UNBOLD  = '\033[2m'

# Initialize cache (for example, cache responses for 2 hours)
requests_cache.install_cache('http_cache', backend='sqlite', expire_after=7200, fast_save=True)


# Thread-safe logging buffer
log_buffer = []
log_buffer_lock = threading.Lock()

################################################################################
############################### CLIENT BACKENDS ################################
################################################################################

# http_get - Updated with timeout and exception handling
def http_get(url: str):
    ret = []
    try:
        while True:
            req = requests.get(url, allow_redirects=False, timeout=15)  # 15-second timeout
            ret.append((url, req.status_code, req.elapsed.microseconds))
            if req.is_redirect and req.next.url is not None:
                url = req.next.url
            else:
                break
    except requests.RequestException as e:
        print(f"Request error: {e}")
    return ret

################################################################################
########################### RESPONSE PRETTY PRINTERS ###########################
################################################################################

# disp_http - Updated with efficient logging
def disp_http(resp_list):
    log_entries = []
    for resp in resp_list:
        # Prepare log entry
        entry = ""
        if resp[1] == "ERROR":
            entry += f"{ANSI_RED}ERROR: {resp[2]} for URL {resp[0]}{ANSI_CLR}\n"
        else:
            # select color for status message depending on class
            if 100 <= resp[1] < 200:    # Informational Response
                sm_color = ANSI_BLUE
            elif 200 <= resp[1] < 300:  # Successful Response
                sm_color = ANSI_GREEN
            elif 300 <= resp[1] < 400:  # Redirection Response
                sm_color = ANSI_YELLOW
            elif 400 <= resp[1]:        # Error Response
                sm_color = ANSI_RED
            else:
                sm_color = ANSI_MAGENTA # Invalid code
            entry += f'{ANSI_BOLD}URL :{ANSI_UNBOLD} {resp[0]}{ANSI_CLR}\n'
            entry += f'{ANSI_BOLD}CODE:{ANSI_UNBOLD} {sm_color}{resp[1]}{ANSI_CLR}\n'
            entry += f'{ANSI_BOLD}TIME:{ANSI_UNBOLD} {resp[2]} [microsecs]{ANSI_CLR}\n\n'
        
        log_entries.append(entry)

    with log_buffer_lock:
        log_buffer.extend(log_entries)

# Write log buffer to file
def write_log():
    with open('client_log.txt', 'a') as logfile:
        with log_buffer_lock:
            for entry in log_buffer:
                print(entry, file=logfile, end='')


################################################################################
############################## SCRIPT ENTRY POINT ##############################
################################################################################

def process_url(proto, url):
    if proto == 'http' and not url.startswith('http://'):
        url = 'http://' + url
    elif proto == 'https' and not url.startswith('https://'):
        url = 'https://' + url
    ans = http_get(url)
    disp_http(ans)


def main():
    # parse CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('URLs', nargs='+', help='resource links to access')
    parser.add_argument('-p', '--proto', help='application protocol', default='http', choices=['http', 'https'])
    args = parser.parse_args()

    # Use ThreadPoolExecutor to parallelize the URL processing

    with ThreadPoolExecutor(max_workers=10) as executor:
         # Submit all URLs for processing
        futures = [executor.submit(process_url, args.proto, url) for url in args.URLs]

         # Wait for all futures to complete (optional)
        for future in futures:
             # You can add error handling or logging here if needed
            future.result()

    write_log()

if __name__ == '__main__':
    main()
