import sys
import json

while True:
    message = sys.stdin.readline().strip()
    if message:
        message = json.loads(message)
        print({"host": message["host"], 
               "device": "Hello host!"})
