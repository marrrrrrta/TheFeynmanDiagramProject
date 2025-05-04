import unittest
from src.parser import normalize_particles
from src.particles import load_particles

# Checks if:
# - the parsed reaction is normalized correctly

class TestNormalizer(unittest.TestCase):
    def test_normalize_particles(self):
        db = load_particles()
        reaction = {
            "initial": ["e+", "e-"],
            "final": ["μ+", "μ-"]
        }
        normalized = normalize_particles(reaction, db)
        self.assertEqual(normalized["initial"], ["positron", "electron"])
        self.assertEqual(normalized["final"], ["antimuon", "muon"])
        