"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: <your name>

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  

- Do not use try...except statements

- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable>, end=', ', flush=True)

Add any comments for me:

"""

import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp
import time

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2
WRITE_INDEX = 10 
READ_INDEX = 11
CURRENT_VALUE = 12
VALUES_RECEIVED = 13

def reader(shared, reader_sem, writer_sem, items_to_send, lock):
    for i in range(items_to_send):
        # if (shared[BUFFER_SIZE + WRITE_INDEX] != shared[BUFFER_SIZE + READ_INDEX]):
			
            reader_sem.acquire()
            with lock:
      
                position = shared[READ_INDEX]
                value = shared[position]
                values_received = shared[VALUES_RECEIVED]
                values_received += 1
                position = (position + 1) % BUFFER_SIZE
                shared[READ_INDEX] = position
                shared[VALUES_RECEIVED] = values_received
    
            print(f'Value: {value} Total Received: {values_received}')
            writer_sem.release()
    
def writer(shared, reader_sem, writer_sem, items_to_send, lock):
    while True:
        # if (shared[BUFFER_SIZE + WRITE_INDEX + 1] % BUFFER_SIZE != shared[BUFFER_SIZE + READ_INDEX]):

            writer_sem.acquire()
            
            if items_to_send == shared[VALUES_RECEIVED]:
                break
            with lock:
                position = shared[WRITE_INDEX]
                value = shared[CURRENT_VALUE]
                shared[position] = value
                value += 1
                position = (position + 1) % BUFFER_SIZE
                shared[CURRENT_VALUE] = value
                shared[WRITE_INDEX] = position
            reader_sem.release()

def main():

    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(100, 1000)

    smm = SharedMemoryManager()
    smm.start()
    
    # TODO - Create a ShareableList to be used between the processes
    #      - The buffer should be size 10 PLUS at least three other
    #        values (ie., [0] * (BUFFER_SIZE + 3)).  The extra values
    #        are used for the head and tail for the circular buffer.
    #        The another value is the current number that the writers
    #        need to send over the buffer.  This last value is shared
    #        between the writers.
    #        You can add another value to the sharedable list to keep
    #        track of the number of values received by the readers.
    #        (ie., [0] * (BUFFER_SIZE + 4))
    shared = smm.ShareableList([0] * (BUFFER_SIZE + 4))
    print(items_to_send)
    print(shared)
    time.sleep(2)
    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    reader_sem = mp.Semaphore(0)
    writer_sem = mp.Semaphore(BUFFER_SIZE)
    lock = mp.Lock()
    # TODO - create reader and writer processes
    writers = [mp.Process(target=writer, args=(shared, reader_sem, writer_sem, items_to_send, lock)) for i in range(WRITERS)]
    readers = [mp.Process(target=reader, args=(shared, reader_sem, writer_sem, items_to_send, lock)) for i in range(READERS)]
    # TODO - Start the processes and wait for them to finish
    for r in readers:
        r.start()
    for w in writers:
        w.start()
    for r in readers:
        r.join()
    for w in writers:
        w.join()
    
    print(f'{items_to_send} values sent')

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    # print(f'{<your variable>} values received')
    print(f'Values sent: {shared[VALUES_RECEIVED]}')
    smm.shutdown()


if __name__ == '__main__':
    main()