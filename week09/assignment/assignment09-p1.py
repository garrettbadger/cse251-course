"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p1.py 
Author: Garrett Badger

Purpose: Part 1 of assignment 09, finding a path to the end position in a maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included

"""
import math
from screen import Screen
from maze import Maze
import cv2
import sys

# Include cse 251 common Python files - Dont change
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)


# TODO add any functions


def solve_path(maze):
    """ Solve the maze and return the path found between the start and end positions.  
        The path is a list of positions, (x, y) """
        
    # TODO start add code here
    path = []
    #recursive function
    # def _solve(maze, pos, path): # needs to return true or false if you found the end or not.
    #     pass
    # _solve(maze, maze.get_start(), path)


    def _solve(x, y): # needs to return true or false if you found the end or not.
       
        #base case
        if maze.at_end(x, y):
            return True
        
        poss = maze.get_possible_moves(x, y)

        if len(poss) == 0:
            return False
        
        # do stuff
        # try moves from the possible list
        # update path variable
        for m in poss:
            if maze.can_move_here(*m):
                maze.move(*m, COLOR)
                path.append(m)
            if _solve(*m):
                return True
            else:
                maze.restore(*m)
                if len(path) > 0:
                    path.pop()
        return False        


    start = maze.get_start_pos()
    path.append(start)
    maze.move(*start, COLOR)
    _solve(start[0], start[1])
    
    


    return path


def get_path(log, filename):
    """ Do not change this function """

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    path = solve_path(maze)

    log.write(f'Number of drawing commands for = {screen.get_command_count()}')

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

    return path


def find_paths(log):
    """ Do not change this function """

    files = ('verysmall.bmp', 'verysmall-loops.bmp', 
            'small.bmp', 'small-loops.bmp', 
            'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    log.write('*' * 40)
    log.write('Part 1')
    for filename in files:
        log.write()
        log.write(f'File: {filename}')
        path = get_path(log, filename)
        log.write(f'Found path has length          = {len(path)}')
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_paths(log)


if __name__ == "__main__":
    main()