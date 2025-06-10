import unittest
from src.identifier import process_particles
from src.identifier import identify_flavor_change

# Checks for:
# - the reaction correctly identifies spectator and interacting particles

class TestProcessParticles(unittest.TestCase):
    def test_process_particles(self):
        processed_reaction = {
            'initial': ['e-', 'mu-', 'nu_mu'],
            'final': ['e-', 'nu_e', 'nu_mu']
        }

        expected_spectator = {
            'initial': ['e-', 'nu_mu'],
            'final': ['e-', 'nu_mu']
        }
        expected_interacting = {
            'initial': ['mu-'],
            'final': ['nu_e']
        }

        spectator, interacting = process_particles(processed_reaction)
        self.assertEqual(spectator, expected_spectator)
        self.assertEqual(interacting, expected_interacting)



class TestIdentifyFlavorChange(unittest.TestCase):
    def setUp(self):
        self.db = {
            'e-': {'baryon_number': 0, 
                   'family': '1e', 
                   'charge': -1,
                   'symbol': 'e-',
                   'lepton_number': 1,
                   },
            'mu-': {'baryon_number': 0, 
                    'family': '1mu',
                    'charge': -1,
                    'symbol': 'mu-',
                    'lepton_number': 1,},
            'nu_e': {'baryon_number': 0, 
                     'family': '1e',
                     'charge': 0,
                     'symbol': 'nu_e',
                     'lepton_number': 1,},
            'nu_mu': {'baryon_number': 0, 
                      'family': '1mu',
                      'charge': 0,
                      'symbol': 'nu_mu',
                      'lepton_number': 1,},
            'u': {'baryon_number': 0.3333333333333333, 
                  'family': 1,
                  'charge': 0.6666666666666666,
                  'symbol': 'u',
                  'lepton_number': 0},
            'd': {'baryon_number': 0.3333333333333333, 
                  'family': 1,
                  'charge': -0.3333333333333333,
                  'symbol': 'd',
                  'lepton_number': 0},
        }

    def test_lepton_flavor_change(self):
        interacting = {
            'initial': ['mu-', 'nu_e'],
            'final': ['e-', 'nu_mu']
        }
        interacting_expected ={
            'initial': [],
            'final': []
        }
        quark_pairs, lepton_pairs, interacting_final = identify_flavor_change(interacting, self.db)
        self.assertEqual(quark_pairs, [])
        self.assertEqual(lepton_pairs, [('mu-', 'nu_mu'), ('nu_e', 'e-')])
        self.assertEqual(interacting_final, interacting_expected)

    def test_baryon_flavor_change(self):
        interacting = {
            'initial': ['u', 'u'],
            'final': ['d', 'u']
        }
        interacting_expected = {
            'initial': ['u'],
            'final': ['u']
        }
        quark_pairs, lepton_pairs, interacting_final= identify_flavor_change(interacting, self.db)
        self.assertEqual(quark_pairs, [('u', 'd')])
        self.assertEqual(lepton_pairs, [])
        self.assertEqual(interacting_final, interacting_expected)

    def test_no_flavor_change(self):
        interacting = {
            'initial': ['e-', 'nu_mu'],
            'final': ['e-', 'nu_mu']
        }
        interacting_expected = {
            'initial': ['e-', 'nu_mu'],
            'final': ['e-', 'nu_mu']
        }
        quark_pairs, lepton_pairs, interacting_final = identify_flavor_change(interacting, self.db)
        self.assertEqual(quark_pairs, [])
        self.assertEqual(lepton_pairs, [])
        self.assertEqual(interacting_final, interacting_expected)
    
    def test_mixed_flavor_change(self):
        interacting = {
            'initial': ['u', 'e-'],
            'final': ['d', 'nu_e']
        }
        interacting_expected ={
            'initial': [],
            'final': []
        }
        quark_pairs, lepton_pairs, interacting_final = identify_flavor_change(interacting, self.db)
        self.assertEqual(quark_pairs, [('u', 'd')])
        self.assertEqual(lepton_pairs, [('e-', 'nu_e')])
        self.assertEqual(interacting_final, interacting_expected)
        

if __name__ == '__main__':
    unittest.main()