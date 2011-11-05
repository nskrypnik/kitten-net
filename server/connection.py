
class Connection(object):
    '''
        Class represents connection object and stores all info about it
    '''

    def __init__(self, sock):
        self.sock = sock

    def response(self, msg):
        self.sock.send(msg)
