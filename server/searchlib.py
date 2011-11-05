# Here is the search request routing facilities

from db import db_conn

SEARCH_REQUEST_INDEX_ID = "search_request_index_id"

class SearchRequest(object):
    def __init__(self, user, need):
        self.need = need
        self.user = user
    
    @classmethod
    def get(self, cls, id):
        pass

def register_search_request(connection, need):
    search_request = SearchRequest(connection.user, need)
    params = {'result': 'Ok', 'request_id': search_request.id}
    connection.response({'cmd': 'search', 'params': params})
