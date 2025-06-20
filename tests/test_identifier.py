import unittest
from src.particles import load_ElementalParticles

from src.identifier import process_particles
from src.identifier import identify_flavor_change
from src.identifier import identify_strong
from src.identifier import identify_em
from src.identifier import identify_weak

# Checks for:
# - the reaction correctly identifies spectator and interacting particles

class TestProcessParticles(unittest.TestCase):
    def test_process_particles(self):
        processed_reaction = {
            'initial': ['electron', 'muon', 'muon neutrino'],
            'final': ['electron', 'electron neutrino', 'muon neutrino']
        }

        expected_spectator = {
            'initial': ['electron', 'muon neutrino'],
            'final': ['electron', 'muon neutrino']
        }
        expected_interacting = {
            'initial': ['muon'],
            'final': ['electron neutrino']
        }

        spectator, interacting = process_particles(processed_reaction)
        self.assertEqual(spectator, expected_spectator)
        self.assertEqual(interacting, expected_interacting)



class TestIdentifyFlavorChange(unittest.TestCase):
    def setUp(self):
        self.db = load_ElementalParticles("data/ElementalParticles.json")

    def test_lepton_flavor_change(self):
        interacting = {
            'initial': ['muon', 'electron neutrino'],
            'final': ['electron', 'muon neutrino']
        }
        interacting_expected ={
            'initial': [],
            'final': []
        }
        quark_pairs, lepton_pairs, interacting_final = identify_flavor_change(interacting, self.db)
        self.assertEqual(quark_pairs, [])
        self.assertEqual(lepton_pairs, [('muon', 'muon neutrino'), ('electron neutrino', 'electron')])
        self.assertEqual(interacting_final, interacting_expected)

    def test_baryon_flavor_change(self):
        interacting = {
            'initial': ['up', 'up'],
            'final': ['down', 'up']
        }
        interacting_expected = {
            'initial': ['up'],
            'final': ['up']
        }
        quark_pairs, lepton_pairs, interacting_final= identify_flavor_change(interacting, self.db)
        self.assertEqual(quark_pairs, [('up', 'down')])
        self.assertEqual(lepton_pairs, [])
        self.assertEqual(interacting_final, interacting_expected)

    def test_no_flavor_change(self):
        interacting = {
            'initial': ['electron', 'muon neutrino'],
            'final': ['electron', 'muon neutrino']
        }
        interacting_expected = {
            'initial': ['electron', 'muon neutrino'],
            'final': ['electron', 'muon neutrino']
        }
        quark_pairs, lepton_pairs, interacting_final = identify_flavor_change(interacting, self.db)
        self.assertEqual(quark_pairs, [])
        self.assertEqual(lepton_pairs, [])
        self.assertEqual(interacting_final, interacting_expected)
    
    def test_mixed_flavor_change(self):
        interacting = {
            'initial': ['up', 'electron'],
            'final': ['down', 'electron neutrino']
        }
        interacting_expected ={
            'initial': [],
            'final': []
        }
        quark_pairs, lepton_pairs, interacting_final = identify_flavor_change(interacting, self.db)
        self.assertEqual(quark_pairs, [('up', 'down')])
        self.assertEqual(lepton_pairs, [('electron', 'electron neutrino')])
        self.assertEqual(interacting_final, interacting_expected)
        
'''class TestIdentifyStrong(unittest.TestCase):
    def setUp(self):
        self.db = load_ElementalParticles("data/ElementalParticles.json")
        
    def test_basic_strong(self):
        interacting = {
            'initial': ['up', 'down'],
            'final': ['antiup', 'down', 'up']
        }
        interacting_expected = {
            'initial': ['up', 'down'],
            'final': ['down']
        }
        quark_pairs, interacting_final = identify_strong(interacting, self.db)
        self.assertEqual(quark_pairs, [('antiup', 'up')])
        self.assertEqual(interacting_final, interacting_expected)
    
    def test_no_strong(self):
        interacting = {
            'initial': ['up', 'down'],
            'final': ['up', 'down']
        }
        interacting_expected = {
            'initial': ['up', 'down'],
            'final': ['up', 'down']
        }
        quark_pairs, interacting_final = identify_strong(interacting, self.db)
        self.assertEqual(quark_pairs, [])
        self.assertEqual(interacting_final, interacting_expected)
    
    def test_no_strong_with_antiparticles(self):
        interacting = {
            'initial': ['up', 'down'],
            'final': ['antiup', 'antidown']
        }
        interacting_expected = {
            'initial': ['up', 'down'],
            'final': ['antiup', 'antidown']
        }
        quark_pairs, interacting_final = identify_strong(interacting, self.db)
        self.assertEqual(quark_pairs, [])
        self.assertEqual(interacting_final, interacting_expected)
        
        
class TestIdentifyEM(unittest.TestCase):
    def setUp(self):
        self.db = load_ElementalParticles("data/ElementalParticles.json")
    
    def test_basic_em(self):
        interacting = {
            'initial': ['electron', 'positron'],
            'final': ['positron', 'antiup']
        }
        interacting_expected = {
            'initial': [],
            'final': ['positron','antiup']
        }
        initial_em, final_em, interacting_particles = identify_em(interacting, self.db)
        self.assertEqual(initial_em, [('electron', 'positron')])
        self.assertEqual(final_em, [])
        self.assertEqual(interacting_particles, interacting_expected)
    
    def no_em(self):
        interacting = {
            'initial': ['electron', 'electron'],
            'final': ['positron', 'positron']
        }
        interacting_expected = {
            'initial': ['electron', 'electron'],
            'final': ['positron', 'positron']
        }
        initial_em, final_em, interacting_particles = identify_em(interacting, self.db)
        self.assertEqual(initial_em, [])
        self.assertEqual(final_em, [])
        self.assertEqual(interacting_particles, interacting_expected)
 
class TestIdentifyWeak(unittest.TestCase):    
    def setUp(self):
        self.db = load_ElementalParticles("data/ElementalParticles.json")
        
    def test_basic_weak(self):
        interacting = {
            'initial': ['electron', 'up'],
            'final': ['electron', 'antiup']
        }
        interacting_expected = {
            'initial': ['up'],
            'final': ['antiup']
        }
        weak_pairs, interacting_particles = identify_weak(interacting, self.db)
        self.assertEqual(weak_pairs, [('electron', 'electron')])
        self.assertEqual(interacting_particles, interacting_expected)
    
    def test_no_weak(self):
        interacting = {
            'initial': ['electron', 'antiup'],
            'final': ['positron', 'up']
        }
        interacting_expected = {
            'initial': ['electron', 'antiup'],
            'final': ['positron', 'up']
        }
        weak_pairs, interacting_particles = identify_weak(interacting, self.db)
        self.assertEqual(weak_pairs, [])
        self.assertEqual(interacting_particles, interacting_expected)'''

if __name__ == '__main__':
    unittest.main()