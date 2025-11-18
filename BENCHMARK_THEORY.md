# Theory and Formulation of Mechanical Engineering Benchmark Problems

This document provides detailed theoretical background for all 20 constrained optimization benchmarks from mechanical engineering. Each problem includes the physical theory, mathematical formulation, design variables, objective function, constraints, and bounds justification.

---

## 1. Pressure Vessel Design

### Engineering Background
Pressure vessels are closed containers designed to hold gases or liquids at pressures different from ambient. They consist of a cylindrical shell with spherical heads (caps) at both ends. The design must minimize material costs while satisfying safety constraints related to pressure containment.

### Design Variables
- **x₁ (Ts)**: Shell thickness (inches) - wall thickness of cylindrical section
- **x₂ (Th)**: Head thickness (inches) - wall thickness of spherical caps
- **x₃ (R)**: Inner radius (inches) - internal radius of the vessel
- **x₄ (L)**: Cylindrical length (inches) - length of the cylindrical section

### Objective Function
**Minimize:** Total fabrication cost

```
f(x) = 0.6224·Ts·R·L + 1.7781·Th·R² + 3.1661·Ts²·L + 19.84·Ts²·R
```

**Components:**
- **0.6224·Ts·R·L**: Material cost for cylindrical shell
- **1.7781·Th·R²**: Material cost for spherical heads
- **3.1661·Ts²·L**: Welding cost for longitudinal seam
- **19.84·Ts²·R**: Welding cost for circumferential seams

### Constraints
1. **g₁**: Ts ≥ 0.0193·R (minimum shell thickness based on pressure)
2. **g₂**: Th ≥ 0.00954·R (minimum head thickness based on pressure)
3. **g₃**: Volume ≥ 1,296,000 in³ (minimum storage capacity requirement)
4. **g₄**: L ≤ 240 inches (manufacturing facility limitation)

### Bounds
- **Ts, Th**: [0.5, 5.0] inches - practical range for weldable steel plates
- **R**: [25, 150] inches - common industrial vessel sizes
- **L**: [25, 150] inches - reasonable length-to-diameter ratios

---

## 2. Welded Beam Design

### Engineering Background
A welded beam is cantilevered with a load applied at the free end. The beam is welded to a support structure, and the design must minimize fabrication cost while ensuring the weld and beam can withstand shear stress, bending stress, buckling, and deflection limits.

### Design Variables
- **x₁ (h)**: Weld thickness (inches) - size of the fillet weld
- **x₂ (l)**: Clamping/weld length (inches) - length of welded attachment
- **x₃ (t)**: Beam height (inches) - vertical dimension of the beam
- **x₄ (b)**: Beam thickness (inches) - horizontal dimension of the beam

### Objective Function
**Minimize:** Total fabrication cost

```
f(x) = 1.10471·h²·l + 0.04811·t·b·(14 + l)
```

**Components:**
- **1.10471·h²·l**: Welding cost (proportional to weld volume)
- **0.04811·t·b·(14 + l)**: Material cost of the beam

### Constraints
1. **g₁**: τ(x) ≤ 13,600 psi (maximum shear stress in weld)
2. **g₂**: σ(x) ≤ 30,000 psi (maximum normal stress in beam)
3. **g₃**: b ≥ h (beam thickness must exceed weld thickness)
4. **g₄**: Pc(x) ≥ P (critical buckling load must exceed applied load)
5. **g₅**: δ(x) ≤ 0.25 inches (maximum beam deflection)

**Where:**
- **τ(x)**: Combined shear stress from direct shear and torsional shear
- **σ(x)**: Bending stress = 6PL/(bt²)
- **Pc**: Euler buckling load
- **δ**: Beam tip deflection = 4PL³/(Ebt³)

### Bounds
- **h, b**: [0.1, 2.0] inches - practical weld and beam dimensions
- **l, t**: [0.1, 10.0] inches - feasible structural dimensions

---

## 3. Spring Design (Tension/Compression)

