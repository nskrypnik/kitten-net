
#Here is the commands of our system

import sys
import hashlib
from searchlib import search, SearchRequest
from connection import CONNECTIONS_POOL

from users import User

this_module = sys.modules[__name__]

def auth_required(func):
    def gen(connection, **kwargs):
        if connection.authenticated:
            func(connection, **kwargs)
        else:
            params = {'result': 'Fail', 'errormsg': 'Authentication required'}
            connection.response({'cmd': func.__name__, 'params': params})
    return gen

search = auth_required(search)

def handle_request(json_req, connection):
    ''' 
        This functions calls all functions form `cmd` parameter of json request
        and pass to this functions response function to send connection object and
        params like kwargs
    '''
    command_name = json_req['cmd']
    params = json_req['params']

    _callable = getattr(this_module, command_name, None)
    _callable(connection, **params)

def echo(connection, msg):
    print "Kitten said: %s" % msg
    params = {'msg': msg}
    connection.response({'cmd': 'echo', 'params': params})

def register(connection, **params):
    email = params['email']
    password = params['password']
    user = User.create_new(email, password)
    user.save()
    params = {'result': 'Ok', 'token': user.token}
    response_msg = {'cmd': 'register', 'params': params}
    connection.response(response_msg)

def auth(connection, email, password=None, token=None):
    user = User.load(email)
    if not user:
        params = {'result': 'Fail', 'errormsg': 'No such user'}
        connection.response({'cmd': 'auth', 'params': params})
        return
    auth_succesful = False
    if token and token == user.token:
            auth_succesful = True
    if password and hashlib.md5(password).hexdigest() == user.password:
        auth_succesful = True
    
    if auth_succesful:
        user.update_token()
        params = {'result': 'Ok', 'token': user.token}
        connection.response({'cmd': 'auth', 'params': params})
        connection.authenticate(user)
    else:
        params = {'result': 'Fail', 'errormsg': 'Authentication failed'}
        connection.response({'cmd': 'auth', 'params': params})

@auth_required
def found(connection, sequence, request_id, result):
    search_request = SearchRequest.get(request_id)
    requester_connection = CONNECTIONS_POOL.get(int(search_request.user))
    params = {'result': result, 'request_id': request_id, 'sequence': sequence}
    requester_connection.response({'cmd': 'found', 'params': params})

@auth_required
def add_friend(connection, email):
    if connection.user.add_friend(email):
        result = 'Ok'
    else: result = 'Fail'
    msg = {'cmd': 'add_friend', 'params': {'result': result}}
    connection.response(msg)
