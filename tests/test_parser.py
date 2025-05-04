import unittest
from src.parser import parse_reaction


# Checks if:
# - the parser function isolates correctly all the components of the process
# - the parser function can handle whitespace

class TestParser(unittest.TestCase):
    def test_basic_parse(self):
        reaction = "e+ e- -> mu+ mu-"
        parsed = parse_reaction(reaction)
        self.assertEqual(parsed["initial"], ["e+", "e-"])
        self.assertEqual(parsed["final"], ["mu+", "mu-"])
        
    def test_whitespace(self):
        reaction = "   e+   e-   ->   mu+   mu-   "
        parsed = parse_reaction(reaction)
        self.assertEqual(parsed["initial"], ["e+", "e-"])
        self.assertEqual(parsed["final"], ["mu+", "mu-"])