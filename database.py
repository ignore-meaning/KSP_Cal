import json

class Tank:
    def __init__(self, name:str, tankData:dict):
        self.name = name
        self.utilization = tankData['utilization']
        self.densityStructure = tankData['densityStructure'] * 1e6
        self.densityContainer = tankData['densityContainer'] * 1e6
        self.effectiveDensity = self.densityStructure + self.densityContainer * self.utilization / 100

    def show(self):
        print(f"Tank Name: \t\t{self.name}")
        print(f"Utilization: \t\t{self.utilization}%")
        print(f"Structure Density: \t{self.densityStructure:.4g} kg/kL")
        print(f"Container Density: \t{self.densityContainer:.4g} kg/kL")
        print(f"Effective Density: \t{self.effectiveDensity:.4g} kg/kL")
        print('--- ' * 10)

class Engine:
    def __init__(self, familyName:str, name:str, engineData:dict, origMass:float):
        self.familyName = familyName
        self.name = name
        self.mass = origMass * engineData['massMult']
        self.maxThrust = engineData['maxThrust']
        self.impulse = engineData['impulse']
        self.ratedBurnTime = engineData['ratedBurnTime']
        self.propellant = engineData['propellant']
        self.gas = engineData['gas']
        fuelInfo = {fuelName: Fuels[fuelName] for fuelName in list(self.propellant.keys()) + list(self.gas.keys())}
        self.consumption = [0, 0]
        self.consumptionDetail = {"propellant" : {propName : [0, 0] for propName in self.propellant}, "gas" : {gasName : [0, 0] for gasName in self.gas}}
        conAllPropMass = self.maxThrust * 1000 / (9.80665 * self.impulse)
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


with open("Fuel.json", 'r') as f:
    Fuels = json.load(f)

with open("Tank.json", 'r') as f:
    Tanks_Data = json.load(f)
Tanks = {}
for name, tankData in Tanks_Data.items():
    Tanks[name] = Tank(name,tankData)

with open("Engine.json", 'r') as f:
    Engines_Data = json.load(f)
Engines = {}
for familyName, engineFamily_Data in Engines_Data.items():
    Engines[familyName] = {}
    for name, engineData in engineFamily_Data['config'].items():
        Engines[familyName][name] = Engine(familyName, name, engineData, engineFamily_Data['origMass'])

# print('--- ' * 10)
# for tankName in Tanks:
#     Tanks[tankName].show()
# for engineFamilyName in Engines:
#     for engineName in Engines[engineFamilyName]:
#         Engines[engineFamilyName][engineName].show()