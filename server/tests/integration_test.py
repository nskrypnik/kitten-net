import gevent
from gevent import socket
from gevent import Timeout
from gevent import monkey; monkey.patch_all()

import json
import sys

sys.path.append('..')
from config import PORT

email_pass = [("ti@la", 'hello'), ("he@lo", "whatsup"), ("hi@ka", "hooka")]

def send_msg(msg, s):
    s.send(json.dumps(msg))
    data = s.recv(1024)
    print data

def kitten_test(num):
    try:
        #s = socket.create_connection(('46.19.34.217', PORT))
        s = socket.create_connection(('localhost', PORT))
        print 'It seeems to be ok', num
    except Exception as e:
        raise e

    send_msg({'cmd': 'register', 'params': {'email': email_pass[num][0],
                'password': email_pass[num][1]}}, s)

    send_msg({'cmd': 'auth', 'params': {'email': email_pass[num][0], 
                'password': email_pass[num][1]}}, s)
    if num == 2:
        friend_id = 0
    else:
        friend_id = num + 1
    send_msg({'cmd': 'add_friend', 'params': {'email': email_pass[friend_id][0]}}, s)

    gevent.sleep(num + 1)
    if num == 0:
        send_msg({'cmd': 'search', 'params': {'need': 'salo'}}, s)
        gevent.sleep(4)
    else:
        data = s.recv(1024)
        print data, "from kitten #%i" % num
        if num == 1:
            data = json.loads(data)
            params = data['params']
            send_msg({'cmd': 'search', 'params': {'request_id': params['request_id'], 
                'sequence': params['sequence'], 'need': params['need']}}, s)
        if num == 2:
            data = json.loads(data)
            request_id = data['params']['request_id']
            send_msg({'cmd': 'found', 'params': {
                                'result': {'we': 'have'},
                                'request_id': request_id
                        }}, s)


tests = [gevent.spawn(kitten_test, num) for num in range(0, 3)]
gevent.joinall(tests)
