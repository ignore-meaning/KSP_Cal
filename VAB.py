from database import G, Fuels, RealTank, Engines

class Stage:
    def __init__(self, num: int, tankName: str, engineList: list[tuple[str, int]]):
        self.num = num
        self.tank = RealTank(tankName)
        self.engines = [(Engines[engineName], n) for engineName, n in engineList]
        self.massStructure = 0
        self.netMass = 0
        self.wetMass = 0
        self.burnTime = 0
        self.maxThrust = sum(engine.maxThrust * n for engine, n in self.engines)

    def setMassStructure(self, massStructure: float):
        self.massStructure = massStructure

    def autoFill(self):
        self.burnTime = min(engine.ratedBurnTime for engine in [engine for engine, n in self.engines]) + 5
        self.tank.fillFuel(self.engines, self.burnTime)
        self.netMass = self.massStructure + self.tank.netMass + sum(engine.mass * n for engine, n in self.engines)
        self.wetMass = self.netMass - self.tank.netMass + self.tank.wetMass

    def info(self):
        info = [f"Stage num: \t\t{self.num}",
                f"Tank Name: \t\t{self.tank.name}",
                f"Stage Wet Mass: \t{self.wetMass:.4g} kg",
                f"Stage Net Mass: \t{self.netMass:.4g} kg",
                f"Stage Burn Time: \t{self.burnTime:.4g} s",
                f"Stage Max Thrust: \t{self.maxThrust:.4g} kN",]
        info += [f"\t{f'{fuelName}:':15} {self.tank.fuel[fuelName]:.4g} L" for fuelName in self.tank.fuel]
        return info

    def show(self):
        print("\n".join(self.info()))
        print("--- " * 10)

stage1 = Stage(1, "HP Steel Fuselage", [("WAC-Corporal", 1)])
stage1.autoFill()
print("--- " * 10)
stage1.tank.show()
stage1.engines[0][0].show()
stage1.show()