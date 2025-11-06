# Applies conservation laws and interaction rules

def validate_process(reaction, elemental_particles_db, complex_particles_db=None):
    """
    Validates the process by checking conservation laws. Such are, in order of preference:

    1. Electric charge (Q)
    2. Baryon number (B)
    3. Lepton number (L)

    The laws state that the initial property must be equal in both sides of the process. If the process is a decay, it will also check if the initial mass is greater or equal to the final mass.

    Args:
        reaction (dict): Dictionary with 'initial' and 'final' lists of particle names
        elemental_particles_db (dict): Database of elemental particles
        complex_particles_db (dict, optional): Database of complex particles
    """
    errors = []

    # Sums all the attributes of initial and final particles
    def sum_attributes(particles, attribute):
        """Sum the given attribute for all particles in the list"""
        total = 0
        for p in particles:
            # Try to find particle in either database
            if p in elemental_particles_db:
                particle = elemental_particles_db[p]
            elif complex_particles_db and p in complex_particles_db:
                particle = complex_particles_db[p]
            else:
                raise KeyError(f"Particle '{p}' not found in either database")

            if hasattr(particle, attribute):
                total += getattr(particle, attribute)
        return total
    
    # 1. ELECTRIC CHARGE CONSERVATION (Q)
    charge_initial = sum_attributes(reaction["initial"], "charge")
    charge_final = sum_attributes(reaction["final"], "charge")
    if charge_initial != charge_final:
        errors.append(f"Process FORBIDDEN due to charge conservation: {charge_initial} != {charge_final}")
    
    # 2. BARYON NUMBER CONSERVATION (B)
    baryon_initial = sum_attributes(reaction["initial"], "baryon_number")
    baryon_final = sum_attributes(reaction["final"], "baryon_number")
    if baryon_initial != baryon_final:
        errors.append(f"Process FORBIDDEN due to baryon number conservation: {baryon_initial} != {baryon_final}")
    
    # 3. LEPTON NUMBER CONSERVATION (L)
    for lepton_type in ["le_number", "lmu_number", "tau_number"]:
        lepton_initial = sum_attributes(reaction["initial"], lepton_type)
        lepton_final = sum_attributes(reaction["final"], lepton_type)
        if lepton_initial != lepton_final:
            errors.append(f"Process FORBIDDEN due to {lepton_type} conservation: {lepton_initial} != {lepton_final}")
    
    
    # 4. MASS CONSERVATION
    # Only check mass conservation if there is a single initial particle 
    if len(reaction["initial"]) == 1:
        mass_initial = sum_attributes(reaction["initial"], "mass")
        mass_final = sum_attributes(reaction["final"], "mass")  
        if mass_initial < mass_final:
            errors.append(f"Process FORBIDDEN due to mass conservation: {mass_initial} < {mass_final}")
    
    return errors
    
    