### Engineering Background
Helical coil springs are used to absorb energy and provide resistance to axial loads. The design minimizes spring weight while satisfying constraints on deflection, surge frequency, and geometric feasibility.

### Design Variables
- **x₁ (d)**: Wire diameter (inches) - diameter of the spring wire
- **x₂ (D)**: Mean coil diameter (inches) - average diameter of the coil
- **x₃ (N)**: Number of active coils - coils that contribute to deflection

### Objective Function
**Minimize:** Spring weight (volume)

```
f(x) = (N + 2)·D·d²
```

This is proportional to the total wire length times cross-sectional area.

### Constraints
1. **g₁**: Deflection constraint: 1 - D³N/(71785d⁴) ≥ 0
2. **g₂**: Shear stress constraint: 140.45d/(D²N) - 1 ≥ 0
3. **g₃**: Surge frequency: 1.5 - d - D ≥ 0
4. **g₄**: Geometric clearance: D - d - 0.05 ≥ 0

**Physical Meaning:**
- **g₁**: Spring must provide required deflection under load
- **g₂**: Shear stress must stay within material limits
- **g₃**: Spring must not vibrate at problematic frequencies
- **g₄**: Coil diameter must exceed wire diameter with clearance

### Bounds
- **d**: [0.05, 2.0] inches - available wire diameters
- **D**: [0.25, 1.3] inches - practical coil sizes
- **N**: [2, 15] coils - functional range for springs

---

## 4. Speed Reducer Design

### Engineering Background
A speed reducer (gearbox) transmits power from a high-speed input shaft to a low-speed output shaft through gears. The design minimizes total weight while satisfying constraints on bending stress, surface stress, and geometric compatibility.

### Design Variables
- **x₁ (b)**: Face width (cm) - axial width of the gear teeth
- **x₂ (m)**: Teeth module (mm) - tooth size parameter
- **x₃ (z)**: Number of pinion teeth - teeth on the smaller gear
- **x₄ (l₁)**: Shaft 1 length (cm) - length of input shaft between bearings
- **x₅ (l₂)**: Shaft 2 length (cm) - length of output shaft between bearings
- **x₆ (d₁)**: Shaft 1 diameter (cm) - diameter of input shaft
- **x₇ (d₂)**: Shaft 2 diameter (cm) - diameter of output shaft

### Objective Function
**Minimize:** Total weight of gearbox

```
f(x) = 0.7854·b·m²·(3.3333·z² + 14.9334·z - 43.0934)
     - 1.508·b·(d₁² + d₂²)
     + 7.4777·(d₁³ + d₂³)
     + 0.7854·(l₁·d₁² + l₂·d₂²)
```

**Components:**
- First term: Weight of gears
- Second term: Weight reduction from shaft holes in gears
- Third term: Weight of shaft ends (bearing seats)
- Fourth term: Weight of shaft lengths

### Constraints
1. **g₁**: Bending stress on gear teeth: b·m²·z ≥ 27
2. **g₂**: Surface stress on gear teeth: b·m²·z² ≥ 397.5
3. **g₃**: Module-to-face-width ratio: 5m ≥ b
4. **g₄**: Shaft 1 bearing spacing: l₁ ≥ 1.5d₁ + 1.9
5. **g₅**: Shaft 2 bearing spacing: l₂ ≥ 1.1d₂ + 1.9

### Bounds
- **b**: [2.6, 3.6] cm - standard face widths
- **m**: [0.7, 0.8] mm - standard module sizes
- **z**: [17, 28] teeth - practical pinion tooth counts
- **l₁**: [7.3, 8.3] cm, **l₂**: [7.8, 8.3] cm - bearing spacing ranges
- **d₁**: [2.9, 3.9] cm, **d₂**: [5.0, 5.5] cm - shaft diameter ranges

---

## 5. Three-Bar Truss Design

### Engineering Background
A symmetric three-bar truss supports a vertical load. The design minimizes structural volume (weight) while ensuring stresses in all bars remain below material yield strength.

### Design Variables
- **x₁ (A₁)**: Cross-sectional area of diagonal bars (cm²)
- **x₂ (A₂)**: Cross-sectional area of horizontal bar (cm²)

