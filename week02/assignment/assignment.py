"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
global call_count
call_count = 0


# TODO Add your threaded class definition here
class Request_thread(threading.Thread):

    def __init__(self, url):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        response = requests.get(self.url)
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)

# TODO Add any functions you need here
def characters(film6, threads_c, call_count):

    for i in film6['characters']:
      thread = Request_thread(i)
      
      threads_c.append(thread)
    for i in threads_c:
        i.start()
        call_count += 1
    for i in threads_c:
        i.join()
    for i in threads_c:
        print(i.response['name'], end=", ")
    print()
    return call_count

def planets(film6, threads_p, call_count):
    for i in film6['planets']:
        thread = Request_thread(i)
        threads_p.append(thread)
    for i in threads_p:
        i.start()
        call_count += 1
    for i in threads_p:
        i.join()
    for i in threads_p:
        print(i.response['name'], end=", ")
    print()
    return call_count

def starships(film6, threads_s, call_count):
    for i in film6['starships']:
        thread = Request_thread(i)
        threads_s.append(thread)
    for i in threads_s:
        i.start()
        call_count += 1
    for i in threads_s:
        i.join()
    for i in threads_s:
        print(i.response['name'], end=", ")
    print()
    return call_count

def vehicles(film6, threads_v, call_count):
    for i in film6['vehicles']:
        thread = Request_thread(i)
        threads_v.append(thread)
    for i in threads_v:
        i.start()
        call_count += 1
    for i in threads_v:
        i.join()
    for i in threads_v:
        print(i.response['name'], end=", ")
    print()
    return call_count

def species(film6, threads_sp, call_count):
    for i in film6['species']:
        thread = Request_thread(i)
        threads_sp.append(thread)
    for i in threads_sp:
        i.start()
        call_count += 1
    for i in threads_sp:
        i.join()
    for i in threads_sp:
        print(i.response['name'], end=", ")
    print()
    return call_count

# def display(threads):
#     for i in threads:
#       print(i)
        
def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')
    threads_c = []
    threads_v = []
    threads_s = []
    threads_sp = []
    threads_p = []
    
    # TODO Retrieve Top API urls
    top = Request_thread(TOP_API_URL)
    top.start()
    top.join()
    
    # TODO Retireve Details on film 6
    film6 = Request_thread(f'{top.response["films"]}6')
    film6.start()
    film6.join()
    global call_count
    call_count = characters(film6.response, threads_c, call_count)
    call_count = planets(film6.response, threads_p, call_count)
    call_count = starships(film6.response, threads_s, call_count)
    call_count = vehicles(film6.response, threads_v, call_count)
    call_count = species(film6.response, threads_sp, call_count)
    
    # TODO Display results
    # display(threads)
    
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
