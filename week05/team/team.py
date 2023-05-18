"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import multiprocessing as mp
import random
import queue

#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 8

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# TODO create read_thread function
def read_thread(filename, q, log):
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "urls.txt" and place items into a queue
    with open(filename) as file:
        for line in file:
            value = line.strip()
            q.put(int(value))
        log.write(q.qsize())
    for _ in range(PRIME_PROCESS_COUNT):
        q.put(-1)
 
# TODO create prime_process function
def process_function(process_id, q, primes):
    while True:
        start_time = time.perf_counter()
        if q.get() == -1:
            return
        else:
        
            prime = q.get()
            
            if is_prime(prime):
                primes.append(prime)
        total_time = time.perf_counter() - start_time

    
    # print(f'Process {process_id}: time = {total_time:.5f}: primes found = {len(primes)}')


def create_data_txt(filename):
    with open(filename, 'w') as f:
        for _ in range(1000):
            f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'

    # Once the data file is created, you can comment out this line
    # create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    q = mp.Queue()
    primes = mp.Manager().list()
    # TODO create reading thread
    reader = threading.Thread(target=read_thread, args=(filename, q, log,))
    # TODO create prime processes
    
    processes = [mp.Process(target=process_function, args=(i, q, primes)) for i in range(PRIME_PROCESS_COUNT)]
    
    # TODO Start them all
    reader.start()
    for p in processes:
        p.start()

    
    # TODO wait for them to complete
    reader.join()
    for p in processes:
        p.join()
    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()

