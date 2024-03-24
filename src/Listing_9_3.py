import time
import random
import _thread

buf = []

def first_thread():
    global buf
    while True:
        lock.acquire()
        for j in range(5):
            buf += [random.random()]
        lock.release()

def second_thread():
    global buf
    while True:
        if lock.acquire():
            print(buf)
            buf = []
            lock.release()

lock = _thread.allocate_lock()
_thread.start_new_thread(first_thread, ())
second_thread()