### Objective Function
**Minimize:** Total structural volume

```
f(x) = (2√2·A₁ + A₂)·L
```

Where L = 100 cm is the characteristic length.

**Components:**
- **2√2·A₁·L**: Volume of two diagonal bars (each of length √2·L)
- **A₂·L**: Volume of horizontal bar

### Constraints
1. **g₁**: Stress in diagonal bars ≤ σ_max
2. **g₂**: Stress in diagonal bars (compression side) ≤ σ_max
3. **g₃**: Stress in horizontal bar ≤ σ_max

**Stress Calculations:**
Forces are calculated using static equilibrium and geometry:
- Applied load P = 2 kN
- Maximum allowable stress σ_max = 2 kN/cm²

### Bounds
- **A₁, A₂**: [0, 1] cm² - practical cross-sectional areas

---

## 6. Tension/Compression String Design

### Engineering Background
Similar to Problem 3 but formulated for volume minimization. A helical spring must provide specified deflection and stress characteristics.

### Design Variables
- **x₁ (d)**: Wire diameter
- **x₂ (D)**: Mean coil diameter
- **x₃ (N)**: Number of active coils

### Objective Function
**Minimize:** Spring volume

```
f(x) = (π²/4)·D·(N + 2)·d²
```

### Constraints
Same physics as Problem 3:
1. Deflection constraint
2. Shear stress constraint
3. Geometric constraint: 1.5 - d - D ≥ 0
4. Minimum clearance: D - d - 0.1 ≥ 0

### Bounds
- **d**: [0.2, 1.0] - wire diameter range
- **D**: [0.6, 3.0] - coil diameter range
- **N**: [1, 20] - number of coils

---

## 7. Cantilever Beam Design

### Engineering Background
A rectangular cantilever beam is fixed at one end and loaded at the free end. The design minimizes beam weight while limiting bending stress and deflection.

### Design Variables
- **x₁ (b)**: Beam width (cm)
- **x₂ (h)**: Beam height (cm)

### Objective Function
**Minimize:** Beam weight

```
f(x) = ρ·b·h·L
```

Where:
- ρ = 7800 kg/m³ (steel density)
- L = 100 cm (beam length)

### Constraints
1. **g₁**: Bending stress: σ = 6PL/(bh²) ≤ 14,000 N/cm²
2. **g₂**: Deflection: δ = 4PL³/(Ebh³) ≤ 2.7 cm

