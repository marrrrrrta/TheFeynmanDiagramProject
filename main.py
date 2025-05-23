# Entry point (CLI or GUI launcher)

from src.particles import load_ElementalParticles, load_ComplexParticles
from src.parser import parse_reaction
from src.parser import normalize_particles
from src.parser import analyze_complex_particles
from src.validator import validate_process
from src.diagram_generator import generate_tikz

def main():
    print("This is the Feynmann Diagrams Project!")
    
    # Get the reaction string from the user
    reaction_str = input("Enter a process (e.g., e+ e- -> mu+ mu-): ")
    
    # Parse the process and divide it into 'initial' and 'final' particles
    try:
        parsed = parse_reaction(reaction_str)
    except Exception as e:
        print(f"Error parsing reaction: {e}")
        return

    # Separate the complex particles into elemental particles
    try:
        parsed = analyze_complex_particles(parsed)
    except Exception as e:
        print(f"Error analyzing complex particles: {e}")
        return

    # Load the particles database
    ElementalParticles_db = load_ElementalParticles()
    ComplexParticles_db = load_ComplexParticles()
    
    # Normalize the particles in the reaction
    try:
        normalized = normalize_particles(parsed, ElementalParticles_db, ComplexParticles_db)
    except Exception as e:
        print(f"Error normalizing particles: {e}")
        return
    
    # Validate the reaction
    errors = validate_process(normalized, ElementalParticles_db)
    if errors:
        print("This process is not allowed due to the following errors:")
        for error in errors:
            print(f"- {error}")
        return
    else:
        print("This process is allowed!")
        generate_tikz(normalized)
        print("Diagram generated successfully!")
    
if __name__ == "__main__":
    main()
        