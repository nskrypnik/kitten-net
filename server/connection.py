import json
from db import db_conn

class Connection(object):
    '''
        Class represents connection object and stores all info about it
    '''

    def __init__(self, sock):
        self.sock = sock
        self.user = None

    def response(self, msg):
        self.sock.send(json.dumps(msg))

    @property
    def authenticated(self):
        if self.user: return True
        return False

    def authenticate(self, user):
        self.user = user
