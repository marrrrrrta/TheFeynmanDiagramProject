import unittest
from src.validator import validate_process
from src.particles import load_particles
from src.parser import normalize_particles

# Checks if:
# - errors are raised when conservation laws are violated
# - no errors are raised when conservation laws are satisfied

class TestValidator(unittest.TestCase):
    def test_validate_process(self):
        particles_db = load_particles("data/particles.json")
        reaction1 = {
            "initial": ["e+", "e-"],
            "final": ["e+", "e-"]
        }
        reaction2 = {
            "initial": ["e+", "e+"],
            "final": ["μ+", "μ-"]
        }
        # Normalize both reactions first
        reaction1 = normalize_particles(reaction1, particles_db)
        reaction2 = normalize_particles(reaction2, particles_db)
        
        errors1 = validate_process(reaction1, particles_db)
        errors2 = validate_process(reaction2, particles_db)
        
        self.assertEqual(errors1, [])
        self.assertNotEqual(errors2, [])