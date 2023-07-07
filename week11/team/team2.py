"""
Course: CSE 251
Lesson Week: 11
File: team2.py
Author: Brother Comeau

Purpose: Team Activity 2: Queue, Pipe, Stack

Instructions:

Part 1:
- Create classes for Queue_t, Pipe_t and Stack_t that are thread safe.
- You can use the List() data structure in your classes.
- Once written, test them using multiple threads.

Part 2
- Create classes for Queue_p, Pipe_p and Stack_p that are process safe.
- You can use the List() data structure in your classes.
- Once written, test them using multiple processes.

Queue methods:
    - constructor(<no arguments>)
    - size()
    - get()
    - put(item)

Stack methods:
    - constructor(<no arguments>)
    - push(item)
    - pop()

Steps:
1) write the Queue_t and test it with threads.
2) write the Queue_p and test it with processes.
3) Implement Stack_t and test it 
4) Implement Stack_p and test it 

Note: Testing means having lots of concurrency/parallelism happening.  Also
some methods for lists are thread safe - some are not.

"""
import time
import threading
import multiprocessing as mp

# -------------------------------------------------------------------
class Queue_t:
    def __init__(self):
        self.lock = threading.Lock()
        self.queue = []
    def size(self):
        with self.lock:
            return len(self.queue)
        
    def get(self):
        with self.lock:
            return self.queue.pop(0)
        
    def put(self, item):
        with self.lock:
            self.queue.append(item)
        
    

# -------------------------------------------------------------------
class Stack_t:
    def __init__(self):
        self.lock = threading.Lock()
        self.stack = []

    def size(self):
        with self.lock:
            return len(self.stack)

    def push(self, item):
        with self.lock:
            self.stack.append(item)

    def pop(self):
        with self.lock:
            return self.stack.pop()

# -------------------------------------------------------------------
class Queue_p:
    def __init__(self):
        self.lock = mp.Lock()
        self.queue = mp.Manager.list()
    def size(self):
        with self.lock:
            return len(self.queue)
        
    def get(self):
        with self.lock:
            return self.queue.pop(0)
        
    def put(self, item):
        with self.lock:
            self.queue.append(item)

# -------------------------------------------------------------------
class Stack_p:
    def __init__(self):
        self.lock = mp.Lock()
        self.stack = mp.Manager.list()

    def push(self, item):
        with self.lock:
            self.stack.append(item)

    def pop(self):
        with self.lock:
            return self.stack.pop()
        
prime_count = 0
numbers_processed = 0

def is_prime(n: int) -> bool:
    global numbers_processed
    numbers_processed += 1

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


def process_range(start, end, stack):
    global prime_count
    for i in range(start, end):
        if is_prime(i):
            prime_count += 1
            
            stack.push(i)

def read_from_queue(queue):
    while True:
        if queue.size() <= 0:
            break
        print(queue.get(), end=', ', flush=True)
    print()

def read_from_stack(stack):
    while True:
        if stack.size() <= 0:
            break
        print(stack.pop(), end=', ', flush=True)
    print()
        

def main():


    start = 10_000_000_000
    range_count = 100_000

    number_threads = 10
    threads = []
    thread_range = range_count // number_threads
    queue = Queue_t()
    stack = Stack_t()
    # Create threads and give each one a range to test
    for i in range(10):
        thread_start = start + (thread_range * i)
        thread_end = thread_start + thread_range
        t = threading.Thread(target=process_range, args=(thread_start, thread_end, stack))
        threads.append(t)

    # Start all threads
    for t in threads:
        t.start()

    # Wait for them to finish
    for t in threads:
        t.join()
    
    threads2 = [threading.Thread(target = read_from_stack, args = (stack,)) for i in range(10)]
    for t in threads2:
        t.start()
    for t in threads2:
        t.join()
    print(f'Number of primes: {prime_count}. Number of numbers processed: {numbers_processed}')

if __name__ == '__main__':
    main()
