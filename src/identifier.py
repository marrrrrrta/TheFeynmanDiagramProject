from collections import Counter
import re

# Identifies which interaction is happening in the reaction. For that, we need to:
# 1 - Rule out espectator particles
# 2 - Check interactions available
#   2.1 - Select interacting partibles
#   2.2 - Check flavor change
#   2.3 - Check strong, em and weak interaction in order

def process_particles(processed_reaction):
    """
    Checks which individual particles exist in both sides of the reaction and returns two lists: one with the spectator particles and one with the interacting particles.

    Args:
        processed_reaction (dict): Dictionary with 'initial' and 'final' keys containing lists of elemental particles involved.
    """
    initial = processed_reaction['initial']
    final = processed_reaction['final']
    
    spectator = [p for p in initial if p in final]
    interacting_initial = [p for p in initial if p not in spectator]
    interacting_final = [p for p in final if p not in spectator]
    
    spectator_particles ={
            'initial': spectator,
            'final': spectator
    }
    interacting_particles = {
            'initial': interacting_initial,
            'final': interacting_final
    }
    return spectator_particles, interacting_particles

def identify_flavor_change(interacting_particles, ElementalParticles_db):
    """
    Identifies if there is a flavor change in the reaction, and if it is a lepton or baryon flavor change. Returns an array with the pairs of elemental particles that change.
    
    Args:
        reaction (_type_): _description_
        ElementalParticles_db (_type_): _description_
    """
    initial = interacting_particles['initial']
    initial_copy = initial.copy()
    final = interacting_particles['final']
    final_copy = final.copy()
    
    
    quark_flavor_pairs = []
    lepton_flavor_pairs = []
    
    # Check for particle type
    def extract_type(particles):
        leptons = []
        quarks = []
        for p in particles:
            if ElementalParticles_db[p]['baryon_number'] == 0:
                leptons.append(p)
            else:
                quarks.append(p)
        return leptons, quarks

    initial_leptons, initial_quarks = extract_type(initial)
    final_leptons, final_quarks = extract_type(final)
    
    # Quarks
    used_final_quarks = set()
    for p1 in initial_quarks:
        for p2 in final_quarks:
            # For every pair of two quarks in initial and final states
            if p2 in used_final_quarks:
                # If the quark has already been used in a flavor change, skip it
                continue
            if ElementalParticles_db[p1]['baryon_number'] == ElementalParticles_db[p2]['baryon_number']:
                # Only pairs of particle/particle and antiparticle/antiparticle go through
                if ElementalParticles_db[p1]['charge'] != ElementalParticles_db[p2]['charge']:
                    # If there they have different charge, they can have a flavor change
                    if ElementalParticles_db[p1]['symbol'] != ElementalParticles_db[p2]['symbol']:
                        # If they have different symbols, they have a flavor change
                        quark_flavor_pairs.append((p1, p2))
                        used_final_quarks.add(p2)
                        if p1 in initial_copy: initial_copy.remove(p1)
                        if p2 in final_copy: final_copy.remove(p2)
                        break
    
    # Leptons
    used_final_leptons = set()
    for p1 in initial_leptons:
        for p2 in final_leptons:
            # For every pair of two leptons in initial and final states
            if p2 in used_final_leptons:
                # If the lepton has already been used in a flavor change, skip it
                continue
            if ElementalParticles_db[p1]['lepton_number'] == ElementalParticles_db[p2]['lepton_number']:
                # Only pairs of particle/particle and antiparticle/antiparticle go through
                fam1 = re.sub(r'[^a-z]', '', ElementalParticles_db[p1]['family'])
                fam2 = re.sub(r'[^a-z]', '', ElementalParticles_db[p2]['family'])
                if fam1 == fam2 and ElementalParticles_db[p1]['symbol'] != ElementalParticles_db[p2]['symbol']:
                    # If they are from the same family and have different symbols, they have a flavor change
                    lepton_flavor_pairs.append((p1, p2))
                    used_final_leptons.add(p2)
                    if p1 in initial_copy: initial_copy.remove(p1)
                    if p2 in final_copy: final_copy.remove(p2)
                    break
    
    interacting_particles = {
            'initial' : initial_copy,
            'final' : final_copy
    }
    
    return quark_flavor_pairs, lepton_flavor_pairs, interacting_particles

