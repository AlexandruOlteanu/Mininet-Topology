#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import argparse
import requests_cache
import threading
from concurrent.futures import ThreadPoolExecutor

BATCH_CHUNK_SIZE = 15

# ANSI color escape codes
ANSI_RED     = '\033[31m'
ANSI_GREEN   = '\033[32m'
ANSI_YELLOW  = '\033[33m'
ANSI_BLUE    = '\033[34m'
ANSI_MAGENTA = '\033[35m'
ANSI_CLR     = '\033[0m'
ANSI_BOLD    = '\033[1m'
ANSI_UNBOLD  = '\033[2m'

requests_cache.install_cache('http_cache', backend='sqlite', expire_after=3600, fast_save=True)

log_buffer = []
log_buffer_lock = threading.Lock()

################################################################################
############################### CLIENT BACKENDS ################################
################################################################################

# Persistent HTTP session for batch requests
session = requests.Session()

def http_get_batch(urls: list):
    ret = []
    for url in urls:
        try:
            req = session.get(url, allow_redirects=False, timeout=15)
            ret.append((url, req.status_code, req.elapsed.microseconds))
            if req.is_redirect and req.next.url is not None:
                url = req.next.url
        except requests.RequestException as e:
            print(f"Request error: {e}")
    return ret

def process_url_batch(proto, urls):
    # Add protocol if not present
    processed_urls = [f'{proto}://{url}' if not url.startswith(f'{proto}://') else url for url in urls]
    ans = http_get_batch(processed_urls)
    disp_http(ans)


# Write log buffer to file
def write_log():
    with open('client_log.txt', 'a') as logfile:
        with log_buffer_lock:
            for entry in log_buffer:
                print(entry, file=logfile, end='')

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

################################################################################
############################## SCRIPT ENTRY POINT ##############################
################################################################################

def main():
    # parse CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('URLs', nargs='+', help='resource links to access')
    parser.add_argument('-p', '--proto', help='application protocol', default='http', choices=['http', 'https'])
    args = parser.parse_args()

    with ThreadPoolExecutor(max_workers=10) as executor:
        # Group URLs for batch processing
        urls_grouped = [args.URLs[i:i + BATCH_CHUNK_SIZE] for i in range(0, len(args.URLs), BATCH_CHUNK_SIZE)]
        futures = [executor.submit(process_url_batch, args.proto, group) for group in urls_grouped]

        # Wait for all futures to complete
        for future in futures:
            future.result()

    write_log()

if __name__ == '__main__':
    main()
