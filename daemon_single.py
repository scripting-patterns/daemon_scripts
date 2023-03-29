#!/usr/bin/env python3
import os
import sys
import time
import re

LOG_FILE = "/var/log/httpd/access_log"

def mail_out(broken_link, referrer):
    print (
    """
    Write your code to send out the mail alerts
    {missing_link} is missing refered from {referrer}
    """.format(missing_link=broken_link, referrer=referrer)
    )


def main():
    pid = os.fork()

    if(pid):
        print("Daemonizing...\n")
        sys.exit(0)
    else:
        try:
            with open(LOG_FILE) as log:
                log.seek(0, 2) #seek to the end
                while True:
                    for line in log:
                        match = re.search(
                            r'GET\s{1,}([^\s]{1,})\s{1,}[^\s]{1,}\s{1,}404\s{1,}\d{1,}\s{1,}([^\s]{1,})', 
                            line
                        )
                        if match:
                            mail_out(match.group(1), match.group(2))
                    time.sleep(1)
        except OSError:
            print ("Unable to open file {}\n".format(LOG_FILE))
            sys.exit(1)

if __name__ == "__main__":
    main()