def identify_strong(interacting_particles, ElementalParticles_db):
    """
    Checks if the interaction is a strong interaction based on whether there's a quark particle/antiparticle pair generated in the final particles. 

    Args:
        interacting_particles (_type_): _description_
        ElementalParticles_db (_type_): _description_
    """    
    initial = interacting_particles['initial']
    final = interacting_particles['final']
    final_copy = final.copy()
    quark_pairs = []

    # Only keep quarks in final
    def is_quark(p):
        return ElementalParticles_db[p]['baryon_number'] != 0

    final_quarks = [p for p in final if is_quark(p)]
    used_final_quarks = set()

    for p1 in final_quarks:
        if p1 in used_final_quarks:
            continue
        for p2 in final_quarks:
            # For every pair of two quarks in final states
            if p2 in used_final_quarks or p1 == p2:
                # Check if they are unused
                continue
            if (
                ElementalParticles_db[p1]['baryon_number'] == -ElementalParticles_db[p2]['baryon_number']
                and abs(ElementalParticles_db[p1]['charge']) == abs(ElementalParticles_db[p2]['charge'])
                and abs(ElementalParticles_db[p1]['family']) == abs(ElementalParticles_db[p2]['family'])
            ):
                # If they are a particle/antiparticle pair, they can have a strong interaction
                quark_pairs.append((p1, p2))
                used_final_quarks.add(p1)
                used_final_quarks.add(p2)
                if p1 in final_copy: final_copy.remove(p1)
                if p2 in final_copy: final_copy.remove(p2)
                break

    interacting_particles = {
        'initial': initial,
        'final': final_copy
    }

    return quark_pairs, interacting_particles

def identify_em(interacting_particles, ElementalParticles_db):
    """
    The EM interaction is going to be studied as an interaction that joins two sets of particle/antiparticle in both sides of the equation. It will return the pairs of interacting particles distinguishing between initial and final states, and the final output will either be a vertex or a photon creation->anhilation.
    
    Checks if there is an electromagnetic interaction based on whether:
    - There are charged particles involved
    - They are the same particle type (lepton or quark)
    - Both sides have either a particle or antiparticle

    Args:
        interacting_particles (_type_): _description_
        ElementalParticles_db (_type_): _description_
    """    
    initial = interacting_particles['initial']
    final = interacting_particles['final']
    
    # Check if there are charged particles in the initial and final states    
    initial_charged = [p for p in initial if ElementalParticles_db[p]['charge'] != 0]
    final_charged = [p for p in final if ElementalParticles_db[p]['charge'] != 0]
    
    def check_pairs(particles):
        em_pairs = []
        used = set()
        for i, p1 in enumerate(particles):
            if p1 in used:
                # If the particle has already been used, skip it
                continue
            for j, p2 in enumerate(particles):
                if i == j or p2 in used:
                    # If they are the same particle or it has been already used, skip it
                    continue
                # LEPTONS
                if (
                    ElementalParticles_db[p1]['baryon_number'] == 0 and ElementalParticles_db[p2]['baryon_number'] == 0
                    and re.sub(r'[^a-z]', '', ElementalParticles_db[p1]['family']) == re.sub(r'[^a-z]', '', ElementalParticles_db[p2]['family'])
                    and ElementalParticles_db[p1]['charge'] + ElementalParticles_db[p2]['charge'] == 0
                    ):
                    # If both particles are leptons, are from the same family and their charges cancel each other
                    em_pairs.append((p1, p2))
                    used.add(p1)
                    used.add(p2)
                
                # QUARKS
                if (
                    ElementalParticles_db[p1]['baryon_number'] != 0 and ElementalParticles_db[p2]['baryon_number'] != 0
                    and abs(ElementalParticles_db[p1]['family']) == abs(ElementalParticles_db[p2]['family'])
                    and ElementalParticles_db[p1]['charge'] + ElementalParticles_db[p2]['charge'] == 0
                    ):
                    # If both particles are quarks, are from the same family and their charges cancel each other
                    em_pairs.append((p1, p2))
                    used.add(p1)
                    used.add(p2)
                    break
        
        # Look for remaining particles
        remaining = [p for p in particles if p not in used]
        return em_pairs, remaining

    initial_em, initial_remaining = check_pairs(initial_charged)
    final_em, final_remaining = check_pairs(final_charged)
    
    interacting_particles = {
        'initial': initial_remaining,
        'final': final_remaining
    }
    return initial_em, final_em, interacting_particles
        

