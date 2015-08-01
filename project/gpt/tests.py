from django.test import TestCase
from .models import *

class ResultSetTests(TestCase):

    def test_construct_result_set(self):
        rs = ResultSet()
        self.assertEqual(1, 1)
