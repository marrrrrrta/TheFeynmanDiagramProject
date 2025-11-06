import unittest
from src.validator import validate_process
from src.particles import load_ElementalParticles, load_ComplexParticles
from src.parser import normalize_particles

# Checks if:
# - errors are raised when conservation laws are violated
# - no errors are raised when conservation laws are satisfied

class TestValidator(unittest.TestCase):
    def test_validate_process(self):
        elemental_db = load_ElementalParticles("data/ElementalParticles.json")
        complex_db = load_ComplexParticles("data/ComplexParticles.json")
        reaction1 = {
            "initial": ["e+", "e-"],
            "final": ["e+", "e-"]
        }
        reaction2 = {
            "initial": ["e+", "e+"],
            "final": ["mu+", "mu-"]
        }
        # Normalize both reactions first
        reaction1 = normalize_particles(reaction1, elemental_db, complex_db)
        reaction2 = normalize_particles(reaction2, elemental_db, complex_db)
        
        errors1 = validate_process(reaction1, elemental_db, complex_db)
        errors2 = validate_process(reaction2, elemental_db, complex_db)
        
        self.assertEqual(errors1, [])
        self.assertNotEqual(errors2, [])