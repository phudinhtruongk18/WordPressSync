# https://www.youtube.com/watch?v=ULxMQ57engo

from wpservices.wordpess import WordpressService

import unittest
from random import randint


# Random order for tests runs. (Original is: -1 if x<y, 0 if x==y, 1 if x>y).
unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: randint(-1, 1)


def setUpModule():
    pass


def tearDownModule():
    pass



class WordpressServiceTest(unittest.TestCase):

    """Unittest."""
    
    maxDiff, __slots__ = None, ()
    
    def setUp(self):
        """Method to prepare the test fixture. Run BEFORE the test methods."""
        pass

    def tearDown(self):
        """Method to tear down the test fixture. Run AFTER the test methods."""
        pass

    def addCleanup(self, function, *args, **kwargs):
        """Function called AFTER tearDown() to clean resources used on test."""
        pass

    @classmethod
    def setUpClass(cls):
        """Class method called BEFORE tests in an individual class run. """
        pass  # Probably you may not use this one. See setUp().

    @classmethod
    def tearDownClass(cls):
        """Class method called AFTER tests in an individual class run. """
        pass  # Probably you may not use this one. See tearDown().
    
    def test_1_euqal_1(self):
        print("I did run")
        self.assertEqual(1,1)

    def test_get_token_not_return(self):
        ...

    def test_get_token_return(self):
        # token = WordpressService.get_token(domain="abc", username= "xyz", password="secret")
        # self.assertEqual(token, "token")
        ...
    
    def test_get_posts_not_return(self):
        ...

    def test_get_posts_return(self):
        ...

    def test_post_img_not_return(self):
        ...

    def test_post_img_return(self):
        ...

    def test_post_post_return(self):
        ...
        
    def test_post_post_not_return(self):
        ...
        
    def test_hide_post_return(self):
        ...

    def test_delete_post_return(self):
        ...

    def test_delete_post_not_return(self):
        ...
