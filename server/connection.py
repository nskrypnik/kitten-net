import json
from searchlib import KITTEN_SEARCH_JOBS, check_search_job
from db import db_conn
from gevent.queue import Queue
import gevent

class Connection(object):
    '''
        Class represents connection object and stores all info about it
    '''

    def __init__(self, sock):
        self.sock = sock
        self.user = None
        self.greenlets = []

    def response(self, msg):
        self.sock.send(json.dumps(msg))

    @property
    def authenticated(self):
        if self.user: return True
        return False

    def authenticate(self, user):
        # Lets start here all ...
        self.user = user
        this_job_queue = Queue()
        KITTEN_SEARCH_JOBS[user.id] = this_job_queue
        print "Kitten #%s init job queue" % user.id
        greenlet = gevent.spawn(check_search_job, self, this_job_queue)
        self.greenlets.append(greenlet)

    def close(self):
        ''' Do here all close conection logic '''
        for greenlet in self.greenlets:
            gevent.kill(greenlet)
