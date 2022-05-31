"""
Day simulation with FSM
"""
# pylint:disable=method-hidden
from random import random


def prime(func):
    """
    create generators
    """
    def wrapper(*args, **kwargs):
        generator = func(*args, **kwargs)
        generator.send(None)
        return generator
    return wrapper


class FSM:
    """
    FINIT STATE MACHINE
    """

    def __init__(self):
        """
        Init state
        """
        self.start = self.start()
        self.sleep = self.sleep()
        self.study = self.study()
        self.eat = self.eat()
        self.relax = self.relax()
        self.day_sleep = self.day_sleep()
        self.current_state = self.start
        self.stopped = False

    def trace_time(self, time):
        """
        send time value to state
        """
        try:
            self.current_state.send(time)
        except StopIteration:
            self.stopped = True

    @prime
    def start(self):
        """
        start state
        """
        while True:
            yield
            if random() < 0.5:
                print('GM. It is time to have a breakfast')
                self.current_state = self.eat
            else:
                yield
                print('Here we go again. Seems like there is no time for eating...')
                self.current_state = self.study

    @prime
    def eat(self):
        """
        eat state
        """
        while True:
            time = yield
            print(f"eat at {time}")
            if time == 8 and random() < 0.2:
                print('Oh... seems that there is no work to do. You can relax')
                self.current_state = self.relax
            elif time in [8, 15, 20]:
                self.current_state = self.study

    @prime
    def sleep(self):
        """
        sleep state
        """
        while True:
            time = yield
            print(f'Slepping at {time%24}')
            if time > 32:
                self.stopped = True

    @prime
    def day_sleep(self):
        """
        dayly sleep state
        """
        while True:
            time = yield
            print(f'dayly slepp at {time}')
            if time == 19:
                print('Time to get up !')
                self.current_state = self.eat

    @prime
    def study(self):
        """
        study state
        """
        while True:
            time = yield
            print(f'studying at {time%24}')
            if time in [14, 19]:
                self.current_state = self.eat
            elif time == 17:
                if random() < .5:
                    self.current_state = self.relax
                else:
                    self.current_state = self.day_sleep
            elif time == 22:
                if random() < 0.5:
                    self.current_state = self.relax
                else:
                    print('Looks like there is a new deadline... Keep studying!')

            elif time >= 24:
                probab = 2/(29 - time)
                if random() < probab:
                    print('Well done. Now You can go to sleep')
                    self.current_state = self.sleep

    @prime
    def relax(self):
        """
        Relax state
        """
        while True:
            time = yield
            print(f'Relaxing at {time}')
            if time in [14, 19]:
                self.current_state = self.eat
            elif time == 24:
                print("Ohh.. It is late. Time to sleep ...")
                self.current_state = self.sleep


def main():
    """
    Main function
    """
    cycle = FSM()
    print('--- START A NEW DAY ---')
    for time in range(7, 32):
        cycle.trace_time(time)
        if cycle.stopped:
            break
    print('What a nice day.\n--- END OF THE DAY ---')


main()
