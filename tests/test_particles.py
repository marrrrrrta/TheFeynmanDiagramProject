import unittest
from src.particles import load_particles

# Checks if:
# - the load_particles function loads the particle data correctly
# - the loaded data contains expected attributes

class TestParticles(unittest.TestCase):
    def test_load_particles(self):
        db = load_particles("data/particles.json")
        self.assertIn("electron", db)
        self.assertTrue(hasattr(db["electron"], "mass"))