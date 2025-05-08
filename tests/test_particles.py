import unittest
from src.particles import load_ElementalParticles
from src.particles import load_ComplexParticles

# Checks if:
# - the load_ElementalParticles function loads the particle data correctly
# - the loaded data contains expected attributes

class TestElementalParticles(unittest.TestCase):
    def test_load_ElementalParticles(self):
        db = load_ElementalParticles("data/particles.json")
        self.assertIn("electron", db)
        self.assertTrue(hasattr(db["electron"], "mass"))

class TestComplexParticles(unittest.TestCase):
    def test_load_ComplexParticles(self):
        db = load_ComplexParticles("data/particles.json")
        self.assertIn("proton", db)
        self.assertTrue(hasattr(db["proton"], "mass"))
        self.assertTrue(hasattr(db["proton"], "content"))