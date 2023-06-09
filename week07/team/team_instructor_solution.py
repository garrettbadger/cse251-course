"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau
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
call_count = 0

chars = []
planets = []
stars = []
vehs = []
species = []


# -------------------------------------------------------------------------------
class Request_thread(threading.Thread):

    def __init__(self, url, data):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.url = url
        self.data = data

    def run(self):
        global call_count
        response = requests.get(self.url)
        call_count += 1
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.data.append(response.json())

# -------------------------------------------------------------------------------
def get_url(url):
    print(url, flush=True)

    results = []

    t = Request_thread(url, results)
    t.start()
    t.join()

    return results[0]


def cb_char(result):
   chars.append(result)

def cb_planet(result):
   planets.append(result)

def cb_star(result):
   stars.append(result)

def cb_veh(result):
   vehs.append(result)

def cb_species(result):
   species.append(result)

# -------------------------------------------------------------------------------
def print_film_details(log, film, chars, planets, starships, vehicles, species):
    log.write('-' * 40)
    log.write(f'Title   : {film["title"]}')
    log.write(f'Director: {film["director"]}')
    log.write(f'Producer: {film["producer"]}')
    log.write(f'Released: {film["release_date"]}')

    log.write('')
    log.write(f'Characters: {len(chars)}')

    names = sorted([item["name"] for item in chars])
    name_str = ''
    for str in names:
      name_str += str + ', '
    log.write(name_str)

    log.write('')
    log.write(f'Planets: {len(planets)}')
    names = sorted([item["name"] for item in planets])
    name_str = ''
    for str in names:
      name_str += str + ', '
    log.write(name_str)

    log.write('')
    log.write(f'Starships: {len(starships)}')
    names = sorted([item["name"] for item in starships])
    name_str = ''
    for str in names:
      name_str += str + ', '
    log.write(name_str)

    log.write('')
    log.write(f'Vehicles: {len(vehicles)}')
    names = sorted([item["name"] for item in vehicles])
    name_str = ''
    for str in names:
      name_str += str + ', '
    log.write(name_str)

    log.write('')
    log.write(f'Species: {len(species)}')
    names = sorted([item["name"] for item in species])
    name_str = ''
    for str in names:
      name_str += str + ', '
    log.write(name_str)


# -------------------------------------------------------------------------------
def main():

    pool = mp.Pool(10)

    log = Log(show_terminal=True)

    log.start_timer('Starting to retrieve data from swapi.dev')

    # Retrieve Top API urls
    urls = []
    t = Request_thread(TOP_API_URL, urls)
    t.start()
    t.join()
    # log.write(urls)

    # Retrieve film 6 details   
    top_urls = urls[0]
    film_url = top_urls['films']

    film6 = []
    t = Request_thread(f'{film_url}6', film6)
    t.start()
    t.join()
    # log.write(film6)
    film_data = film6[0]

    # Retrieve details about the film
    for url in film_data['characters']:
        pool.apply_async(get_url, args=(url,), callback=cb_char)
    for url in film_data['planets']:
        pool.apply_async(get_url, args=(url,), callback=cb_planet)
    for url in film_data['starships']:
        pool.apply_async(get_url, args=(url,), callback=cb_star)
    for url in film_data['vehicles']:
        pool.apply_async(get_url, args=(url,), callback=cb_veh)
    for url in film_data['species']:
        pool.apply_async(get_url, args=(url,), callback=cb_species)

    pool.close()
    pool.join()

    # Display results
    print_film_details(log, film_data, chars, planets, stars, vehs, species)

    log.write('')
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to swapi server')


if __name__ == "__main__":
    main()
