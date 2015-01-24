from unittest import TestCase

__author__ = 'John Sonneville'


class TestApp(TestCase):
    def __init__(self, method_name='runTest'):
        super().__init__(method_name)

    def setUpModule(self):
        pass

    def tearDownModule(self):
        pass