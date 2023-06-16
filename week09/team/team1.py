"""
Course: CSE 251
Lesson Week: 09
File: team1.py

Purpose: team activity - Dining philosophers problem

Problem statement

Five silent philosophers sit at a round table with bowls of spaghetti. Forks
are placed between each pair of adjacent philosophers.

Each philosopher must alternately think and eat. However, a philosopher can
only eat spaghetti when they have both left and right forks. Each fork can be
held by only one philosopher and so a philosopher can use the fork only if it
is not being used by another philosopher. After an individual philosopher
finishes eating, they need to put down both forks so that the forks become
available to others. A philosopher can only take the fork on their right or
the one on their left as they become available and they cannot start eating
before getting both forks.  When a philosopher is finished eating, they think 
for a little while.

Eating is not limited by the remaining amounts of spaghetti or stomach space;
an infinite supply and an infinite demand are assumed.

The problem is how to design a discipline of behavior (a concurrent algorithm)
such that no philosopher will starve

Instructions:

        **************************************************
        ** DO NOT search for a solution on the Internet **
        ** your goal is not to copy a solution, but to  **
        ** work out this problem.                       **
        **************************************************

- You have Locks and Semaphores that you can use.
- Remember that lock.acquire() has an argument called timeout.
- philosophers need to eat for 1 to 3 seconds when they get both forks.  
  When the number of philosophers has eaten MAX_MEALS times, stop the philosophers
  from trying to eat and any philosophers eating will put down their forks when finished.
- philosophers need to think for 1 to 3 seconds when they are finished eating.  
- You want as many philosophers to eat and think concurrently.
- Design your program to handle N philosophers and N forks after you get it working for 5.
- Use threads for this problem.
- When you get your program working, how to you prove that no philosopher will starve?
  (Just looking at output from print() statements is not enough)
- Are the philosophers each eating and thinking the same amount?
- Using lists for philosophers and forks will help you in this program.
  for example: philosophers[i] needs forks[i] and forks[i+1] to eat
"""

import time
import threading

PHILOSOPHERS = 5
MAX_MEALS = PHILOSOPHERS * 5
global meals_eaten 
meals_eaten = 0


class Philosopher(threading.Thread):
    def __init__(self, id, lock_meals, l_fork, r_fork):
        threading.Thread.__init__(self)
        self.l_fork = l_fork
        self.r_fork = r_fork
        self.ate = 0
        self.id = id
        self.lock_meals = lock_meals

    def run(self):
       global meals_eaten
       done = False
       while not done:
           with self.lock_meals:
               if meals_eaten >= MAX_MEALS:
                   done = True
                   continue
            self.l_fork.acquire()
           if not
       if meals_eaten < MAX_MEALS:
          self.l_fork.acquire()
          self.r_fork.acquire()
          time.sleep(2) 
          self.l_fork.release()
          self.r_fork.release()
          meals_eaten += 1
          self.thinking()      
    def thinking(self):
        time.sleep(2)



    


def main():
    # TODO - create the forks
    forks = [threading.Lock() for i in range(PHILOSOPHERS)]
    
    # TODO - create PHILOSOPHERS philosophers
    philosophers = [Philosopher(forks[i], forks[i % PHILOSOPHERS]) for i in range(PHILOSOPHERS)]
    # TODO - Start them eating and thinking
    for phil in philosophers:
        phil.start()
    for phil in philosophers:
        phil.join()
    # TODO - Display how many times each philosopher ate

    pass

if __name__ == '__main__':
    main()
