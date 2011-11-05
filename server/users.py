from db import db_conn
import hashlib
from datetime import datetime
import json

USER_INDEX_ID = "user_id_index"

class User(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.email = kwargs.get('email')
        raw_password = kwargs.get('password')
        if kwargs.get('create_new'):
            password_hash = hashlib.md5(raw_password)
            self.password = password_hash.hexdigest()
        else:
            self.password = raw_password
        self.update_token()

    @classmethod
    def create_new(cls, email, password):
        user = User.load(email=email)
        if user:
            return user
        else:
            new_user_id = db_conn.incr(USER_INDEX_ID)
            new_user = cls(email=email, password=password, id=new_user_id, create_new=True)
            new_user.save()
            return new_user

    @classmethod
    def load(cls, email):
        user_key = "kitten:users:%s" % email
        user_db_string = db_conn.get(user_key)
        if user_db_string:
            user_serialized = json.loads(user_db_string)
            return cls(**user_serialized)
        else:
            return None

    @property
    def user_key(self):
        return "kitten:users:%s" % self.email

    def save(self):
        serialized = {'email': self.email, 'password': self.password, 'id': self.id}
        db_conn.set(self.user_key, json.dumps(serialized))

    def update_token(self):
        token_hash = hashlib.md5("".join([self.email, str(datetime.now)]))
        self.token = token_hash.hexdigest()

