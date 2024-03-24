import random
import _thread

first_buf = []
second_buf = []
semaphore = False

def first_thread():
    global first_buf, second_buf, semaphore
    while True:
        semaphore = True
        for j in range(5):
            first_buf += [random.random()]
        while semaphore:
            pass
        print("first_buf:", first_buf)
        print("second_buf:", second_buf)
        first_buf, second_buf = [], []

def second_thread():
    global first_buf, second_buf, semaphore
    while True:
        while not semaphore: 
            pass
        for j in range(5):
            second_buf += [random.random()]
        semaphore = False

_thread.start_new_thread(first_thread, ())
second_thread()
