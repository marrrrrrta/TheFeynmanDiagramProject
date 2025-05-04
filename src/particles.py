# Loads particle data, handles lookup

import json

class Particle:
    def __init__(self, name, data):
        self.name = name
        self.symbol = data.get("symbol")
        self.mass = float(data.get("mass", 0)) # Always cast to float
        self.charge = float(data.get("charge", 0))  
        self.spin = float(data.get("spin", 0))
        self.lepton_number = data.get("lepton_number", 0)
        self.baryon_number = int(data.get("baryon_number", 0))
        self.interactions = data.get("interactions", [])
        self.type = data.get("type")

    def __repr__(self):
        return f"<Particle({self.name}, (symbol={self.symbol})>"
    
def load_particles(path = "data/particles.json"):
    with open(path) as f:
            data = json.load(f)
    return {name: Particle(name, props) for name, props in data.items()}