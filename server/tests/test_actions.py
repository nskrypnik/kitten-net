
import unittest
import sys

sys.path.append('..')

import actions
from connection import Connection
from users import User

class DumbSocket(object):

    def __init__(self):
        pass
    
    def send(self, msg):
        print msg
    

dumb_socket = DumbSocket()
connection = Connection(dumb_socket)

class CommandsTest(unittest.TestCase):

    def test_register(self):
        print "Hello"
        actions.register(connection, email='bogdan@mail.ua', password='bogdan1986')
        user = User.load("bogdan@mail.ua")
        self.assertEqual(user.email, "bogdan@mail.ua")

    def test_auth_not_user(self):
	print "Yo"
	actions.register(connection, email='bogdan1@mail.ua', password='bogdan19861')
	actions.auth(connection, "bogdan@mail.ua", password='bogdan19861', token=None)
	params = connection.authenticate(user)
	self.assertEqual(params, 'Fail')

if __name__ == "__main__":
    unittest.main()	