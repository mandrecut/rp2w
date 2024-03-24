import time
import _thread

def first_thread():
    while True:
        lock.acquire()
        print("first thread")
        time.sleep(0.5)
        lock.release()

def second_thread():
    while True:
        lock.acquire()
        time.sleep(1)
        print("second thread")
        lock.release()

lock = _thread.allocate_lock()
_thread.start_new_thread(first_thread, ())
second_thread()
