"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls

Instructions:

- Review instructions in I-Learn.

"""

from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.card = {}
    def run(self):
        
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            self.card = data
            # self.card = data['cards'][0]['code']
            return(self.card)
        else:
            return('Error in requesting from url')

   

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        thread1 = Request_thread(f'https://deckofcardsapi.com/api/deck/{deck_id}/shuffle/')
        thread1.start()
        thread1.join()
        

    def draw_card(self):
        thread2 = Request_thread(f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1')
        thread2.start()
        thread2.join()
        if thread2 != {}:
            self.remaining = thread2.card['remaining']
            return thread2.card['cards'][0]['code']

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = '0eqkwj2ruu81'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(i, card, flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<

