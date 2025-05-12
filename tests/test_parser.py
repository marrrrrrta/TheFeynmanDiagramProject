import unittest
from src.parser import parse_reaction
from src.parser import normalize_particles, analyze_complex_particles
from src.particles import load_ComplexParticles, load_ElementalParticles


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
        
# Checks if:
# - the parser function can handle complex particles
# - the parser function can handle complex particles with whitespace

class TestComplexParser(unittest.TestCase):
    def setUp(self):
        # Load the complex particles database
        self.elemental_db = load_ElementalParticles("data/ElementalParticles.json")
        self.complex_db = load_ComplexParticles("data/ComplexParticles.json")
    
    def test_normalize_and_expand(self):
        # Example reaction: K+  n -> pi0  sigma+
        parsed_reaction = parse_reaction("K+ n -> pi0 sigma+")
        # Normalize particle names
        normalized = normalize_particles(parsed_reaction, self.elemental_db, self.complex_db)
        # Expand complex particles
        expanded = analyze_complex_particles(normalized, self.complex_db)
        
        # Expected results:
        expected_initial = ["u", "antis", "u", "d", "d"]
        expected_final = ["u", "antiu", "u", "u", "s"]
        
        self.assertEqual(expanded["initial"], expected_initial)
        self.assertEqual(expanded["final"], expected_final)
    
if __name__ == "__main__":
    unittest.main()