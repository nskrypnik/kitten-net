#Here is the commands of our system

import sys
this_module = sys.modules[__name__]

def handle_request(json_req, response):
    ''' 
        This functions calls all functions form `cmd` parameter of json request
        and pass to this functions response function to send response and
        params like kwargs
    '''
    command_name = json_req['cmd']
    params = json_req['params']
    
    _callable = getattr(this_module, command_name, None)
    _callable(response, **params)

def ping(response, msg):
    response(msg)

