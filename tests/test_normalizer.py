import unittest
from src.parser import normalize_particles
from src.particles import load_ElementalParticles, load_ComplexParticles

# Checks if:
# - the parsed reaction is normalized correctly

class TestNormalizer(unittest.TestCase):
    def test_normalize_particles(self):
        elemental_db = load_ElementalParticles()
        complex_db = load_ComplexParticles()
        reaction = {
            "initial": ["e+", "e-"],
            "final": ["mu+", "mu-"]
        }
        normalized = normalize_particles(reaction, elemental_db, complex_db)
        self.assertEqual(normalized["initial"], ["positron", "electron"])
        self.assertEqual(normalized["final"], ["antimuon", "muon"])
        