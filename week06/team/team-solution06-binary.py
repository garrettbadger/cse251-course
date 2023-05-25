import multiprocessing as mp
from multiprocessing import Value, Process
import filecmp 

# Include cse 251 common Python files
from cse251 import *

BLOCK_SIZE = 1024 * 4

END_MESSAGE = 'All Done!!'

def sender(conn, filename): 
    """ function to send messages to other end of pipe """
    with open(filename, "rb") as f:
        done = False
        while not done:
            block = f.read(BLOCK_SIZE)
            if block:
                conn.send(block) 
            else:
                done = True

    conn.send(END_MESSAGE)
    conn.close() 


def receiver(conn, count, filename): 
    """ function to print the messages received from other end of pipe """
    count.value = 0

    with open(filename, 'wb') as f:
        while True: 
            block = conn.recv() 
            if block == END_MESSAGE: 
                break
            count.value += 1
            f.write(block)
    
    conn.close()


def are_files_same(filename1, filename2):
    return filecmp.cmp(filename1, filename2, shallow = False) 


def copy_file(log, filename1, filename2):
    # creating a pipe 
    parent_conn, child_conn = mp.Pipe() 

    count = Value('i', 0)

    # creating new processes 
    p1 = mp.Process(target=sender, args=(parent_conn, filename1)) 
    p2 = mp.Process(target=receiver, args=(child_conn, count, filename2)) 

    log.start_timer()
    start_time = log.get_time()

    # running processes 
    p1.start() 
    p2.start() 

    # wait until processes finish 
    p1.join() 
    p2.join() 

    stop_time = log.get_time()

    log.stop_timer(f'Total time to transfer content = {count.value}: ')
    log.write(f'items / second = {count.value / (stop_time - start_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')



if __name__ == "__main__": 

    log = Log(show_terminal=True)

    # copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')
    
    # After you get the gettysburg.txt file working, uncomment this statement
    # to copy the Book of Mormon
    copy_file(log, 'bom.txt', 'bom-copy.txt')


"""
2021-01-14
12:48:27| Total time words transfered = 17971410:  = 248.73241030
12:48:27| Words / second = 72251.99123609411
"""