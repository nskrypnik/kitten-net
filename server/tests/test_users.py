
import unittest
import sys
sys.path.append('..')

from users import User

class UsersTest(unittest.TestCase):

    def test_create_user(self):
        user = User.create_new("niko@gmail.com", "hello")
        user.save()

    def test_load_user(self):
        user = User.load("niko@gmail.com")
        self.assertEqual(user.email, "niko@gmail.com")
        print user.password

if __name__ == "__main__":
    unittest.main()

