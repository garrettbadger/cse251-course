"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: <Add name here>

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included
- Each thread requires a different color by calling get_color()


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

<Answer here>


Why would it work?

<Answer here>

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
  

    # Inner recursive function
    def _solve(x, y, color):
        global stop
        global thread_count

        if stop:
            return

        if maze.at_end(x, y):
            stop = True
            return

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
        for m in poss:
            # all below maze methods need a lock
            if maze.can_move_here(*m):
                maze.move(*m, color)
                new_poss = maze.get_possible_moves(*m)
                if len(new_poss) > 1:
                    if m == new_poss[0]:
                        _solve(*m, color)
                    else:
                        thread_count += 1
                        thread = threading.Thread(target=_solve, args=(*m, get_color()))
                        thread.start()
                        thread.join()
                else:
                    _solve(*m, color)
            
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