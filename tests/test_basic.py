from pyspell.norvig import BasicSpellCorrector
from pkg_resources import resource_filename
import unittest
import os


class TestBasic(unittest.TestCase):

    def setUp(self):
        fname = resource_filename(__name__, "../data/en_ANC.txt.bz2")
        self.assertTrue(os.path.exists(fname))
        self.corrector = BasicSpellCorrector(fname)

    def test_suggestions(self):
        suggested = self.corrector.correct("halp", suggestions=10)
        expected = ['help', 'half', 'hall', 'halt', 'hale', 'hal', 'harp', 'halo', 'hals', 'hap']
        self.assertListEqual(suggested, expected)

    def test_single(self):
        suggested = 'mom'
        expected = 'mom'
        self.assertEqual(suggested, expected)


if __name__ == "__main__":
    unittest.run(verbose=True)
