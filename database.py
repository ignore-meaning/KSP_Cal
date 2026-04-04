import json

G = 9.80665

class Tank:
    def __init__(self, name:str):
        tankData = Tanks_Data[name]
        self.name = name
        self.utilization = tankData['utilization']
        self.densityStructure = tankData['densityStructure'] * 1e6
        self.densityContainer = tankData['densityContainer'] * 1e6
        self.effectiveDensity = self.densityStructure + self.densityContainer * self.utilization / 100

    def info(self):
        info = [f"Tank Name: \t\t{self.name}",
                f"Utilization: \t\t{self.utilization}%",
                f"Structure Density: \t{self.densityStructure:.4g} kg/kL",
                f"Container Density: \t{self.densityContainer:.4g} kg/kL",
                f"Effective Density: \t{self.effectiveDensity:.4g} kg/kL"]
        return info

    def show(self):
        print("\n".join(self.info()))
        print('--- ' * 10)

class Engine:
    def __init__(self, familyName:str, name:str):
        engineData = Engines_Data[familyName]['config'][name]
        origMass = Engines_Data[familyName]['origMass']
        self.familyName = familyName
        self.name = name
        self.mass = origMass * engineData['massMult'] * 1000
        self.maxThrust = engineData['maxThrust']
        self.impulse = engineData['impulse']
        self.ratedBurnTime = engineData['ratedBurnTime']
        self.propellant = engineData['propellant']
        self.gas = engineData['gas']
        fuelInfo = {fuelName: Fuels[fuelName] for fuelName in list(self.propellant.keys()) + list(self.gas.keys())}
        self.consumption = [0, 0]
        self.consumptionDetail = {"propellant" : {propName : [0, 0] for propName in self.propellant}, "gas" : {gasName : [0, 0] for gasName in self.gas}}
        conAllPropMass = self.maxThrust * 1000 / (G * self.impulse)
        densityAllProp = sum(fuelInfo[prop] * ratio for prop, ratio in self.propellant.items()) * 1000
        conAllPropVolume = conAllPropMass / densityAllProp
        for propName in self.propellant:
            self.consumptionDetail["propellant"][propName][1] = conAllPropVolume * self.propellant[propName]
            self.consumptionDetail["propellant"][propName][0] = self.consumptionDetail["propellant"][propName][1] * fuelInfo[propName] * 1000
            self.consumption[1] += self.consumptionDetail["propellant"][propName][1]
            self.consumption[0] += self.consumptionDetail["propellant"][propName][0]
        for gasName in self.gas:
            self.consumptionDetail["gas"][gasName][1] = conAllPropVolume * self.gas[gasName]
            self.consumptionDetail["gas"][gasName][0] = self.consumptionDetail["gas"][gasName][1] * fuelInfo[gasName] * 1000
            self.consumption[1] += self.consumptionDetail["gas"][gasName][1] / 200
            self.consumption[0] += self.consumptionDetail["gas"][gasName][0]

    def show(self):
        print(f"Family Name: \t\t{self.familyName}")
        print(f"Engine Name: \t\t{self.name}")
        print(f"Mass: \t\t\t{self.mass:.4g} kg")
        print(f"Max Thrust: \t\t{self.maxThrust:.4g} kN")
        print(f"Impulse: \t\t{self.impulse:.4g} s")
        print(f"Rated Burn Time: \t{self.ratedBurnTime:.4g} s")
        print(f"Fuel Consumption Rate: \t{self.consumption[0]:.4g} kg/s")
        print(f"\t\t\t{self.consumption[1]:.4g} L/s")
        print("Consumption Details:")
        for fuelType in self.consumptionDetail:
            for fuelName in self.consumptionDetail[fuelType]:
                print(f"\t{f'{fuelName}:':15} {self.consumptionDetail[fuelType][fuelName][0]:.4g} kg/s")
                print(f"\t\t\t{self.consumptionDetail[fuelType][fuelName][1]:.4g} L/s")
        print('--- ' * 10)

class RealTank(Tank):
    def __init__(self, name: str):
        super().__init__(name)
        self.volume = 0
        self.capacity = 0
        self.netMass = 0
        self.wetMass = 0
        self.fuel = {}

    def fillFuel(self, engineList: list[tuple[Engine, int]], time: float):
        fuelMass = 0
        for engine, num in engineList:
            for propName in engine.consumptionDetail["propellant"]:
                if propName not in self.fuel: self.fuel[propName] = 0
                self.fuel[propName] += num * engine.consumptionDetail["propellant"][propName][1] * time
                fuelMass += num * engine.consumptionDetail["propellant"][propName][0] * time
            for gasName in engine.consumptionDetail["gas"]:
                if gasName not in self.fuel: self.fuel[gasName] = 0
                self.fuel[gasName] += num * engine.consumptionDetail["gas"][gasName][1] / 200 * time
                fuelMass += num * engine.consumptionDetail["gas"][gasName][0] * time
        self.capacity = sum(self.fuel.values())
        self.volume = self.capacity / self.utilization * 100
        self.netMass = self.volume * self.effectiveDensity / 1000
        self.wetMass = self.netMass + fuelMass

    def info(self):
        info = super().info()
        info.insert(1, f"Capacity: \t\t{self.capacity:.4g} L")
        info.insert(1, f"Volume: \t\t{self.volume:.4g} L")
        info.insert(1, f"Wet Mass: \t\t{self.wetMass:.4g} kg")
        info.insert(1, f"Net Mass: \t\t{self.netMass:.4g} kg")
        return info

    def show(self):
        print("\n".join(self.info()))
        print('--- ' * 10)


with open("Fuel.json", 'r') as f:
    Fuels = json.load(f)

with open("Tank.json", 'r') as f:
    Tanks_Data = json.load(f)

with open("Engine.json", 'r') as f:
    Engines_Data = json.load(f)
Engines = {}
for familyName, engineFamily_Data in Engines_Data.items():
    for name in engineFamily_Data['config']:
        Engines[name] = Engine(familyName, name)

# print('--- ' * 10)
# for tankName in Tanks_Data:
#     Tank(tankName).show()
# for engineName in Engines:
#     Engines[engineName].show()