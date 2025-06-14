# Applies conservatino laws and interaction rules

def validate_process(reaction, particles_db):
    """
    Validates the process by checking conservation laws. Such are, in order of preference:
    
    1. Electric charge (Q)
    2. Baryon number (B)
    3. Lepton number (L)
    
    The laws state that the initial property must be equal in both sides of the process. If the process is a decay, it will also check if the initial mass is greater or equal to the final mass.
    
    Args:
        reaction (???): _description_
        particles_db (???): _description_
    """    
    errors = []
    
    # Sums all the attributes of initial and final particles
    def sum_attributes(particles, attribute):
        return sum(getattr(particles_db[p], attribute) for p in particles)
    
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
    
    
    '''# 4. MASS CONSERVATION
    mass_initial = sum_attributes(reaction["initial"], "mass")
    mass_final = sum_attributes(reaction["final"], "mass")
    if mass_initial < mass_final:
        errors.append(f"Process FORBIDDEN due to mass conservation: {mass_initial} < {mass_final}")'''
    
    return errors
    
    

