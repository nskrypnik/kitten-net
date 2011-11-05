
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



if __name__ == "__main__":
    unittest.main()
