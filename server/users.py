
from db import db_conn
import hashlib
import json

USER_INDEX_ID = "user_id_index"

class User(object):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.email = kwargs.get('email')
        raw_password = kwargs.get('password')
        md5 = hashlib.md5
        self.password = md5.hexdigest(raw_password)

    @classmethod
    def create_new(cls, email, password):
        new_user_id = db_conn.incr(USER_INDEX_ID)
        new_user = cls(email=email, password=password, id=new_user_id)
        new_user.save()
        return new_user

    @classmethod
    def load(cls, email):
        user_key = "kitten:users:%s" % email
        user_serialized = json.loads(db_conn.get(user_key))
        return cls(**user_serialized)

    @property
    def user_key(self):
        return "kitten:users:%s" % self.email

    def save(self):
        serialized = {'email': self.email, 'password': self.password, 'id': self.id}
        db_conn.set(self.user_key, json.dumps(serialized))

