# Entry point (CLI or GUI launcher)

from src.particles import load_ElementalParticles
from src.parser import parse_reaction
from src.parser import normalize_particles
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

    # Load the particles databasee+
    particles_db = load_ElementalParticles()
    
    # Normalize the particles in the reaction
    try:
        normalized = normalize_particles(parsed, particles_db)
    except Exception as e:
        print(f"Error normalizing particles: {e}")
        return
    
    # Validate the reaction
    errors = validate_process(normalized, particles_db)
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
        