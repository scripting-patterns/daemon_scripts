#!/usr/bin/env python3
import os
import sys
import time
import multiprocessing
import selectors

NUM_PROCESS = 5

def main():
    # fork to daemonize the script
    pid = os.fork()

    if(pid):
        print("Daemonizing...\n")
        sys.exit(0)
    else:
        # we collect all the pipes to list
        pipes = []

        # selector to figureout which pipes to read
        # and which pipes are ready to read
        selector = selectors.DefaultSelector()

        for proc in range(NUM_PROCESS):
            # create the pipes
            pipes.append(multiprocessing.Pipe())

            if not os.fork(): # we're inside the child process

                # close the read pipe, we don't need to read from the 
                pipes[proc][0].close()
                count = 0
                while True:
                    count += 1
                    # write to the pipes 
                    pipes[proc][1].send(
                        "Process {proc}: {count}".format(
                            proc=proc, 
                            count=count
                        )
                    )
                    time.sleep(proc)
            else:
                pipes[proc][1].close()
                selector.register(pipes[proc][0], selectors.EVENT_READ) 

                # once we spawn the last child process, start listening to 
                # pipes for data.
                if proc == NUM_PROCESS-1: 
                    while True:
                        events = selector.select(timeout=1)
                        for key, mask in events:
                            print(key.fileobj.recv())
                        time.sleep(2)

if __name__ == "__main__":
    main()
