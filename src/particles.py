# Loads particle data, handles lookup

import json

class ElementalParticle:
    def __init__(self, name, data):
        self.name = name
        self.symbol = data.get("symbol")
        self.LaTeX = data.get("LaTeX")
        self.mass = float(data.get("mass", 0)) 
        self.spin = float(data.get("spin", 0))
        self.charge = float(data.get("charge", 0))  
        self.baryon_number = int(data.get("baryon_number", 0))
        self.strangeness = int(data.get("strangeness", 0))
        self.charm = int(data.get("charm", 0))
        self.beauty = int(data.get("beauty", 0))
        self.truth = int(data.get("truth", 0))
        self.interactions = data.get("interactions", [])
        self.family = data.get("family")
        self.category = data.get("category")
        self.supcategory = data.get("supcategory")
    
class ComplexParticle:
    def __init__(self, name, data):
        self.name = name
        self.symbol = data.get("symbol")
        self.LaTeX = data.get("LaTeX")
        self.content = data.get("content", [])
        self.mass = float(data.get("mass", 0))
        self.spin = float(data.get("spin", 0))
        self.charge = float(data.get("charge", 0))
        self.baryon_number = int(data.get("baryon_number", 0))
        self.strangeness = int(data.get("strangeness", 0))
        self.charm = int(data.get("charm", 0))
        self.beauty = int(data.get("beauty", 0))
        self.truth = int(data.get("truth", 0))
        self.interactions = data.get("interactions", [])
        self.category = data.get("category")
        self.family = data.get("family")

    def __repr__(self):
        return f"<Particle({self.name}, (symbol={self.symbol})>"
    
def load_ElementalParticles(path = "data/ElementalParticles.json"):
    with open(path) as f:
            data = json.load(f)
    return {name: ElementalParticle(name, props) for name, props in data.items()}

def load_ComplexParticles(path = "data/ComplexParticles.json"):
    with open(path) as f:
            data = json.load(f)
    return {name: ComplexParticle(name, props) for name, props in data.items()}