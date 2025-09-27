# Maps reactions to diagram topologies and creates TikZ diagrams

from jinja2 import Environment, FileSystemLoader
import os
import subprocess

def generate_advanced_diagram(spectator, interactions, output_dir="output/diagrams"):
    """
    Generates a Feynman diagram
    
    Args:
        spectator (dict): Dictionary with 'initial' and 'final' spectator particles
        interactions (dict): Dictionary with all identified interactions:
            - flavor_change: {'quark_pairs': [...], 'lepton_pairs': [...]}
            - strong: {'quark_pairs': [...]}
            - em: {'initial_pairs': [...], 'final_pairs': [...]}
            - weak: {'pairs': [...]}
        output_dir (str): Directory to save the output files
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "diagram.tex")
    
    # Build diagram structure
    diagram_data = {
        'spectators': spectator,            
        'interactions': interactions,       
        
        # Vertical general spacing
        'spacing': {
            'spectator': 0,
            'flavor_change': 1,
            'strong': 2,
            'em': 3,
            'weak': 4
        },
        
        # Symbols for interactions
        'symbols': {
            'flavor_change': 'W^\\pm',
            'strong': 'g',
            'em': '\\gamma',
            'weak': 'Z'
        }
    }
    
    # Environment setup
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("advanced_template.tex")
    
    # Render the template with the diagram data
    tex_output = template.render(**diagram_data)
    
    with open(output_path, "w") as f:
        f.write(tex_output)
    
    print(f"Advanced diagram saved to {output_path}")
    compile_tex(output_path)
    
    # Clean up auxiliary files
    clean_aux_files("output/diagrams", base_filename="diagram")


    
def compile_tex(tex_path):
    """Compile the .tex file into a PDF using pdflatex."""
    directory = os.path.dirname(tex_path)
    filename = os.path.basename(tex_path)
    
    try:
        subprocess.run(["lualatex", filename], cwd=directory, check=True)
        print(f"Compiled {filename} to PDF in {directory}")
    except subprocess.CalledProcessError as e:
        print("LaTeX compilation failed.")

def clean_aux_files(directory, base_filename):
    extensions = [".aux", ".log", ".out", ".fls", ".fdb_latexmk", ".toc", ".gz"]
    for ext in extensions:
        file_path = os.path.join(directory, base_filename + ext)
        if os.path.exists(file_path):
            os.remove(file_path)