from django.test import TestCase
from .models import *
from gpt import eutils
from project import settings
import pprint


pp = pprint.PrettyPrinter(indent=4)

class ResultSetTests(TestCase):

    def test_construct_result_set(self):
        eutils.test_eutils = True

        rs = ResultSet.create_from_query("human")
        self.assertEqual(len(rs.genes), 10)
        self.assertEqual(len(rs.proteins), 14)

        settings.GPT['max_genes'] = 5
        settings.GPT['max_proteins_per_gene'] = 2
        rs = ResultSet.create_from_query("human")
        self.assertEqual(len(rs.genes), 5)
        self.assertEqual(len(rs.proteins), 6)


