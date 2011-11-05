#Simple test for our server

import socket
import sys
import json

sys.path.append('..')

from config import PORT

try:
    s = socket.create_connection(('localhost', PORT))
    print 'It seeems to be ok'
except Exception as e:
    raise e

msg = {'hello': 'world'}

s.send(json.dumps(msg))

while 1:
    pass
