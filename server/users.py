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
        user = User.load(email)
        if user:
            return user
        else:
            new_user_id = db_conn.incr(USER_INDEX_ID)
            new_user = cls(email=email, password=password, id=new_user_id, create_new=True)
            new_user.save()
            db_conn.set("kitten:user_by_id:%i" % new_user_id, new_user.email)
            return new_user

    @classmethod
    def load(cls, email_or_id):
        try:
            user_id = int(email_or_id)
            email = db_conn.get("kitten:user_by_id:%i" % user_id)
        except ValueError:
            email = email_or_id
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

    @property
    def friends_key(self):
        return "kitten:users:%s:friends" % self.email

    def save(self):
        serialized = {'email': self.email, 'password': self.password, 'id': self.id}
        db_conn.set(self.user_key, json.dumps(serialized))

    def update_token(self):
        token_hash = hashlib.md5("".join([self.email, str(datetime.now)]))
        self.token = token_hash.hexdigest()
    
    def get_friends(self):
        return list(db_conn.smembers(self.friends_key))

    def add_friend(self, email):
        user = User.load(email)
        db_conn.sadd(self.friends_key, user.id)

