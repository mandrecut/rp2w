import time
import _thread

def first_thread():
    while True:
        print("first thread")
        time.sleep(0.5)
        print("first thread")
        time.sleep(0.5)

def second_thread():
    while True:
        time.sleep(1)
        print("second thread")

_thread.start_new_thread(first_thread, ())
second_thread()
