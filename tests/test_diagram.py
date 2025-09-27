#!/usr/bin/env python3
# filepath: /Users/martadelarosanunez/Documents/TheFeynmanDiagramProject/test_diagram.py

import os
import sys
from src.diagram_generator import generate_advanced_diagram

def test_simple_em_interaction():
    """Test diagram generation for e+ e- -> mu+ mu-"""
    # Mock data
    spectator = {
        'initial': [],
        'final': []
    }
    
    interactions = {
        'flavor_change': {
            'quark_pairs': [],
            'lepton_pairs': []
        },
        'strong': {
            'quark_pairs': []
        },
        'em': {
            'initial_pairs': [('electron', 'positron')],
            'final_pairs': [('muon', 'antimuon')]
        },
        'weak': {
            'pairs': []
        }
    }
    
    output_dir = "output/diagrams/test_em"
    
    # Generate the diagram
    generate_advanced_diagram(spectator, interactions, output_dir)
    
    # Check if files were created
    pdf_path = os.path.join(output_dir, "diagram.pdf")
    if os.path.exists(pdf_path):
        print(f"✓ Success: PDF generated at {pdf_path}")
        # Optionally open the PDF on macOS
        # os.system(f"open {pdf_path}")
    else:
        print(f"✗ Error: PDF not generated at {pdf_path}")

def test_flavor_change():
    """Test diagram with flavor change: mu- -> e- ve vmu"""
    print("Testing flavor change: mu- -> e- ve vmu")
    
    spectator = {
        'initial': [],
        'final': []
    }
    
    interactions = {
        'flavor_change': {
            'quark_pairs': [],
            'lepton_pairs': [('muon', 'electron')]
        },
        'strong': {
            'quark_pairs': []
        },
        'em': {
            'initial_pairs': [],
            'final_pairs': []
        },
        'weak': {
            'pairs': []
        }
    }
    
    output_dir = "output/diagrams/test_flavor"
    generate_advanced_diagram(spectator, interactions, output_dir)
    
    pdf_path = os.path.join(output_dir, "diagram.pdf")
    if os.path.exists(pdf_path):
        print(f"✓ Success: PDF generated at {pdf_path}")
    else:
        print(f"✗ Error: PDF not generated at {pdf_path}")

def test_with_spectators():
    """Test diagram with spectator particles"""
    print("Testing with spectator particles")
    
    spectator = {
        'initial': ['photon', 'gluon'],
        'final': ['photon', 'gluon']
    }
    
    interactions = {
        'flavor_change': {'quark_pairs': [], 'lepton_pairs': []},
        'strong': {'quark_pairs': [('up', 'antiup')]},
        'em': {'initial_pairs': [], 'final_pairs': []},
        'weak': {'pairs': []}
    }
    
    output_dir = "output/diagrams/test_spectators"
    generate_advanced_diagram(spectator, interactions, output_dir)
    
    pdf_path = os.path.join(output_dir, "diagram.pdf")
    if os.path.exists(pdf_path):
        print(f"✓ Success: PDF generated at {pdf_path}")
    else:
        print(f"✗ Error: PDF not generated at {pdf_path}")

def test_complex_scenario():
    """Test a complex diagram with multiple interaction types"""
    print("Testing complex scenario with multiple interactions")
    
    spectator = {
        'initial': ['photon'],
        'final': ['photon']
    }
    
    interactions = {
        'flavor_change': {
            'quark_pairs': [('up', 'down')],
            'lepton_pairs': []
        },
        'strong': {
            'quark_pairs': [('up', 'antiup')]
        },
        'em': {
            'initial_pairs': [('electron', 'positron')],
            'final_pairs': []
        },
        'weak': {
            'pairs': [('neutrino', 'antimuon')]
        }
    }
    
    output_dir = "output/diagrams/test_complex"
    generate_advanced_diagram(spectator, interactions, output_dir)
    
    pdf_path = os.path.join(output_dir, "diagram.pdf")
    if os.path.exists(pdf_path):
        print(f"✓ Success: PDF generated at {pdf_path}")
    else:
        print(f"✗ Error: PDF not generated at {pdf_path}")

if __name__ == "__main__":
    # Run all tests by default
    if len(sys.argv) == 1:
        test_simple_em_interaction()
        test_flavor_change()
        test_with_spectators()
        test_complex_scenario()
    else:
        # Run specific test based on command line argument
        test_name = sys.argv[1]
        if test_name == "em":
            test_simple_em_interaction()
        elif test_name == "flavor":
            test_flavor_change()
        elif test_name == "spectators":
            test_with_spectators()
        elif test_name == "complex":
            test_complex_scenario()
        else:
            print(f"Unknown test: {test_name}")
            print("Available tests: em, flavor, spectators, complex")