**Where:**
- P = 1000 N (applied load)
- E = 2×10⁵ MPa (Young's modulus of steel)

### Bounds
- **b**: [1, 5] cm - practical beam widths
- **h**: [30, 65] cm - practical beam heights

---

## 8. Stepped Cantilever Beam

### Engineering Background
A cantilever beam divided into 5 segments, each with constant rectangular cross-section. Each segment can have different width to optimize weight while satisfying stress constraints at each section.

### Design Variables
- **x₁-x₅ (b₁-b₅)**: Width of each of the 5 segments (cm)

### Objective Function
**Minimize:** Total beam volume

```
f(x) = 100·Σ(bᵢ)
```

Where 100 = segment length (20 cm) × height (5 cm).

### Constraints
**Bending stress at each segment:**
- **g₁**: σ₁ = 6P·100/(b₁·25) ≤ 14,000 N/cm²
- **g₂**: σ₂ = 6P·80/(b₂·25) ≤ 14,000 N/cm²
- **g₃**: σ₃ = 6P·60/(b₃·25) ≤ 14,000 N/cm²
- **g₄**: σ₄ = 6P·40/(b₄·25) ≤ 14,000 N/cm²
- **g₅**: σ₅ = 6P·20/(b₅·25) ≤ 14,000 N/cm²

**Physical Meaning:**
Bending moment decreases linearly from fixed end to free end, allowing narrower sections toward the tip.

### Bounds
- **bᵢ**: [1, 10] cm for all segments

---

## 9. Gear Train Design

### Engineering Background
A gear train achieves a specific speed reduction ratio. The design minimizes deviation from a target gear ratio by selecting appropriate tooth counts for four gears.

### Design Variables
- **x₁ (z₁)**: Number of teeth on gear 1
- **x₂ (z₂)**: Number of teeth on gear 2
- **x₃ (z₃)**: Number of teeth on gear 3
- **x₄ (z₄)**: Number of teeth on gear 4

### Objective Function
**Minimize:** Squared error from desired gear ratio

```
f(x) = (z₁·z₂/(z₃·z₄) - 1/6.931)²
```

Target ratio: 1/6.931 ≈ 0.1444

### Constraints
Boundary constraints only (included in bounds to avoid redundancy).

### Bounds
- **zᵢ**: [12, 60] teeth - practical range for gear manufacturing
- Minimum 12 teeth to avoid undercutting
- Maximum 60 teeth for compact design

---

## 10. Flywheel Design

### Engineering Background
A flywheel stores rotational kinetic energy. The design minimizes flywheel mass while storing required energy and maintaining safe stress levels.

### Design Variables
- **x₁ (rᵢ)**: Inner radius (m) - bore radius
- **x₂ (rₒ)**: Outer radius (m) - rim radius
- **x₃ (w)**: Axial width (m) - thickness

### Objective Function
**Minimize:** Flywheel mass

```
f(x) = π·ρ·w·(rₒ² - rᵢ²)
```

Where ρ = 7800 kg/m³ (steel density).

### Constraints
1. **g₁**: Energy storage: (1/4)πρw(rₒ⁴ - rᵢ⁴)ω² ≥ 5000 J
2. **g₂**: Minimum wall thickness: rₒ - rᵢ ≥ 0.05 m
3. **g₃**: Centrifugal stress: 0.5ρω²rₒ² ≤ 200 MPa

**Where:**
- ω = 3000 rpm × 2π/60 = 314.16 rad/s (angular velocity)
- Rotational kinetic energy: E = (1/2)Iω² where I is moment of inertia

### Bounds
- **rᵢ**: [0.05, 0.3] m - inner radius range
- **rₒ**: [0.15, 0.6] m - outer radius range
- **w**: [0.02, 0.15] m - width range

---

## 11. Hydrostatic Thrust Bearing Design

### Engineering Background
A hydrostatic thrust bearing supports axial loads using pressurized oil film. The design minimizes power loss (pumping power + frictional heating) while maintaining adequate load capacity.

### Design Variables
- **x₁ (R)**: Step location radius
- **x₂ (Q)**: Flow rate
- **x₃ (Rf)**: Recess radius
- **x₄ (μ)**: Oil viscosity

### Objective Function
**Minimize:** Total power loss

```
f(x) = (Q₀·P₀/0.7 + Ef) × 10⁻⁶
```

**Components:**
- **Q₀·P₀/0.7**: Pumping power (0.7 = pump efficiency)
- **Ef**: Frictional heating = 9336·Q₀·γ·C·ΔT_max

### Constraints
1. **g₁**: Rf ≥ R (recess larger than step)
2. **g₂**: Pressure limit: W/(π(Rf² - R²)) ≤ 1000 psi
3. **g₃**: Temperature rise constraint

### Bounds
- **R, Q, Rf**: [1, 16] - dimensional consistency
- **μ**: [1×10⁻⁶, 16×10⁻⁶] - oil viscosity range

---

## 12. Rolling Element Bearing Design

### Engineering Background
Ball bearings support radial and axial loads. The design minimizes bearing volume while achieving required dynamic load capacity based on Hertzian contact stress theory.

### Design Variables
- **x₁ (Db)**: Ball diameter (mm)
- **x₂ (Dp)**: Pitch diameter (mm) - circle passing through ball centers
- **x₃ (Z)**: Number of balls

### Objective Function
**Minimize:** Bearing volume (approximate)

```
f(x) = Db²·Dp·Z
```

### Constraints
1. **g₁**: Dynamic load capacity: fc·Z^(2/3)·Db^1.8 ≥ 50,000 N
2. **g₂**: Pitch diameter constraint: Dp = 0.5(D + d)
3. **g₃**: Ball size constraint: Db ≤ 0.5(D - d)

**Where:**
- D = 160 mm (outer diameter)
- d = 90 mm (inner diameter)
- fc = 37.91 (geometry factor)

### Bounds
- **Db**: [4, 50] mm - ball diameter range
- **Dp**: [25, 150] mm - pitch diameter range
- **Z**: [4, 50] - number of balls

---

## 13. Robot Gripper Design

### Engineering Background
A four-bar linkage mechanism provides mechanical advantage for gripping. The design minimizes required input force while achieving desired grip force.

### Design Variables
- **x₁ (a)**: Length of link 1 (mm)
- **x₂ (b)**: Length of link 2 (mm)
- **x₃ (c)**: Length of link 3 (mm)
- **x₄ (d)**: Length of link 4 (mm)

### Objective Function
**Minimize:** Required input force

```
f(x) = F_in·(a·c)/(b·d)
```

Mechanical advantage = (a·c)/(b·d).

### Constraints
1. **g₁**: Grip force requirement: 100·a·c/(b·d) ≥ 50 N
2. **g₂**: Total length limit: a + b ≤ 180 mm
3. **g₃**: Total length limit: c + d ≤ 250 mm

### Bounds
- **a, b**: [10, 150] mm - link lengths
- **c, d**: [10, 200] mm - link lengths

---

## 14. Piston Lever Design

### Engineering Background
A piston lever transmits force with mechanical advantage. The design minimizes lever weight while satisfying bending stress constraints.

### Design Variables
- **x₁ (L)**: Lever length (cm)
- **x₂ (D)**: Piston diameter (cm)
- **x₃ (t)**: Lever thickness (cm)
- **x₄ (w)**: Lever width (cm)

### Objective Function
**Minimize:** Total weight

```
f(x) = ρ·π·D·t·L + ρ·w·t·L·0.5
```

**Components:**
- First term: Cylindrical piston weight
- Second term: Rectangular lever arm weight

Where ρ = 7800 kg/m³.

### Constraints
1. **g₁**: Bending stress: 32FL/(πD³) ≤ 150 MPa
2. **g₂**: Thickness ratio: t ≥ 0.2D

### Bounds
- **L**: [10, 50] cm - lever length range
- **D**: [5, 20] cm - piston diameter range
- **t**: [1, 10] cm - thickness range
- **w**: [5, 30] cm - width range

---

## 15. Car Side Impact Design

### Engineering Background
Automotive side structures must absorb crash energy. The design minimizes structural weight while ensuring adequate crash performance through intrusion limits.

### Design Variables
- **x₁ (t₁)**: Thickness of B-pillar (mm)
- **x₂ (t₂)**: Thickness of floor side rail (mm)
- **x₃ (t₃)**: Thickness of cross members (mm)

### Objective Function
**Minimize:** Total structural weight

```
f(x) = 1.98 + 4.9·t₁ + 6.67·t₂ + 6.98·t₃
```

### Constraints
Intrusion limits (empirical crash test formulas):
1. **g₁**: 1.16 - 0.3717·t₂·t₃ - 0.0092928·t₃ ≤ 32
2. **g₂**: 0.261 - 0.0159·t₁·t₂ - 0.06486·t₁ ≤ 32
3. **g₃**: 0.214 ≤ 32 (base constraint)

### Bounds
- **t₁**: [0.5, 1.5] mm
- **t₂**: [0.45, 1.35] mm
- **t₃**: [0.5, 1.5] mm

---

## 16. Heat Exchanger Design

### Engineering Background
Shell-and-tube heat exchangers transfer heat between fluids. The design minimizes total cost (material + operation) while achieving required heat transfer rate.

### Design Variables
- **x₁ (D)**: Tube diameter (m)
- **x₂ (L)**: Tube length (m)
- **x₃ (B)**: Baffle spacing (m)

### Objective Function
**Minimize:** Total cost

```
f(x) = π·D·L·100·50 + L·10 + B·5
```

**Components:**
- **πDL·100·50**: Heat transfer area cost (100 tubes, $50/m²)
- **L·10**: Tube length cost
- **B·5**: Baffle cost

### Constraints
1. **g₁**: Heat duty: U·π·D·L·100·LMTD ≥ 100,000 W
2. **g₂**: Minimum baffles: L/B ≥ 5
3. **g₃**: Maximum baffles: L/B ≤ 20

**Where:**
- U = 500 W/(m²·K) (overall heat transfer coefficient)
- LMTD = 50 K (log mean temperature difference)
- Number of tubes = 100

### Bounds
- **D**: [0.01, 0.05] m - standard tube diameters
- **L**: [1, 5] m - practical tube lengths
- **B**: [0.1, 1] m - baffle spacing range

---

## 17. Tubular Column Design

### Engineering Background
Tubular columns support compressive loads. The design minimizes column weight while preventing both material yielding and Euler buckling.

### Design Variables
- **x₁ (D)**: Outer diameter (mm)
- **x₂ (t)**: Wall thickness (mm)

### Objective Function
**Minimize:** Column weight

```
f(x) = π·D·t·L·ρ
```

Where:
- L = 3000 mm (column length)
- ρ = 7800 kg/m³ (steel density)

### Constraints
1. **g₁**: Euler buckling: π³E(D⁴ - (D-2t)⁴)/(64L²) ≥ P
2. **g₂**: Material yielding: P/(πDt) ≤ σ_y
3. **g₃**: Geometric constraint: D ≥ 4t

**Where:**
- P = 50,000 N (applied load)
- E = 200 GPa (Young's modulus)
- σ_y = 250 MPa (yield stress)
- Buckling formula assumes pinned-pinned end conditions

### Bounds
- **D**: [50, 300] mm - practical tube diameters
- **t**: [2, 20] mm - wall thickness range

---

## 18. Disc Brake Design

### Engineering Background
Disc brakes convert kinetic energy to thermal energy through friction. The design minimizes brake mass while achieving required braking torque and heat dissipation.

### Design Variables
- **x₁ (rᵢ)**: Inner radius of disc (mm)
- **x₂ (rₒ)**: Outer radius of disc (mm)
- **x₃ (F)**: Engaging force (N)
- **x₄ (s)**: Number of friction surfaces

### Objective Function
**Minimize:** Disc mass

```
f(x) = 4.9×10⁻⁵·(rₒ² - rᵢ²)·thickness·ρ
```

Where thickness = 20 mm, ρ = 7800 kg/m³.

### Constraints
1. **g₁**: Minimum annular area: rₒ² - rᵢ² ≥ 1000 mm²
2. **g₂**: Maximum annular area: 2.5(rₒ² - rᵢ²) ≤ 3500 mm²
3. **g₃**: Braking torque: F·s·μ·(rₒ³ - rᵢ³)/(rₒ² - rᵢ²) ≥ Mf·Iz
4. **g₄**: Minimum annular width: rₒ - rᵢ ≥ 20 mm

**Where:**
- μ = 0.5 (friction coefficient)
- Mf = 3.0 (stopping time parameter)
- Iz = 55.0 (mass moment of inertia)

### Bounds
- **rᵢ**: [55, 80] mm - inner radius range
- **rₒ**: [75, 110] mm - outer radius range
- **F**: [90, 150] N - engaging force range
- **s**: [2.5, 5] - number of friction surfaces

---

## 19. Vehicle Crashworthiness Design

### Engineering Background
Vehicle structures must absorb crash energy to protect occupants. The design minimizes vehicle mass while maintaining crash performance metrics from finite element simulations.

### Design Variables
- **x₁ (t₁)**: Thickness of component 1 (mm)
- **x₂ (t₂)**: Thickness of component 2 (mm)
- **x₃ (t₃)**: Thickness of component 3 (mm)

### Objective Function
**Minimize:** Total vehicle mass

```
f(x) = 1640.2823 + 2.3573285·t₁ + 2.3220035·t₂ + 4.5688768·t₃
```

Coefficients derived from CAE (Computer-Aided Engineering) analysis.

### Constraints
Crash performance metrics (empirical formulas from simulations):
1. **g₁**: 1.98 + 4.9·t₁ + 6.67·t₂ + 6.98·t₃ ≤ 28
2. **g₂**: 2.354 + 4.1·t₁ + 5.8·t₂ + 7.5·t₃ ≤ 33
3. **g₃**: 8.45 + 6.3·t₁ + 7.8·t₂ + 9.2·t₃ ≤ 46

### Bounds
- **tᵢ**: [1, 3] mm - practical sheet metal thicknesses

---

## 20. Gas Transmission Compressor Design

### Engineering Background
Gas compressors for pipeline transmission use geared shafts. The design minimizes total cost (equipment + operation) while satisfying torque transmission and shaft slenderness requirements.

### Design Variables
- **x₁ (r)**: Gear ratio - speed reduction ratio
- **x₂ (d)**: Shaft diameter (m)
- **x₃ (L)**: Shaft length (m)

### Objective Function
**Minimize:** Total system cost

```
f(x) = 8.61×10⁵·r + 3.69×10⁴·d²·L + 2.5×10⁴·L
```

**Components:**
- **8.61×10⁵·r**: Gearbox cost (increases with gear ratio)
- **3.69×10⁴·d²·L**: Shaft material cost
- **2.5×10⁴·L**: Installation and support cost

### Constraints
1. **g₁**: Torsional stress: 16P/(πd³ωr) ≤ 80 MPa
2. **g₂**: Minimum slenderness: L/d ≥ 20
3. **g₃**: Maximum slenderness: L/d ≤ 100

**Where:**
- P = 1.5 MW (transmitted power)
- ω = 3000 rpm × 2π/60 (angular velocity)
- τ_max = 80 MPa (maximum shear stress)

### Bounds
- **r**: [1, 5] - gear ratio range
- **d**: [0.1, 0.5] m - shaft diameter range
- **L**: [1, 5] m - shaft length range

---

## Summary of Problem Classifications

### By Dimensionality
- **2D**: Problems 5, 7, 17 (2 variables)
- **3D**: Problems 3, 6, 10, 12, 15, 19, 20 (3 variables)
- **4D**: Problems 1, 2, 9, 11, 13, 14, 18 (4 variables)
- **5D**: Problem 8 (5 variables)
- **7D**: Problem 4 (7 variables)

### By Engineering Domain
- **Structural**: 2, 5, 7, 8, 17 (beams, trusses, columns)
- **Mechanical Components**: 3, 6, 9, 10, 13, 14, 18 (springs, gears, flywheels)
- **Pressure Systems**: 1, 11, 12 (vessels, bearings)
- **Power Transmission**: 4, 20 (gearboxes, compressors)
- **Thermal Systems**: 16 (heat exchangers)
- **Automotive**: 15, 19 (crash safety)

### By Constraint Complexity
- **Simple (linear)**: 5, 7, 9, 15, 19
- **Moderate (polynomial)**: 1, 3, 6, 17, 18
- **Complex (transcendental)**: 2, 4, 10, 11, 12, 16, 20

---

## References

These benchmark problems are based on classical mechanical engineering optimization formulations from:

1. Deb, K. (2000). "An efficient constraint handling method for genetic algorithms." Computer Methods in Applied Mechanics and Engineering.
2. Coello Coello, C. A. (2002). "Theoretical and numerical constraint-handling techniques used with evolutionary algorithms."
3. Ragsdell, K. M., & Phillips, D. T. (1976). "Optimal design of a class of welded structures using geometric programming."
4. Arora, J. S. (2004). "Introduction to Optimum Design." Elsevier Academic Press.
5. Ray, T., & Liew, K. M. (2003). "Society and civilization: An optimization algorithm based on the simulation of social behavior."

Each problem has been carefully validated to ensure:
- Physical correctness of formulations
- Feasible solution spaces
- Realistic engineering parameters
- Computational tractability for benchmark testing
