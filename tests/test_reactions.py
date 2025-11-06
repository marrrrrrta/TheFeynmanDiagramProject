import unittest
from src.particles import load_ElementalParticles, load_ComplexParticles
from src.parser import parse_reaction, normalize_particles, analyze_complex_particles
from src.validator import validate_process


class TestReactions(unittest.TestCase):
    """Test various particle physics reactions"""

    @classmethod
    def setUpClass(cls):
        """Load particle databases once for all tests"""
        cls.elemental_db = load_ElementalParticles("data/ElementalParticles.json")
        cls.complex_db = load_ComplexParticles("data/ComplexParticles.json")

    def process_reaction(self, reaction_str):
        """Helper method to parse, normalize, and validate a reaction"""
        # Parse
        parsed = parse_reaction(reaction_str)

        # Normalize
        normalized = normalize_particles(parsed, self.elemental_db, self.complex_db)

        # Validate
        errors = validate_process(normalized, self.elemental_db, self.complex_db)

        # Analyze complex particles
        elemental = analyze_complex_particles(normalized, self.complex_db, self.elemental_db)

        return {
            'parsed': parsed,
            'normalized': normalized,
            'elemental': elemental,
            'errors': errors
        }

    def test_neutron_beta_decay(self):
        """Test: neutron + nu_e- -> proton + e-"""
        result = self.process_reaction("neutron nu_e- -> proton e-")

        # Should parse correctly
        self.assertEqual(result['parsed']['initial'], ['neutron', 'nu_e-'])
        self.assertEqual(result['parsed']['final'], ['proton', 'e-'])

        # Should normalize correctly
        self.assertEqual(result['normalized']['initial'], ['neutron', 'electron neutrino'])
        self.assertEqual(result['normalized']['final'], ['proton', 'electron'])

        # Should have no validation errors
        self.assertEqual(result['errors'], [])

    def test_tau_decay_to_electron(self):
        """Test: tau- -> e- nu_e+ nu_tau-"""
        result = self.process_reaction("tau- -> e- nu_e+ nu_tau-")

        # Should parse correctly
        self.assertEqual(result['parsed']['initial'], ['tau-'])
        self.assertEqual(result['parsed']['final'], ['e-', 'nu_e+', 'nu_tau-'])

        # Should have no validation errors
        self.assertEqual(result['errors'], [])

    def test_tau_scattering(self):
        """Test: tau- nu_tau- -> e- nu_e+"""
        result = self.process_reaction("tau- nu_tau- -> e- nu_e+")

        # Should parse correctly
        self.assertEqual(result['parsed']['initial'], ['tau-', 'nu_tau-'])
        self.assertEqual(result['parsed']['final'], ['e-', 'nu_e+'])

        # Check for validation errors (this may violate conservation laws)
        # We'll see what happens
        print(f"\ntau- nu_tau- -> e- nu_e+ errors: {result['errors']}")

    def test_proton_antiproton_annihilation(self):
        """Test: proton antiproton -> pi+ pi-"""
        result = self.process_reaction("proton antiproton -> pi+ pi-")

        # Should parse correctly
        self.assertEqual(result['parsed']['initial'], ['proton', 'antiproton'])
        self.assertEqual(result['parsed']['final'], ['pi+', 'pi-'])

        # Should have no validation errors
        self.assertEqual(result['errors'], [])

    def test_electron_positron_to_muons(self):
        """Test: e- e+ -> mu+ mu-"""
        result = self.process_reaction("e+ e- -> mu+ mu-")

        # Should parse correctly
        self.assertEqual(set(result['parsed']['initial']), {'e+', 'e-'})
        self.assertEqual(set(result['parsed']['final']), {'mu+', 'mu-'})

        # Should have no validation errors
        self.assertEqual(result['errors'], [])

    def test_sigma_decay(self):
        """Test: sigma0 -> lambda0 pi0

        Note: This decay violates mass conservation as sigma0 (1193 MeV)
        cannot decay to lambda0 (1116 MeV) + pi0 (135 MeV) = 1251 MeV.
        The physical decay is sigma0 -> lambda0 + gamma.
        """
        result = self.process_reaction("sigma0 -> lambda0 pi0")

        # Should parse correctly
        self.assertEqual(result['parsed']['initial'], ['sigma0'])
        self.assertEqual(result['parsed']['final'], ['lambda0', 'pi0'])

        # Should have mass conservation error
        self.assertTrue(len(result['errors']) > 0)
        self.assertTrue(any('mass conservation' in err for err in result['errors']))

    def test_sigma_decay_correct(self):
        """Test: sigma0 -> lambda0 gamma (correct physical decay)"""
        result = self.process_reaction("sigma0 -> lambda0 gamma")

        # Should parse correctly
        self.assertEqual(result['parsed']['initial'], ['sigma0'])
        self.assertEqual(result['parsed']['final'], ['lambda0', 'gamma'])

        # Should have no validation errors
        self.assertEqual(result['errors'], [])


if __name__ == '__main__':
    unittest.main()
