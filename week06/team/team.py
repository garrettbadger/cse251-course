"""
Course: CSE 251
Lesson Week: 06
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe

After you can copy a text file word by word exactly
- Change the program to be faster (Still using the processes)

"""

import multiprocessing as mp
from multiprocessing import Value, Process
import filecmp 

# Include cse 251 common Python files
from cse251 import *

def sender(filename, parent):
    """ function to send messages to other end of pipe """
    '''
    open the file
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe

    '''
    
    with open(filename) as f:
        for line in f:
            line = line.split(' ')
            # parent.send(line)
            for word in line:
                if word != len(line)-1 or word != len(line)-2:
                    parent.send(word)
                    parent.send(' ')
                else:
                    parent.send(word)
    parent.send(-1)
    parent.close()
    


def receiver(filename, child, count):
    """ function to print the messages received from other end of pipe """
    ''' 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    '''
    with open(filename, 'a') as f:
        while True:
            word = child.recv()
            if word == -1:
                break
        
            f.write(word)
            count.value += 1
        
    child.close()


def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow = False) 


def copy_file(log, filename1, filename2):
    if (os.path.exists(filename2)):
        os.remove(filename2)
    # TODO create a pipe 
    parent, child = mp.Pipe()
    # TODO create variable to count items sent over the pipe
    count = Value('i', 0)
    # TODO create processes 
    send = mp.Process(target=sender, args=(filename1, parent, ))
    receive = mp.Process(target=receiver, args=(filename2, child, count,))
    log.start_timer()
    start_time = log.get_time()

    # TODO start processes 
    send.start()
    receive.start()
    # TODO wait for processes to finish
    send.join()
    receive.join()
    stop_time = log.get_time()

    log.stop_timer(f'Total time to transfer content = {stop_time - start_time}: ')
    log.write(f'items / second = {count.value/ (stop_time - start_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__": 

    log = Log(show_terminal=True)

    copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')
    
    # After you get the gettysburg.txt file working, uncomment this statement
    # copy_file(log, 'bom.txt', 'bom-copy.txt')

