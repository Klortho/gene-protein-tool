from django.test import TestCase
from .models import *
from gpt import eutils
from project import settings
import pprint


pp = pprint.PrettyPrinter(indent=4)



class ResultSetTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', '', 'user1')

    def test_construct_result_set(self):
        eutils.test_eutils = True

        rs = ResultSet.create_from_query("human", self.user1)
        self.assertEqual(len(rs.genes.all()), 10)

        g0 = rs.genes.all()[0]
        self.assertEqual(g0.uid, 106099058)

        g0_ps = g0.protein_set.all()
        self.assertEqual(len(g0_ps), 1)





