"""
Course: CSE 251
Lesson Week: 10
File: team2.py
Author: Brother Comeau
Instructions:
- Look for the TODO comments
"""

import time
import threading
import mmap
import string
import os
import random

THREADS = 2

# -----------------------------------------------------------------------------
def reverse_file(filename):
    """ Display a file in reverse order using a mmap file. """
    # TODO add code here
    with open(filename, mode='r', encoding ='utf8') as data:
        with mmap.mmap(data.fileno(), length=0, access=mmap.ACCESS_READ) as map_file:
            for i in range(1, map_file.size()+1):
                print(chr(map_file[-i]), end='')
 


# -----------------------------------------------------------------------------
def promote_letter_a(filename):
    """ 
    change the given file with these rules:
    1) when the letter is 'a', uppercase it
    2) all other letters are changed to the character '.'

    You are not creating a different file.  Change the file using mmap file.
    """
    # TODO add code here
    with open(filename, mode='r+', encoding ='utf8') as data:
        with mmap.mmap(data.fileno(), length=0, access=mmap.ACCESS_WRITE) as map_file:
            for i in range(map_file.size()):
                if map_file[i] == 97:
                    map_file[i] = 65
                else:
                    map_file[i] = 46

    pass


# -----------------------------------------------------------------------------
def promote_letter_a_threads(filename):
    """ 
    change the given file with these rules:
    1) when the letter is 'a', uppercase it
    2) all other letters are changed to the character '.'

    You are not creating a different file.  Change the file using mmap file.

    Use N threads to process the file where each thread will be 1/N of the file.
    """
    # TODO add code here
    lock = threading.Lock()
    threads = [threading.Thread(target=promote_letter_a_threads, args=[filename]) for _ in range(THREADS)]
    for t in threads:
        t.start()
        with lock:
            with open(filename, mode='r+', encoding ='utf8') as data:
                with mmap.mmap(data.fileno(), length=0, access=mmap.ACCESS_WRITE) as map_file:
                    for i in range(map_file.size()):
                        if map_file[i] == 97:
                            map_file[i] = 65
                        else:
                            map_file[i] = 46
    for t in threads:
        t.join()
    pass


# -----------------------------------------------------------------------------
def create_data_file(filename):
    
    words = []
    for _ in range(1000):
        word = ''
        for _ in range(10):
            word += random.choice(string.ascii_lowercase)
        words.append(word)

    with open(filename, 'w') as f:
        for i in range(1000000):
            if i % 25000 == 0:
                print('.', end='', flush=True)

            for _ in range(8):
                f.write(random.choice(words))

            f.write('\n')
        print()
# -----------------------------------------------------------------------------
def main():
    create_data_file('letter_a.txt')
    reverse_file('data.txt')
    # promote_letter_a('letter_a.txt')
    
    # TODO
    # When you get the function promote_letter_a() working
    #  1) Comment out the promote_letter_a() call
    #  2) run create_Data_file.py again to re-create the "letter_a.txt" file
    #  3) Uncomment the function below
    promote_letter_a_threads('letter_a.txt')

if __name__ == '__main__':
    main()
