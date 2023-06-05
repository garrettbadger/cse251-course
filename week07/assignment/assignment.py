"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: <Your name here>
Purpose: Process Task Files

Instructions:  See I-Learn

TODO

For my pool sizes I set them all to 1 and then just modified one of the pools to have more than a size of 1
this told me that just changing the pool size of one of the pools didn't have an effect on the overall time.
Because of this I chose to increment them all together. The best time I got on my system was 7.856 seconds with
all 5 pools having a pool size of 9.


"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
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
 
def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    prime = is_prime(value)
    if prime:
        result = f'{value:,} is prime'
        return result
        
    else:
        result = f'{value:,} is not prime'
        return result
        
    

def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    if len(word_list) <= 0:
        word_list = []
        with open('words.txt') as f:
            for line in f:
                line = f.readline()
                line = line.rstrip()
                word_list.append(line)
    if word in word_list:
        result = f'{word} found'
        return result
        
    else:
        result = f'{word} not found'
        return result
        
    

def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    upper_text = text.upper()
    result = f'{text} ==> {upper_text}'
    return result
    
    

def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    new_term = (end_value - start_value + 1) / 1
    total = (new_term / 2) * (start_value + end_value)
    result = f'sum of {start_value:,} to {end_value:,} = {total:,}'
    return result
    

    

def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    response = requests.get(url)
        # Check the status code to see if the request succeeded.
    if response.status_code == 200:
        response = response.json()
        result = f'{url} has name {response["name"]}'
        return result
        
    else:
        result = f'{url} had an error receiving information error: {response.status_code}'
        return result
        
       
    
def prime_callback(result):
    result_primes.append(result)

def upper_callback(result):
    result_upper.append(result)

def word_callback(result):
    result_words.append(result)

def sum_callback(result):
    result_sums.append(result)

def name_callback(result):
    result_names.append(result)


def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    pools = []
    name_pool = mp.Pool(9)
    sum_pool = mp.Pool(9)
    prime_pool = mp.Pool(9)
    upper_pool = mp.Pool(9)
    word_pool = mp.Pool(9)
    pools.append(name_pool)
    pools.append(sum_pool)
    pools.append(prime_pool)
    pools.append(word_pool)
    pools.append(upper_pool)
    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            # task_prime(task['value'])
            prime_pool.apply_async(task_prime, args=(task['value'],), callback=prime_callback)
        elif task_type == TYPE_WORD:
            # task_word(task['word'])
            word_pool.apply_async(task_word, args=(task['word'],), callback=word_callback)
        elif task_type == TYPE_UPPER:
            # task_upper(task['text'])
            upper_pool.apply_async(task_upper, args=(task['text'],), callback=upper_callback)
        elif task_type == TYPE_SUM:
            # task_sum(task['start'], task['end'])
            sum_pool.apply_async(task_sum, args=(task['start'], task['end'],), callback=sum_callback)
        elif task_type == TYPE_NAME:
            # task_name(task['url'])
            name_pool.apply_async(task_name, args=(task['url'],), callback=name_callback)
        else:
            log.write(f'Error: unknown task type {task_type}')

    # TODO start and wait pools
    for p in pools:
        p.close()
    for p in pools:
        p.join()

    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()
