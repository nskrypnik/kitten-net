#Simple test for our server

import socket
import sys
import json
import time

sys.path.append('..')

from config import PORT

try:
    #s = socket.create_connection(('46.19.34.217', PORT))
    s = socket.create_connection(('localhost', PORT))
    print 'It seeems to be ok'
except Exception as e:
    raise e

def send_msg(msg):
    s.send(json.dumps(msg))
    data = s.recv(1024)
    print data


send_msg({'cmd': 'echo', 'params': {'msg': 'hello world!'}})
send_msg({'cmd': 'register', 'params': {'email': 'bogdan1@mail.com', 'password': 'bogdan19861'}})
send_msg({'cmd': 'auth', 'params': {'email': 'bogdan1@mail.com', 'password': 'bogdan19861'}})
time.sleep(1)



