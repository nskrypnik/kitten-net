#Here is the commands of our system

import sys
import hashlib

from usres import User

this_module = sys.modules[__name__]

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
    connection.response(msg)

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
    else:
        params = {'result': 'Fail', 'errormsg': 'Authentication failed'}
        connection.response({'cmd': 'auth', 'params': params})


    


