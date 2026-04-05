import json, math
G = 9.80665

def fuelDictPlus(a: dict[str, dict[str, float]], b: dict[str, dict[str, float]]) -> dict[str, dict[str, float]]:
    result = {}
    for key1 in list(a.keys()) + list(b.keys()):
        result[key1] = {}
        if key1 in a:
            for key2 in a[key1]:
                result[key1][key2] = a[key1][key2]
        if key1 in b:
            for key2 in b[key1]:
                if not key2 in result[key1]: result[key1][key2] = 0
                result[key1][key2] += b[key1][key2]
    return result
def fuelDictMul(a: dict[str, dict[str, float]], b: float) -> dict[str, dict[str, float]]:
    result = {}
    for key1 in a:
        result[key1] = {}
        for key2 in a[key1]:
            result[key1][key2] = a[key1][key2] * b
    return result




class Tank:
    def __init__(self, name: str):
        tankData = Tanks_Data[name]
        self.name = name
        self.utilization = tankData['utilization'] / 100
        self.densityStructure = tankData['densityStructure'] * 1000
        self.densityContainer = tankData['densityContainer'] * 1000
        self.effectiveDensity = self.densityStructure + self.densityContainer * self.utilization

    def info(self) -> list[str]:
        info = [f"Tank Name: \t\t{self.name}",
                f"Utilization: \t\t{self.utilization * 100:.4g}%",
                f"Structure Density: \t{self.densityStructure * 1000:.4g} kg/kL",
                f"Container Density: \t{self.densityContainer * 1000:.4g} kg/kL",
                f"Effective Density: \t{self.effectiveDensity * 1000:.4g} kg/kL"]
        return info

    def show(self):
        print("\n".join(self.info()))
        print('--- ' * 10)



class Engine:
    def __init__(self, familyName: str, name: str):
        engineData = Engines_Data[familyName]['config'][name]
        origMass = Engines_Data[familyName]['origMass']
        self.familyName = familyName
        self.name = name
        self.mass = origMass * engineData['massMult'] * 1000
        self.maxThrust = engineData['maxThrust']
        self.Isp = engineData['Isp']
        self.ratedBurnTime = engineData['ratedBurnTime']
        self.residual = engineData['residual'] / 100
        self.propellant = engineData['propellant']
        self.gas = engineData['gas']
        fuelInfo = {fuelName: Fuels[fuelName] * 1000 for fuelName in list(self.propellant) + list(self.gas)}
        self.consumption = {'propellant' : {}, 'gas' : {}}
        propVolumeRate = self.maxThrust * 1000 / (self.Isp * G) / sum(fuelInfo[propName] * self.propellant[propName] for propName in self.propellant)
        for propName in self.propellant: self.consumption['propellant'][propName] = [fuelInfo[propName] * self.propellant[propName] * propVolumeRate, self.propellant[propName] * propVolumeRate]
        for gasName in self.gas: self.consumption['gas'][gasName] = [fuelInfo[gasName] * self.gas[gasName] * propVolumeRate, self.gas[gasName] * propVolumeRate]

    def info(self) -> list[str]:
        info = [f"Family Name: \t\t{self.familyName}",
                f"Engine Name: \t\t{self.name}",
                f"Mass: \t\t\t{self.mass:.4g} kg",
                f"Max Thrust: \t\t{self.maxThrust:.4g} kN",
                f"Isp: \t\t\t{self.Isp:.4g} s",
                f"Residual: \t\t{self.residual * 100:.4g}%",
                f"Rated Burn Time: \t{self.ratedBurnTime:.4g} s",
                f"Consumption Details:"]
        for fuelType in self.consumption:
            for fuelName in self.consumption[fuelType]:
                info += [f"\t{f'{fuelName}:':15} {self.consumption[fuelType][fuelName][0]:.4g} kg/s",
                         f"\t\t\t{self.consumption[fuelType][fuelName][1]:.4g} L/s"]
        return info

    def fuelCalByTime(self, time: float) -> list[dict[str, dict[str, float]]]:
        fuel = {'propellant' : {propName: time * self.consumption['propellant'][propName][1] / (1 - self.residual) for propName in self.propellant}, 'gas' : {gasName: time * self.consumption['gas'][gasName][1] / (1 - self.residual) for gasName in self.gas}}
        residualFuel = fuelDictMul(fuel, self.residual)
        return [fuel, residualFuel]

    def fuelCalByCapacity(self, capacity: float) -> list[dict[str, dict[str, float]]]:
        base = sum([self.propellant[propName] for propName in self.propellant] + [self.gas[gasName] / 200 for gasName in self.gas])
        fuel = {'propellant' : {propName : capacity * self.propellant[propName] / base for propName in self.propellant}, 'gas' : {gasName : capacity * self.gas[gasName] * 200 / base for gasName in self.gas}}
        residualFuel = fuelDictMul(fuel, self.residual)
        return [fuel, residualFuel]


    def show(self):
        print("\n".join(self.info()))
        print('--- ' * 10)



