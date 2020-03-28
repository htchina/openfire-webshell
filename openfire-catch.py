#! /usr/bin/env python3

import requests
import sys
import threading
import queue
import time

if len(sys.argv) == 1:
    sys.exit(0)

threads = int(sys.argv[2])
servers_file = sys.argv[1]
timeout = 8

class challengeUrl(threading.Thread):
    def __init__(self, url, queue):
        threading.Thread.__init__(self)
        self.url = url
        self.q = queue

    def run(self):
        global found
        s = test_sever(self.url)
        if s:
            with open(".openfire", 'a') as f:
                f.write(self.url + "\n")
                f.flush()
            found += 1
            #print("\r                                        ", end="")
            print("\rQueued: ", str(round(c * 100 / len(servers), 2)) + "%", "Found: ", found, end="")
            sys.stdout.flush()
        self.q.get()
        self.q.task_done()



def test_sever(url):
    global timeout, thread_counter, port
    url = "http://" + url + ":9090"
    try:
        s = requests.head(url + "/favicon.ico", verify=False, timeout=timeout)
        if str(s.headers).find("'Content-Length': '1150'") != -1:
            second_req = requests.get(url + "/index.jsp")
            if second_req.text.find("Welcome to Setup") != -1:
                return 1
        return 0
    except:
        return 0

# Getting servers


if __name__ == "__main__":
    try:
        thread_counter = 0
        
        with open(sys.argv[1], 'r') as f:
            servers = f.readlines()

        for i in range(len(servers)):
            servers[i] = servers[i].strip()

        print("Total to scan: ", len(servers))
        active_threads = queue.Queue(maxsize=threads)
        c = 0
        found = 0
        to_del = len(str(c)) + 1

        for i in servers:

            while True:
                if active_threads.full():
                    time.sleep(.2)
                    continue

                t = challengeUrl(i, active_threads)
                active_threads.put(t)
                thread_counter += 1
                t.start()
                c += 1
                break


    except KeyboardInterrupt:
        print(thread_counter)
        print("LAST:", i)
        exit()

    except Exception as e:
        print(e)
        exit()

