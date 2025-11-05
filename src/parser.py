# Tokenizes and interprets user imput

import re

def parse_reaction(reaction_str):
    """
    Parses a string reaction into initial and final particles. Determines the objective of the reaction, and the steps can be deduced from it.
    It also checks for the presence of tokens like '->' or '+' to separate reactants and products.

    Args:
        reaction_str (str): input reaction string
    """    
    if '->' not in reaction_str:
        raise ValueError("Reaction string must contain '->' to separate reactants and products.")

    # Split the reaction string into reactants and products
    left, right = reaction_str.split('->')
    initial = re.findall(r'\S+', left.strip())
    final = re.findall(r'\S+', right.strip())

    return {
        'initial': initial,
        'final': final,
    }

def normalize_particles(parsed, ElementalParticles_db, ComplexParticles_db):
    """
    Normalizes a reaction by converting particle symbols or names to canonical names.
    If a particle is already given by name (i.e., it exists in the database keys), it is left unchanged.
       
    Args:
        parsed (dict): parsed reaction from the 'parse_reaction' function
        ElementalParticles_db (dict): database where keys are particle names (i.e. 'electron') and values are particle objects (from particles.py)
    """    
    
    elemental_SymbolToName = {p.symbol: name for name, p in ElementalParticles_db.items()}
    complex_SymbolToName = {p.symbol: name for name, p in ComplexParticles_db.items()}
    

    def resolve(particle_id):
        # If it's already a name in either DB, return as is
        if particle_id in ElementalParticles_db or particle_id in ComplexParticles_db:
            return particle_id
        # If it's a known symbol in elemental particles
        if particle_id in elemental_SymbolToName:
            return elemental_SymbolToName[particle_id]
        # If it's a known symbol in complex particles
        if particle_id in complex_SymbolToName:
            return complex_SymbolToName[particle_id]
        raise ValueError(f"Unknown particle: {particle_id}")

    return {
        'initial': [resolve(p) for p in parsed['initial']],
        'final': [resolve(p) for p in parsed['final']]
    }
    
def analyze_complex_particles(parsed, ComplexParticles_db, ElementalParticles_db=None):
    """
    Translates the complex particles into their elemental components.

    Args:
        parsed (dict): parsed reaction from the 'parse_reaction' function
        ComplexParticles_db (dict): database where keys are complex particle names (i.e. 'kaon-') and values are lists of elemental particles
        ElementalParticles_db (dict, optional): database of elemental particles for symbol-to-name mapping
    """
    # Create symbol-to-name mapping for elemental particles if database is provided
    symbol_to_name = {}
    if ElementalParticles_db:
        symbol_to_name = {p.symbol: name for name, p in ElementalParticles_db.items()}

    def translate(particle):
        if particle in ComplexParticles_db:
            # Use the first possible composition
            components = ComplexParticles_db[particle].content[0]
            component_list = components.split()

            # Map symbols to full names if possible
            if symbol_to_name:
                component_list = [symbol_to_name.get(comp, comp) for comp in component_list]

            return component_list
        else:
            return [particle]

    expanded_initial = []
    for p in parsed["initial"]:
        expanded_initial.extend(translate(p))
    expanded_final = []
    for p in parsed["final"]:
        expanded_final.extend(translate(p))

    return {
        "initial": expanded_initial,
        "final": expanded_final
    }
        