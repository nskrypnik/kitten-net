#Simple test for our server

import socket
import sys
import json

sys.path.append('..')

from config import PORT

try:
    s = socket.create_connection(('46.19.34.217', PORT))
    print 'It seeems to be ok'
except Exception as e:
    raise e

msg = {'cmd': 'echo', 'params': {'msg': 'hello world!'}}

s.send(json.dumps(msg))

data = s.recv(1024)
print data
