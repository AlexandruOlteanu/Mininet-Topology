#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests     # http(s) requests
import argparse     # argument parsing

# ANSI color escape codes
ANSI_RED     = '\033[31m'
ANSI_GREEN   = '\033[32m'
ANSI_YELLOW  = '\033[33m'
ANSI_BLUE    = '\033[34m'
ANSI_MAGENTA = '\033[35m'
ANSI_CLR     = '\033[0m'
ANSI_BOLD    = '\033[1m'
ANSI_UNBOLD  = '\033[2m'

################################################################################
############################### CLIENT BACKENDS ################################
################################################################################

# http_get - performs an HTTP(S) GET and returns relevant info
#   @url : the URL; must start with http:// or https://
#
#   @return : list of (url, status__code, elapsed_time [μs]) tuples
#             one for each redirect
def http_get(url: str):
    ret = [ ]

    # follow redirects and measure them independently
    while True:
        req = requests.get(url, allow_redirects=False)
        ret.append((url, req.status_code, req.elapsed.microseconds))

        # if server answer is a redirect, try again
        if req.is_redirect and req.next.url != None:
            url = req.next.url
        else:
            break

    return ret

################################################################################
########################### RESPONSE PRETTY PRINTERS ###########################
################################################################################

# disp_http - display http responses
#   @resp_list : value returned by http_get()
def disp_http(resp_list):
    for resp in resp_list:
        # select color for status message depending on class
        sm_color = ANSI_MAGENTA     # this signifies an invalid code
        if 100 <= resp[1] < 200:    # Informational Response
            sm_color = ANSI_BLUE
        if 200 <= resp[1] < 300:    # Successful Response
            sm_color = ANSI_GREEN
        if 300 <= resp[1] < 400:    # Redirection Response
            sm_color = ANSI_YELLOW
        if 400 <= resp[1] < 500:    # Client Error Response
            sm_color = ANSI_RED
        if 500 <= resp[1] < 600:    # Server Error Response
            sm_color = ANSI_RED

        # print the info
        logfile = open('client_log.txt', 'w+')
        print('%sURL :%s %s%s' % \
              (ANSI_BOLD, ANSI_UNBOLD, resp[0], ANSI_CLR), file = logfile)
        print('%sCODE:%s %s%d%s' % \
              (ANSI_BOLD, ANSI_UNBOLD, sm_color, resp[1], ANSI_CLR), file = logfile)
        print('%sTIME:%s %d [microsecs]%s' % \
              (ANSI_BOLD, ANSI_UNBOLD, resp[2], ANSI_CLR), file = logfile)
        print("\n", file = logfile)
        logfile.close()


################################################################################
############################## SCRIPT ENTRY POINT ##############################
################################################################################

def main():
    # parse CLI arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('URL',
                        help='resource link to access')
    parser.add_argument('-p', '--proto',
                        help='application protocol',
                        choices=[ 'http', 'https' ])
    cfg = parser.parse_args()

    # select backend depending on protocol
    if cfg.proto == 'http':
        if not cfg.URL.startswith('http://'):
            cfg.URL = 'http://' + cfg.URL

        ans = http_get(cfg.URL)
        disp_http(ans)
    elif cfg.proto == 'https':
        if not cfg.URL.startswith('https://'):
            cfg.URL = 'https://' + cfg.URL

        ans = http_get(cfg.URL)
        disp_http(ans)
    else:
        parser.print_help()
        exit(-1)

if __name__ == '__main__':
    main()

