# Here is the search request routing facilities

from db import db_conn
import json

KITTEN_SEARCH_JOBS = {}

SEARCH_REQUEST_INDEX_ID = "search_request_index_id"

class SearchRequest(object):
    def __init__(self, user, need, id=None):
        if not id:
            self.id = db_conn.incr(SEARCH_REQUEST_INDEX_ID)
        else:
            self.id = id

        self.need = need
        self.user = user

    def is_user_searched(self, user):
        users_set = db_conn.smembers(self.users_set_key)
        return user in users_set

    def add_user_to_searched(self, user):
        db_conn.sadd(self.users_set_key, user)

    @property
    def users_set_key(self):
        return "kitten:search_request:%i:users" % self.id

    @property
    def key(self):
        return "kitten:search_request:%i" % self.id

    @classmethod
    def get(cls, id):
        search_request_raw = db_conn.get("kitten:search_request:%i" % id)
        if search_request_raw:
            search_request = json.loads(search_request_raw)
            search_request = cls(**search_request)
            return search_request
        else:
            return None

    def save(self):
        search_request = {'user': self.user, 'need': self.need}
        db_conn.set(self.key, json.dumps(search_request))

def search(connection, need, request_id=None, sequence=[]):
    if request_id:
        search_request = SearchRequest.get(request_id)
    else:
        search_request = SearchRequest(connection.user.id, need)
        search_request.save()

    params = {'result': 'Ok', 'request_id': search_request.id}
    connection.response({'cmd': 'search', 'params': params})
    users = connection.user.get_friends()
    sequence.append(connection.user.id)
    send_search_request(users, sequence, search_request)

def send_search_request(users, sequence, search_request):
    '''
        Sends requests
    '''
    for user in users:
        job_queue = KITTEN_SEARCH_JOBS.get(int(user))
        if job_queue and not search_request.is_user_searched(user):
            job_queue.put((search_request, sequence))
            search_request.add_user_to_searched(user)

def check_search_job(connection, job_queue):
    while 1:
        print "=========== i'm here ============"
        search_request, sequence = job_queue.get()
        print 'I\'m unlocked'
        params = {'need': search_request.need, 'request_id': search_request.id, 'sequence': sequence}
        connection.response({'cmd': 'find', 'params': params})

