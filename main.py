
from src.particles import load_ElementalParticles, load_ComplexParticles
from src.parser import parse_reaction, normalize_particles, analyze_complex_particles
from src.validator import validate_process
from src.identifier import (
    process_particles,
    identify_flavor_change,
    identify_strong,
    identify_em,
    identify_weak
)
from src.diagram_generator import generate_advanced_diagram

def main():
    print("Welcome to the Feynman Diagrams Project!")

    ## Step 1: Parse the reaction
    reaction_str = input("Enter a process (e.g., e+ e- -> mu+ mu-): ")
    try:
        parsed_reaction = parse_reaction(reaction_str)
    except Exception as e:
        print(f"Error parsing reaction: {e}")
        return

    ## Step 2: Normalize particles
    # Load databases
    ElementalParticles_db = load_ElementalParticles()
    ComplexParticles_db = load_ComplexParticles()
    try:
        normalized_reaction = normalize_particles(parsed_reaction, ElementalParticles_db, ComplexParticles_db)
    except Exception as e:
        print(f"Error normalizing particles: {e}")
        return

    ## Step 3: Validate the reaction
    try:
        errors = validate_process(normalized_reaction, ElementalParticles_db)
        if errors:
            print("The reaction is not valid due to the following errors:")
            for error in errors:
                print(f"- {error}")
            return
        else:
            print("This process is allowed!")
            print("We will now identify the interactions that take place in this reaction.")
    except Exception as e:
        print(f"Validation error: {e}")
        return

    ## Step 4: Analyze complex particles (break into elemental)
    try:
        elemental_reaction = analyze_complex_particles(normalized_reaction, ComplexParticles_db)
    except Exception as e:
        print(f"Error analyzing complex particles: {e}")
        return

    ## Step 5: Identify interactions
    print("Identifying interactions...")

    # 5.1 Process particles (group interacting/spectator)
    spectator, interacting = process_particles(elemental_reaction)
    updated_interacting = interacting.copy()
    interactions_found = []

    # 5.2 Check for flavor change
    quark_flavor_pairs, lepton_flavor_pairs, updated_interacting = identify_flavor_change(interacting, ElementalParticles_db)
    if quark_flavor_pairs or lepton_flavor_pairs:
        print("Flavor-changing interactions detected:")
        if quark_flavor_pairs:
            print(f"Quark flavor pairs: {quark_flavor_pairs}")
        if lepton_flavor_pairs:
            print(f"Lepton flavor pairs: {lepton_flavor_pairs}")
    
    # 5.3 Check strong interaction
    if updated_interacting['initial'] or updated_interacting['final']:
        quark_pairs, updated_interacting = identify_strong(updated_interacting, ElementalParticles_db)
        if quark_pairs:
            print(f"Strong interaction quark pairs: {quark_pairs}")
    
    # 5.4 Check electromagnetic interaction
    if updated_interacting['initial'] or updated_interacting['final']:
        initial_em, final_em, updated_interacting = identify_em(updated_interacting, ElementalParticles_db)
        if initial_em or final_em:
            print(f"Electromagnetic interaction particles: Initial: {initial_em}, Final: {final_em}")
    
    # 5.5 Check weak interaction
    if updated_interacting['initial'] or updated_interacting['final']:
        weak_pairs, updated_interacting = identify_weak(updated_interacting, ElementalParticles_db)
        if weak_pairs:
            print(f"Weak interaction pairs: {weak_pairs}")
    
    if updated_interacting['initial'] or updated_interacting['final']:
        print("Remaining particles after interaction identification:")
        print(f"Initial: {updated_interacting['initial']}, Final: {updated_interacting['final']}")

    # Step 6: Generate diagram
    interactions = {
        'flavor_change': {
            'quark_pairs': quark_flavor_pairs,
            'lepton_pairs': lepton_flavor_pairs
        },
        'strong': {
            'quark_pairs': quark_pairs
        },
        'em': {
            'initial_pairs': initial_em,
            'final_pairs': final_em
        },
        'weak': {
            'pairs': weak_pairs
        }
    }
    
    generation = input("Do you want to generate a Feynman diagram? (yes/no): ").strip().lower()
    if generation == 'yes':
        try:
            generate_advanced_diagram(spectator, interactions, output_dir="output/diagrams")
            print("Feynman diagram generated successfully!")
        except Exception as e:
            print(f"Error generating diagram: {e}")
    else:
        print("Diagram generation skipped.")

if __name__ == "__main__":
    main()