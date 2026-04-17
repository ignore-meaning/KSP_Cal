## Engine(familyName, name)

### 变量

- `familyName` : str

- `name` : str

- `mass` : float

- `maxThrust`

- `Isp`

- `ratedBurnTime`

- `residual`

- `propellant`

- `gas`

- `consumption`

### 方法

- `fuelCalByTime`

- `fuelCalByCapacity`

- `show`

## Tank(name)

### 变量

- `name` : str

- `utilization` : float，为介于 0 到 1 的比值

- `densityStructure` : float，单位为 kg/L

- `densityContainer` : float，单位为 kg/L

- `effectiveDensity` : float，单位为 kg/L

### 方法

- `show`

## RealTank(name)

### 变量

所有 tank 的变量

- `volume`

- `capacity`

- `massStructure`

- `massContainer`

- `effectiveMass`

- `content` : FuelType

### 方法

- `massCal`

- `setByContent`

- `show`

## TankEngMix

### 变量

- `tank`

- `engineList`

- `extraMass`

- `content`

- `residualContent`

- `burnTime`

- `maxThrust`

- `propConMassRate`

- `Isp`

### 方法

- `autoSet`

- `fullSet`

- `show`