class RealTank(Tank):
    def __init__(self, name: str):
        super().__init__(name)
        self. volume, self.capacity, self.massStructure, self.massContainer, self.effectiveMass = 0, 0, 0, 0, 0
        self.content = {'propellant': {}, "gas": {}}
        # self.massContent = 0

    def massCal(self):
        self.massStructure = self.volume * self.densityStructure
        self.massContainer = self.capacity * self.densityContainer
        self.effectiveMass = self.massStructure + self.massContainer
        # self.massContent = sum([Fuels[propName] * self.content['propellant'][propName] for propName in self.content['propellant']] + [Fuels[gasName] * 200 * self.content['gas'][gasName] for gasName in self.content['gas']])

    def setByContent(self, content: dict[str, dict[str, float]]):
        self.content = content
        self.capacity = sum([self.content['propellant'][propName] for propName in self.content['propellant']] + [self.content['gas'][gasName] / 200 for gasName in self.content['gas']])
        self.volume = self.capacity / self.utilization
        self.massCal()

    def info(self):
        info = [f"Tank Name: \t\t{self.name}",
                f"Volume: \t\t{self.volume:.4g} L",
                f"Capacity: \t\t{self.capacity:.4g} L",
                f"Effective Mass: \t{self.effectiveMass:.4g} kg",
                # f"Content Mass: \t\t{self.massContent:.4g} kg",
                "Content:"]
        for contentType in self.content: info += [f"\t{f'{contentName}:':15} {self.content[contentType][contentName]:.4g} L" for contentName in self.content[contentType]]
        return info

    def show(self):
        print("\n".join(self.info()))
        print('--- ' * 10)



class TankEngMix:
    def __init__(self, num: int, tankName: str, engineList: list[tuple[str, int]]):
        self.num = num
        self.tank = RealTank(tankName)
        self.engineList = [(Engines[engName], num) for engName, num in engineList]
        self.extraMass = 0
        self.content = {'propellant': {}, 'gas': {}}
        self.residualContent = {'propellant': {}, 'gas': {}}
        self.burnTime = 0
        self.maxThrust = sum(engine.maxThrust * n for engine, n in self.engineList)
        self.propConMassRate = sum(sum(engine.consumption['propellant'][propName][0] for propName in engine.consumption['propellant']) * n for engine, n in self.engineList)
        self.startMass, self.endMass = 0, 0

    def autoSet(self):
        self.burnTime = min(engine.ratedBurnTime for engine, n in self.engineList) + 5
        self.content, self.residualContent = {'propellant': {}, 'gas': {}}, {'propellant': {}, 'gas': {}}
        for engine, n in self.engineList:
            fuel, residualFuel = engine.fuelCalByTime(self.burnTime)
            self.content = fuelDictPlus(self.content, fuelDictMul(fuel, n))
            self.residualContent = fuelDictPlus(self.residualContent, fuelDictMul(residualFuel, n))
        self.tank.setByContent(self.content)
        self.startMass = self.tank.effectiveMass + sum(engine.mass * n for engine, n in self.engineList)
        self.endMass = self.tank.effectiveMass + sum(engine.mass * n for engine, n in self.engineList)
        for fuelType in self.content:
            for fuelName in self.content[fuelType]:
                self.startMass += self.content[fuelType][fuelName] * Fuels[fuelName] * 1000
                self.endMass += self.residualContent[fuelType][fuelName] * Fuels[fuelName] * 1000

    def info(self) -> list[str]:
        info = [f"Tank Name: \t\t{self.tank.name}", "Engines:"]
        info += [f"\t{f'{engine.name}:':15} {n}" for engine, n in self.engineList]
        info += [f"Extra Mass: \t\t{self.extraMass:.4g} kg",
                 f"Burn Time: \t\t{self.burnTime:.4g} s",
                 f"Max Thrust: \t\t{self.maxThrust:.4g} kN",
                 f"Start Mass:\t\t{self.startMass:.4g} kg",
                 f"End Mass:\t\t{self.endMass:.4g} kg",
                 f"Prop Consumption: \t{self.propConMassRate:.4g} kg/s"]
        info.append("Fuels:")
        for fuelType in self.content:
            for fuelName in self.content[fuelType]:
                info.append(f"\t{f'{fuelName}:':15} {self.content[fuelType][fuelName]:.4g} L")
        info.append("Residual Fuels:")
        for fuelType in self.residualContent:
            for fuelName in self.residualContent[fuelType]:
                info.append(f"\t{f'{fuelName}:':15} {self.residualContent[fuelType][fuelName]:.4g} L")
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


tank = Tank('HP Steel Fuselage')
eng = Engines["WAC-Corporal"]
mix = TankEngMix(1, "HP Steel Fuselage", [("WAC-Corporal", 2)])
mix.autoSet()

eng.show()
mix.show()
mix.tank.show()
tank.show()