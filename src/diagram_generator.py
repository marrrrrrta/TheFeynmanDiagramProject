# Maps reactions to diagram topologies and creates TikZ diagrams

from jinja2 import Environment, FileSystemLoader
import os
import subprocess

def generate_tikz(reaction, output_dir = "output/diagrams"):
    """
    Generates a TikZ diagram for the given reaction and saves it to the specified output path.
    
    Args:
        reaction (dict): The reaction data containing initial and final particles.
        output_path (str): The path where the TikZ diagram will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "diagram.tex")


    initial = reaction["initial"]
    final = reaction["final"]
    
    # simple model, two initial particles per side max
    data = {
        "initial1": initial[0],
        "initial2": initial[1] if len(initial) > 1 else "",
        "final1": final[0],
        "final2": final[1] if len(final) > 1 else "",
        "exchange": r"\gamma or $Z$"  # Placeholder for exchange particle
    }
    
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("feynman_template.tex")
    
    tex_output = template.render(initial=reaction["initial"], final=reaction["final"])
    output_path = os.path.join(output_dir, "diagram.tex") 
    
    with open(output_path, "w") as f:
        f.write(tex_output)
    
    print(f"Diagram saved to {output_path}")
    compile_tex(output_path)
    
    # Clean up auxiliary files
    clean_aux_files("output/diagrams", base_filename="diagram")
    clean_aux_files("templates", base_filename="feynman_template")


    
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