"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: Garrett Badger

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included
- Each thread requires a different color by calling get_color()


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

You could probably use a list like we did before since they are thread safe.


Why would it work?

I think it would work because lists are thread safe. 

"""
import math
import threading 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 common Python files - Dont change
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color


def solve_find_end(maze):
 
    """ finds the end position using threads. Nothing is returned """
    # When one of the threads finds the end position, stop all of them
    global stop
    stop = False
    global thread_count
    thread_count = 0
    lock = threading.Lock()
    threads = []
    # Inner recursive function
    def _solve(x, y, color):
        global stop
        global thread_count

        if maze.at_end(x, y):
            stop = True

        if stop:
            return

        with lock:
            poss = maze.get_possible_moves(x, y)

        if len(poss) == 0:
            return
        
        # get moves
        # create threads
        # go down path myself
        # then join
        # maze is a critical section; get in and out as fast as possible
        # get_possible needs to be locked
        # might be hanging because of threads not joining properly

        for move in poss:
            new_x, new_y = move
            with lock:
                if maze.can_move_here(new_x, new_y):
                    maze.move(new_x, new_y, color)
            if len(poss) > 1:
                thread = threading.Thread(target=_solve, args=(new_x, new_y, get_color()))
                thread_count += 1
                threads.append(thread)
                thread.start()
            else:
                _solve(new_x, new_y, color)

        for thread in threads:
            thread.join()
          
    start = maze.get_start_pos()
    color = get_color()
    maze.move(*start, color)
    thread = threading.Thread(target=_solve, args=(start[0], start[1], color))
    thread_count+=1
    thread.start()
    thread.join()
    

def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count
    global speed
    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False) 
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()