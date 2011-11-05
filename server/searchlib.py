# Here is the search request routing facilities

from db import db_conn
from gevent.queue import Queue

KITTEN_SEARCH_JOBS = {}

SEARCH_REQUEST_INDEX_ID = "search_request_index_id"

class SearchRequest(object):
    def __init__(self, user, need, sequence):
        self.id = db_conn.incr(SEARCH_REQUEST_INDEX_ID)
        self.need = need
        self.user = user
        self.already_searched = []

    @classmethod
    def get(self, cls, id):
        pass

def register_search_request(connection, need):
    search_request = SearchRequest(connection.user, need)
    params = {'result': 'Ok', 'request_id': search_request.id}
    connection.response({'cmd': 'search', 'params': params})
    users = connection.user.get_fiends()
    sequence = [connection.user.email]
    send_search_request(users, need, sequence, search_request)

def send_search_request(users, sequence, search_request):
    '''
        Sends requests
    '''
    for user in users:
        job_queue = KITTEN_SEARCH_JOBS.get(user)
        if job_queue and user not in search_request.already_searched:
            job_queue.put((search_request, sequence))
            search_request.already_searched.append(user)

def check_search_job(connection, job_queue):
    while 1:
        search_request, sequence = job_queue.get()
        params = {'need': search_request.need, 'request_id': search_request.id, 'sequence': sequence}
        connection.response({'cmd': 'find', 'params': params})

