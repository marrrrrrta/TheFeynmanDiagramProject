import unittest
import os
from src.diagram_generator import generate_tikz
import shutil

#  Checks if:
#  - the TikZ diagram generator creates a file
#  - the generated file contains the expected particle names
#  - the generated file contains a boson

class TestDiagramGenerator(unittest.TestCase):
    def setUp(self):
        self.reaction = {
            "initial": ["electron", "positron"],
            "final": ["muon", "antimuon"]
        }
        self.output_dir = "output/diagrams"
        self.tikz_file = os.path.join(self.output_dir, "diagram.tex")
    
    def test_tikz_file_created(self):
        # Generate the TikZ diagram
        generate_tikz(self.reaction, self.output_dir)
        
        # Check if the file was created
        self.assertTrue(os.path.exists(self.tikz_file))
    
    def test_tikz_file_content(self):
        generate_tikz(self.reaction)

        with open(self.tikz_file, "r") as f:
            content = f.read()

        # Check that particle names appear in file
        self.assertIn("electron", content)
        self.assertIn("positron", content)
        self.assertIn("muon", content)
        self.assertIn("antimuon", content)
        self.assertIn("boson", content)  # to confirm a propagator is drawn

