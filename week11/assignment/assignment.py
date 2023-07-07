"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
Name: Garrett Badger
Rationale: I think I deserve a 3 because I completed the requirements but occasionally I get 
a lock error and I am not sure why. 
"""
import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'


room_lock = mp.Lock()
cleaning_staff_counter = mp.Value('i', 0)
guest_counter = mp.Value('i', 0)
party_count = mp.Value('i', 0)
cleaned_count = mp.Value('i', 0)

def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id, count):
    print(f'Guest: {id}, count = {count}')
    time.sleep(random.uniform(0, 1))

def cleaner(start_time, cleaned_count, cleaning_staff_counter, guest_counter, room_lock):
    
    while time.time() - start_time < TIME:
        cleaner_waiting()

        room_lock.acquire()
        if cleaning_staff_counter.value == 0 and guest_counter.value == 0:
            print(STARTING_CLEANING_MESSAGE)
            cleaning_staff_counter.value += 1
            cleaned_count.value += 1

            cleaner_cleaning(mp.current_process().name)
       
            cleaning_staff_counter.value -= 1
            if cleaning_staff_counter.value == 0 and guest_counter.value == 0:
                print(STOPPING_CLEANING_MESSAGE)
                room_lock.release()
                
def guest(start_time, party_count, cleaning_staff_counter, guest_counter, room_lock):
    
    room_lock.acquire()
    while time.time() - start_time < TIME:
        
        guest_waiting()
        
        if cleaning_staff_counter.value == 0:
            if guest_counter.value == 0:
                print(STARTING_PARTY_MESSAGE)
            guest_counter.value += 1

            guest_partying(mp.current_process().name, guest_counter.value)

            guest_counter.value -= 1
            if guest_counter.value == 0:
                print(STOPPING_PARTY_MESSAGE)
                party_count.value += 1
                room_lock.release()
                guest_waiting()
                
def main():
    
    # Start time of the running of the program.
    start_time = time.time()

    # Create and start cleaner processes
    cleaner_processes = []
    for i in range(CLEANING_STAFF):
        cleaner_process = mp.Process(target=cleaner, args=(start_time, cleaned_count, cleaning_staff_counter, guest_counter, room_lock))
        cleaner_processes.append(cleaner_process)
        cleaner_process.start()

    # Create and start guest processes
    guest_processes = []
    for i in range(HOTEL_GUESTS):
        guest_process = mp.Process(target=guest, args = (start_time, party_count, cleaning_staff_counter, guest_counter, room_lock))
        guest_processes.append(guest_process)
        guest_process.start()

    for cleaner_process in cleaner_processes:
        cleaner_process.join()

    for guest_process in guest_processes:
        guest_process.join()

    # Results
    print(f'Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties')

if __name__ == '__main__':
    main()
