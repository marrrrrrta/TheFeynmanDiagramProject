# Tokenizes and interprets user imput

import re

def parse_reaction(reaction_str):
    """
    Parses a string reaction into initial and final particles. Determines the objective of the reaction, and the steps can be deduced from it.

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
    
def normalize_particles(parsed, particles_db):
    """
    Maps the input particle symbols to the internal particle names using the database. 
    Creates a reverse lookup dictionary that maps particle symbols to their canonical names.

    Args:
        parsed (dict): parsed reaction from the 'parse_reaction' function
        particles_db (dict): database where keys are particle names (i.e. 'electron') and values are particle objects (from particles.py)
    """    
    
    symbol_to_name = {p.symbol: p.name for p in particles_db.values()}

    normalized_initial = []
    for p in parsed['initial']:
        name = symbol_to_name.get(p)
        print(f"Mapping symbol '{p}' to name '{name}'")
        normalized_initial.append(name)

    # Same for final
    normalized_final = [symbol_to_name.get(p) for p in parsed['final']]

    return {
        'initial': normalized_initial,
        'final': normalized_final
        }