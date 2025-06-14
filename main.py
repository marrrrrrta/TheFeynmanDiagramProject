# Entry point (CLI or GUI launcher)

from src.particles import load_ElementalParticles, load_ComplexParticles
from src.parser import parse_reaction, normalize_particles, analyze_complex_particles
from src.validator import validate_process
from src.identifier import process_particles, identify_flavor_change, identify_strong, identify_em
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

    # Load the particles database
    ElementalParticles_db = load_ElementalParticles()
    ComplexParticles_db = load_ComplexParticles()
    
    # Normalize the particles in the reaction
    try:
        normalized = normalize_particles(parsed, ElementalParticles_db, ComplexParticles_db)
    except Exception as e:
        print(f"Error normalizing particles: {e}")
        return
    
    # Analyze the complex particles in the reaction, and replace them with elemental particles
    try:
        processed_reaction = analyze_complex_particles(normalized, ComplexParticles_db)
    except Exception as e:
        print(f"Error analyzing complex particles: {e}")
        return
    
    # Validate the reaction
    errors = validate_process(processed_reaction, ElementalParticles_db)
    if errors:
        print("This process is not allowed due to the following errors:")
        for error in errors:
            print(f"- {error}")
        return
    else:
        print("This process is allowed!")
        print("We will now identify the interactions that take place in this reaction.")
        
    ## IDENTIFYING THE REACTIONS
    # 1. Separate the particles into spectator and interacting particles
    try:
        spectator_particles, interacting_particles_initial = process_particles(processed_reaction)
        print("Spectator particles:", spectator_particles)
        print("Interacting particles:", interacting_particles_initial)
    except Exception as e:
        print(f"Error processing particles: {e}")
        return
    
    # 2. Identify flavor changes
    try:
        quark_flavor_pairs, lepton_flavor_pairs, interacting_particles_flavor = identify_flavor_change(interacting_particles_initial, ElementalParticles_db)
        if quark_flavor_pairs or lepton_flavor_pairs:
            print("Flavor changes detected:", quark_flavor_pairs, lepton_flavor_pairs)
        else:
            print("No flavor changes detected.")
    except Exception as e:
        print(f"Error identifying flavor changes: {e}")
        return
    
    # 3. Identify strong interactions
    if interacting_particles_flavor:
        try: 
            quark_pairs, interacting_particles_strong = identify_strong(interacting_particles_flavor, ElementalParticles_db)
            if quark_pairs:
                print("Strong interactions detected:", quark_pairs)
            else:
                print("No strong interactions detected.")
        except Exception as e:
            print(f"Error identifying strong interactions: {e}")
            return
    
    # 4. Identify electromagnetic interactions
    if interacting_particles_strong:
        try:
            initial_em, final_em, interacting_particles_em = identify_em(interacting_particles_strong, ElementalParticles_db)
            if initial_em or final_em:
                em_pairs = [(i, f) for i in initial_em for f in final_em]
                print("Electromagnetic interactions detected:", em_pairs)
            else:
                print("No electromagnetic interactions detected.")
        except Exception as e:
            print(f"Error identifying electromagnetic interactions: {e}")
            return
        
    # Ask whether to generate a diagram
    generate_diagram = input("Do you want to generate a Feynman diagram? (yes/no): ").strip().lower()
    if generate_diagram in ['yes', 'y']:
        try:
            tikz_code = generate_tikz(processed_reaction, ElementalParticles_db, ComplexParticles_db)
            print("Feynman diagram generated successfully!")
            print(tikz_code)
        except Exception as e:
            print(f"Error generating Feynman diagram: {e}")
    else:
        print("No diagram generated.")
    
if __name__ == "__main__":
    main()
        