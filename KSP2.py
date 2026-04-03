import json


def weightedAverage(data: list[tuple[float, float]]) -> float:
    return sum(num * w for num, w in data) / sum(w for num, w in data)


def propCal(propData: dict[str, float], gasData: dict[str, float], propRateMass: float):
    propInfo = [(Fuels[prop], ratio) for prop, ratio in propData.items()]
    gasInfo = [(Fuels[gas] * 200, ratio / 200) for gas, ratio in gasData.items()]
    a = sum(fuel for fuel, ratio in propInfo + gasInfo)
    b = sum(prop for prop, ratio in propInfo)
    density_prop = weightedAverage(propInfo) * 1000
    density_fuel = weightedAverage(propInfo + gasInfo) * 1000
    propRateV = propRateMass / density_prop
    fuelRateV = propRateV * a / b
    fuelRateMass = fuelRateV * density_fuel
    return density_fuel, fuelRateV, fuelRateMass


class Tank:
    def __init__(self, mold: str, TankData: dict):
        self.mold = mold
        self.utilization = TankData['utilization']
        self.density_Structure = TankData['density_Structure']
        self.density_Wall = TankData['density_Wall']
        self.effectiveDensity = self.density_Wall * self.utilization / 100 + self.density_Structure

    def show(self):
        print(f"Tank Mold: \t\t{self.mold}")
        print(f"Utilization: \t\t{self.utilization}%")
        print(f"Structure Density: \t{self.density_Structure} kg/kL")
        print(f"Wall Density: \t\t{self.density_Wall} kg/kL")
        print(f"Effective Density: \t{'%.4g' % self.effectiveDensity} kg/kL")
        print('--- ' * 6)


class Engine:
    def __init__(self, name: str, EngineData: dict, origMass: float):
        self.name = name
        self.mass = origMass * EngineData['massMult'] * 1000
        self.maxThrust = EngineData['maxThrust']
        self.impulse = EngineData['impulse']
        self.ratedBurnTime = EngineData['ratedBurnTime']
        self.propellant = EngineData['propellant']
        self.gas = EngineData['gas'] if 'gas' in EngineData else {"Nitrogen": 0}
        self.propRateMass = self.maxThrust * 1000 / (9.8 * self.impulse)
        self.density_fuel, self.fuelRateV, self.fuelRateMass = propCal(self.propellant, self.gas, self.propRateMass)
        self.VolumeOfFuel = self.fuelRateV * (self.ratedBurnTime + 5)

    def show(self):
        print(f"Engine Name: \t\t{self.name}")
        print(f"Engine Mass: \t\t{'%.4g' % self.mass} kg")
        print(f"Max Thrust: \t\t{self.maxThrust} kN")
        print(f"Impulse: \t\t{self.impulse} s")
        print(f"Rated Burn Time: \t{self.ratedBurnTime} s")
        print(f"Fuel Density: \t\t{'%.4g' % self.density_fuel} kg/L")
        print(f"Fuel Consumption Rate: \t{'%.4g' % self.fuelRateMass} kg/s")
        print(f"fuelRateV: \t\t{'%.4g' % self.fuelRateV} L/s")
        print('--- ' * 6)


with open("Fuel.json", 'r') as f:
    Fuels = json.load(f)

with open("Tank.json", "r") as f:
    Tanks_Data = json.load(f)
Tanks = {}
for mold, TankData in Tanks_Data.items():
    Tanks[mold] = Tank(mold, TankData)

with open("Engine.json", 'r') as f:
    Engines_Data = json.load(f)
Engines = {}
for familyName, engineFamily_Data in Engines_Data.items():
    Engines[familyName] = {}
    origMass = engineFamily_Data['origMass']
    for name, engineData in engineFamily_Data['config'].items():
        Engines[familyName][name] = Engine(name, engineData, origMass)

Tanks['HP Steel Fuselage'].show()
Engines['Aerobee']['WAC-Corporal'].show()