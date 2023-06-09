"""
Course: CSE 251
Lesson Week: Week 07
File: team.py
Purpose: Week 05 Team Activity

Instructions:

- Make a copy of your assignment 2 program.  Since you are working in a team,
  you can design which assignment 2 program that you will use for the team
  activity.
- Convert the program to use a process pool and use apply_async() with a
  callback function to retrieve data from the Star Wars website.

"""

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

Justification: I think I deserve a 4 because my program uses threads to optimize the gathering of I/O bound data and matches the output example.
"""

from datetime import datetime, timedelta
import requests
import json
import threading
import multiprocessing as mp

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


def get_heading():
    
    print(f'Title: Revenge of the Sith')
    print(f'Director: George Lucas')
    print(f'Producer: Rick McCallum')
    print(f'Released: 05/19/2005')
    print()






def get_names2(urls, names):
    global call_count
    threads = []
    
    for url in urls:
        thread = Request_thread(url)
        threads.append(thread)
    for t in threads:
        t.start()
        call_count+=1
    for t in threads:
        t.join()
    for t in threads:
        names.append(t.response['name'])
    names.sort()
    return names
    
'''
words = 'the cat is big'.split()
print(words)
print(' '.join(words))
'''
def display(threads):
    for i in threads:
      print(i, end=', ')
    print()
    print()
        
def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')
  
    
    top = Request_thread(TOP_API_URL)
    top.start()
    top.join()
    
    
    film6 = Request_thread(f'{top.response["films"]}6')
    film6.start()
    film6.join()
    

    c= []
    v=[]
    s=[]
    sp=[]
    p=[]
    
    pool = mp.Pool(5)
    pool.apply_async(get_names2, args = (film6.response['characters'], c, ), callback=display)
    pool.apply_async(get_names2, args=(film6.response['vehicles'], v,), callback=display)
    pool.apply_async(get_names2, args=(film6.response['starships'], s,), callback=display)
    pool.apply_async(get_names2, args=(film6.response['species'], sp,), callback=display)
    pool.apply_async(get_names2, args=(film6.response['planets'], p, ), callback=display)
    pool.close()
    pool.join()
        
    # threads = []
    # threads.append(threading.Thread(target=get_names2, args=(film6.response['characters'], c, )))
    # threads.append(threading.Thread(target=get_names2, args=(film6.response['vehicles'], v,)))
    # threads.append(threading.Thread(target=get_names2, args=(film6.response['starships'], s, )))
    # threads.append(threading.Thread(target=get_names2, args=(film6.response['species'], sp,)))
    # threads.append(threading.Thread(target=get_names2, args=(film6.response['planets'], p, )))

    # for t in threads:
    #     t.start()
    # for t in threads:
    #     t.join()
    # display(c)
    # display(v)
    # display(s)
    # display(sp)
    # display(p)
            
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
