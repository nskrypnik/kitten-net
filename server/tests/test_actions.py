
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
    '''
    def test_register(self):
        print "Hello"
        actions.register(connection, email='bogdan@mail.ua', password='bogdan1986')
        user = User.load("bogdan@mail.ua")
        self.assertEqual(user.email, "bogdan@mail.ua")
    
    def test_auth_not_user(self):
        print "Yo"
        actions.register(connection, email='bogdan1@mail.ua', password='bogdan19861')
        actions.auth(connection, "bogdan1@mail.ua", password='bogdan19861', token=None)
    '''

    def test_search(self):
        actions.register(connection, email='bogdan1@mail.ua', password='bogdan19861')
        actions.auth(connection, "bogdan1@mail.ua", password='bogdan19861', token=None)

        dumb_socket2 = DumbSocket()
        connection2 = Connection(dumb_socket2)
        actions.register(connection2, email='bogdan@mail.ua', password='bogdan1986')
        actions.auth(connection2, "bogdan@mail.ua", password='bogdan1986', token=None)

        dumb_socket3 = DumbSocket()
        connection3 = Connection(dumb_socket3)
        actions.register(connection3, email='bogdan2@mail.ua', password='bogdan21986')
        actions.auth(connection2, "bogdan2@mail.ua", password='bogdan21986', token=None)


        actions.add_friend(connection, email="bogdan@mail.ua")
        actions.add_friend(connection, email="bogdan2@mail.ua")

        user = User.load('bogdan1@mail.ua')
        print user.get_friends()

        actions.search(connection, need="kitten")

if __name__ == "__main__":
    unittest.main()
