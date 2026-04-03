from database import Fuels, Tanks, Engines, Tank

class RealTank(Tank):
    def __init__(self, name: str):
        for attr in ['name', 'utilization', 'densityStructure', 'densityContainer', 'effectiveDensity']: setattr(self, attr, getattr(Tanks[name], attr))

    def show(self):
        super().show()

tank = RealTank("HP Steel Fuselage")
tank.show()