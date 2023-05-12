"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

"""
from multiprocessing import Semaphore
import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 2        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(q, log, number_in_queue_sem):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        number_in_queue_sem.acquire()
        # TODO check to see if anything is in the queue
        if q.get() != NO_MORE_VALUES:
            if q.qsize() > 0:
            # TODO process the value retrieved from the queue
                url = q.get()
                # log.write(url)
            # TODO make Internet call to get characters name and log it
                response = requests.get(url)
                # log.write(response)
                if response.status_code == 200:
                    json_response = response.json()
                    log.write(json_response['name'])
        else:
            break
        
        pass



def file_reader(q, log, number_in_queue_sem): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "urls.txt" and place items into a queue
    with open("urls.txt") as file:
        for line in file:
            value = line.strip()
        # log.write(data)
            q.put(value)
            number_in_queue_sem.release()
    log.write('finished reading file')
    # log.write(q.qsize())
    # TODO signal the retrieve threads one more time that there are "no more values"
    for i in range(RETRIEVE_THREADS):
        q.put(NO_MORE_VALUES)


def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue
    q = queue.Queue()
    # TODO create semaphore (if needed)
    number_in_queue_sem = Semaphore(RETRIEVE_THREADS)
    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job
    reader = threading.Thread(target=file_reader, args=(q, log, number_in_queue_sem))
    threads = [ threading.Thread(target=retrieve_thread, args=(q, log, number_in_queue_sem)) for _ in range(RETRIEVE_THREADS)]
    # for i in range(RETRIEVE_THREADS):
    #     t = threading.Thread(target=retrieve_thread, args=(q, log, number_in_queue_sem))
    #     threads.append(t)
    log.start_timer()

    # TODO Get them going - start the retrieve_threads first, then file_reader
    for t in threads:
        t.start()
    reader.start()
    
    # TODO Wait for them to finish - The order doesn't matter
    reader.join()
    for t in threads:
        t.join()
    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()




