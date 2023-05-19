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

PRIME_PROCESS_COUNT = 10

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
def read_thread(filename, q, log, amount_of_numbers_in_queue, unused_spots_in_queue):
    """ This thread reading the data file and places the values in the data_queue """

    # TODO Open the data file "urls.txt" and place items into a queue
    with open(filename) as file:
        for line in file:
            value = line.strip()
            unused_spots_in_queue.acquire()
            q.put(int(value))
            amount_of_numbers_in_queue.release()

        log.write(q.qsize())
    for _ in range(PRIME_PROCESS_COUNT):
        unused_spots_in_queue.acquire()
        q.put(-1)
        amount_of_numbers_in_queue.release()
 
# TODO create prime_process function
def process_function(q, primes, amount_of_numbers_in_queue, unused_spots_in_queue):
    while True:
        start_time = time.perf_counter()
        
        amount_of_numbers_in_queue.acquire()
        prime = q.get()
        unused_spots_in_queue.release()

        if prime < 0:
            break

        if is_prime(prime):
            print(prime)
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
    # must = 10 always

    amount_of_numbers_in_queue = mp.Semaphore(0)
    unused_spots_in_queue = mp.Semaphore(10)

    # TODO create reading thread
    reader = threading.Thread(target=read_thread, args=(filename, q, log, amount_of_numbers_in_queue, unused_spots_in_queue))
    # TODO create prime processes
    
    processes = [mp.Process(target=process_function, args=(q, primes, amount_of_numbers_in_queue, unused_spots_in_queue)) for _ in range(PRIME_PROCESS_COUNT)]
    
    # TODO Start them all
    for p in processes:
        p.start()
    reader.start()
    

    
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

