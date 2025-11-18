"""
20 Mechanical Engineering Constrained Optimization Problems - CORRECTED VERSION

Each problem includes:
- Objective function to minimize
- Variable bounds
- Constraint functions
- Initial guess
- Problem description
"""

import numpy as np
from typing import Dict, List, Callable, Tuple


class OptimizationProblem:
    """Base class for optimization problems"""
    def __init__(self, name: str, description: str, dim: int):
        self.name = name
        self.description = description
        self.dim = dim

    def objective(self, x: np.ndarray) -> float:
        raise NotImplementedError

    def get_bounds(self) -> List[Tuple[float, float]]:
        raise NotImplementedError

    def get_constraints(self) -> List[Dict]:
        raise NotImplementedError

    def get_initial_guess(self) -> np.ndarray:
        raise NotImplementedError


class PressureVesselDesign(OptimizationProblem):
    """
    Problem 1: Pressure Vessel Design - FIXED
    Minimize the cost of a cylindrical pressure vessel with spherical heads
    Variables: [thickness_shell, thickness_head, inner_radius, length]
    """
    def __init__(self):
        super().__init__(
            "Pressure Vessel Design",
            "Minimize cost of cylindrical pressure vessel",
            4
        )

    def objective(self, x: np.ndarray) -> float:
        Ts, Th, R, L = x
        # Cost = material + forming + welding
        return 0.6224 * Ts * R * L + 1.7781 * Th * R**2 + 3.1661 * Ts**2 * L + 19.84 * Ts**2 * R

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(0.5, 5.0), (0.5, 5.0), (25.0, 150.0), (25.0, 150.0)]

    def get_constraints(self) -> List[Dict]:
        return [
            {'type': 'ineq', 'fun': lambda x: x[0] - 0.0193 * x[2]},  # Shell thickness
            {'type': 'ineq', 'fun': lambda x: x[1] - 0.00954 * x[2]},  # Head thickness
            {'type': 'ineq', 'fun': lambda x: np.pi * x[2]**2 * x[3] + (4/3) * np.pi * x[2]**3 - 1296000},  # Volume
            {'type': 'ineq', 'fun': lambda x: 240 - x[3]}  # Length limit
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([1.0, 1.0, 50.0, 100.0])


class WeldedBeamDesign(OptimizationProblem):
    """
    Problem 2: Welded Beam Design
    Minimize the cost of a welded beam subject to constraints on shear stress,
    bending stress, buckling, and deflection
    Variables: [weld_thickness, clamping_length, beam_height, beam_thickness]
    """
    def __init__(self):
        super().__init__(
            "Welded Beam Design",
            "Minimize cost of welded beam structure",
            4
        )

    def objective(self, x: np.ndarray) -> float:
        h, l, t, b = x
        return 1.10471 * h**2 * l + 0.04811 * t * b * (14.0 + l)

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(0.1, 2.0), (0.1, 10.0), (0.1, 10.0), (0.1, 2.0)]

    def get_constraints(self) -> List[Dict]:
        P = 6000  # Load
        L = 14    # Length
        E = 30e6  # Modulus of elasticity
        G = 12e6  # Shear modulus
        tau_max = 13600  # Max shear stress
        sigma_max = 30000  # Max normal stress
        delta_max = 0.25  # Max deflection

        def tau(x):
            h, l, t, b = x
            tau1 = P / (np.sqrt(2) * h * l)
            M = P * (L + l / 2)
            R = np.sqrt(0.25 * (l**2 + (h + t)**2))
            J = 2 * (np.sqrt(2) * h * l * (l**2 / 12 + 0.25 * (h + t)**2))
            tau2 = M * R / J
            return np.sqrt(tau1**2 + tau1 * tau2 * l / R + tau2**2)

        def sigma(x):
            h, l, t, b = x
            return 6 * P * L / (b * t**2)

        def buckling(x):
            h, l, t, b = x
            Pc = 4.013 * E * np.sqrt(t**2 * b**6 / 36) / L**2 * (1 - t / (2 * L) * np.sqrt(E / (4 * G)))
            return Pc

        def deflection(x):
            h, l, t, b = x
            return 4 * P * L**3 / (E * b * t**3)

        return [
            {'type': 'ineq', 'fun': lambda x: tau_max - tau(x)},
            {'type': 'ineq', 'fun': lambda x: sigma_max - sigma(x)},
            {'type': 'ineq', 'fun': lambda x: x[3] - x[0]},
            {'type': 'ineq', 'fun': lambda x: buckling(x) - P},
            {'type': 'ineq', 'fun': lambda x: delta_max - deflection(x)}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([0.5, 5.0, 5.0, 0.5])


class SpringDesign(OptimizationProblem):
    """
    Problem 3: Tension/Compression Spring Design - FIXED
    Minimize the weight of a spring
    Variables: [wire_diameter, mean_coil_diameter, number_of_coils]
    """
    def __init__(self):
        super().__init__(
            "Spring Design",
            "Minimize weight of tension/compression spring",
            3
        )

    def objective(self, x: np.ndarray) -> float:
        d, D, N = x
        return (N + 2) * D * d**2

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(0.05, 2.0), (0.25, 1.3), (2.0, 15.0)]

    def get_constraints(self) -> List[Dict]:
        # Simplified constraints to avoid division by zero
        return [
            {'type': 'ineq', 'fun': lambda x: 1 - x[1]**3 * x[2] / (71785 * x[0]**4)},
            {'type': 'ineq', 'fun': lambda x: 140.45 * x[0] / (x[1]**2 * x[2]) - 1},
            {'type': 'ineq', 'fun': lambda x: 1.5 - x[0] - x[1]},
            {'type': 'ineq', 'fun': lambda x: x[1] - x[0] - 0.05}  # D > d minimum clearance
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([0.3, 0.8, 10.0])


class SpeedReducerDesign(OptimizationProblem):
    """
    Problem 4: Speed Reducer Design - SIMPLIFIED
    Minimize the weight of a speed reducer
    Variables: [face_width, teeth_module, pinion_teeth, shaft1_length, shaft2_length, shaft1_diameter, shaft2_diameter]
    """
    def __init__(self):
        super().__init__(
            "Speed Reducer Design",
            "Minimize weight of speed reducer gearbox",
            7
        )

    def objective(self, x: np.ndarray) -> float:
        b, m, z, l1, l2, d1, d2 = x
        return 0.7854 * b * m**2 * (3.3333 * z**2 + 14.9334 * z - 43.0934) - \
               1.508 * b * (d1**2 + d2**2) + 7.4777 * (d1**3 + d2**3) + \
               0.7854 * (l1 * d1**2 + l2 * d2**2)

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(2.6, 3.6), (0.7, 0.8), (17, 28), (7.3, 8.3), (7.8, 8.3), (2.9, 3.9), (5.0, 5.5)]

    def get_constraints(self) -> List[Dict]:
        # Simplified constraints
        return [
            {'type': 'ineq', 'fun': lambda x: x[0] * x[1]**2 * x[2] - 27},
            {'type': 'ineq', 'fun': lambda x: x[0] * x[1]**2 * x[2]**2 - 397.5},
            {'type': 'ineq', 'fun': lambda x: 5 * x[1] - x[0]},
            {'type': 'ineq', 'fun': lambda x: x[3] - 1.5 * x[5] - 1.9},
            {'type': 'ineq', 'fun': lambda x: x[4] - 1.1 * x[6] - 1.9}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([3.0, 0.75, 20, 7.5, 8.0, 3.5, 5.2])


class ThreeBarTrussDesign(OptimizationProblem):
    """
    Problem 5: Three-Bar Truss Design
    Minimize the volume of a statically loaded 3-bar truss
    Variables: [area1, area2]
    """
    def __init__(self):
        super().__init__(
            "Three-Bar Truss Design",
            "Minimize volume of 3-bar truss structure",
            2
        )

    def objective(self, x: np.ndarray) -> float:
        l = 100  # Length
        return (2 * np.sqrt(2) * x[0] + x[1]) * l

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(0.0, 1.0), (0.0, 1.0)]

    def get_constraints(self) -> List[Dict]:
        P = 2  # Load
        sigma = 2  # Stress limit
        # Safer constraint formulation with bounds check
        return [
            {'type': 'ineq', 'fun': lambda x: sigma * (np.sqrt(2) * x[0]**2 + 2 * x[0] * x[1]) - (np.sqrt(2) * x[0] + x[1]) * P if (x[0]**2 + x[1] > 1e-6) else -1},
            {'type': 'ineq', 'fun': lambda x: sigma * (np.sqrt(2) * x[0]**2 + 2 * x[0] * x[1]) - x[1] * P if (x[0]**2 + x[1] > 1e-6) else -1},
            {'type': 'ineq', 'fun': lambda x: sigma * (np.sqrt(2) * x[1] + x[0]) - P if (x[0] + x[1] > 1e-6) else -1}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([0.5, 0.5])


class TensionCompressionStringDesign(OptimizationProblem):
    """
    Problem 6: Tension/Compression String Design - FIXED
    Minimize volume of a helical spring
    Variables: [diameter, mean_diameter, coils]
    """
    def __init__(self):
        super().__init__(
            "Tension/Compression String",
            "Minimize volume of helical spring",
            3
        )

    def objective(self, x: np.ndarray) -> float:
        d, D, N = x
        return np.pi**2 / 4 * D * (N + 2) * d**2

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(0.2, 1.0), (0.6, 3.0), (1.0, 20.0)]

    def get_constraints(self) -> List[Dict]:
        # Simplified constraints to avoid numerical issues
        return [
            {'type': 'ineq', 'fun': lambda x: 1 - x[1]**3 * x[2] / (71785 * x[0]**4)},
            {'type': 'ineq', 'fun': lambda x: 140.45 * x[0] / (x[1]**2 * x[2]) - 1},
            {'type': 'ineq', 'fun': lambda x: 1.5 - x[0] - x[1]},
            {'type': 'ineq', 'fun': lambda x: x[1] - x[0] - 0.1}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([0.5, 1.5, 10.0])


class CantileverBeamDesign(OptimizationProblem):
    """
    Problem 7: Cantilever Beam Design
    Minimize weight of a cantilever beam
    Variables: [width, height]
    """
    def __init__(self):
        super().__init__(
            "Cantilever Beam Design",
            "Minimize weight of cantilever beam",
            2
        )

    def objective(self, x: np.ndarray) -> float:
        L = 100  # Length
        rho = 7800  # Density
        return rho * x[0] * x[1] * L

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(1.0, 5.0), (30.0, 65.0)]

    def get_constraints(self) -> List[Dict]:
        P = 1000  # Load
        L = 100  # Length
        sigma_max = 14000  # Max stress
        delta_max = 2.7  # Max deflection
        E = 2e5  # Young's modulus

        return [
            {'type': 'ineq', 'fun': lambda x: sigma_max - 6 * P * L / (x[0] * x[1]**2)},
            {'type': 'ineq', 'fun': lambda x: delta_max - 4 * P * L**3 / (E * x[0] * x[1]**3)}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([2.0, 40.0])


class SteppedCantileverBeam(OptimizationProblem):
    """
    Problem 8: Stepped Cantilever Beam - FIXED
    Minimize volume of a 5-segment cantilever beam
    Variables: [width1, width2, width3, width4, width5]
    """
    def __init__(self):
        super().__init__(
            "Stepped Cantilever Beam",
            "Minimize volume of 5-segment cantilever beam",
            5
        )

    def objective(self, x: np.ndarray) -> float:
        # Volume of 5 segments, each 20 cm long, height 5 cm
        return 100 * sum(x)  # Simplified: 20*5 = 100 per unit width

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(1.0, 10.0)] * 5

    def get_constraints(self) -> List[Dict]:
        P = 600  # Load (N) - reduced for feasibility
        sigma_max = 14000  # Max stress (N/cm^2)
        h = 5  # Height (cm)
        # Stress constraints for each segment: sigma = M*c/I = (6*M)/(b*h^2)
        # where M is the bending moment
        return [
            {'type': 'ineq', 'fun': lambda x: sigma_max - 6 * P * 100 / (x[0] * h**2)},
            {'type': 'ineq', 'fun': lambda x: sigma_max - 6 * P * 80 / (x[1] * h**2)},
            {'type': 'ineq', 'fun': lambda x: sigma_max - 6 * P * 60 / (x[2] * h**2)},
            {'type': 'ineq', 'fun': lambda x: sigma_max - 6 * P * 40 / (x[3] * h**2)},
            {'type': 'ineq', 'fun': lambda x: sigma_max - 6 * P * 20 / (x[4] * h**2)}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([5.0, 4.0, 3.0, 2.5, 2.0])


class GearTrainDesign(OptimizationProblem):
    """
    Problem 9: Gear Train Design
    Minimize gear ratio error
    Variables: [teeth1, teeth2, teeth3, teeth4]
    """
    def __init__(self):
        super().__init__(
            "Gear Train Design",
            "Minimize gear ratio error",
            4
        )

    def objective(self, x: np.ndarray) -> float:
        # Minimize deviation from desired gear ratio 1/6.931
        ratio = x[0] * x[1] / (x[2] * x[3])
        desired_ratio = 1.0 / 6.931
        return (ratio - desired_ratio)**2

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(12, 60), (12, 60), (12, 60), (12, 60)]

    def get_constraints(self) -> List[Dict]:
        return [
            {'type': 'ineq', 'fun': lambda x: x[0] - 12},
            {'type': 'ineq', 'fun': lambda x: 60 - x[0]},
            {'type': 'ineq', 'fun': lambda x: x[1] - 12},
            {'type': 'ineq', 'fun': lambda x: 60 - x[1]}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([30, 30, 30, 30])


class FlywheelDesign(OptimizationProblem):
    """
    Problem 10: Flywheel Design - FIXED
    Minimize mass while storing required energy
    Variables: [inner_radius, outer_radius, width]
    """
    def __init__(self):
        super().__init__(
            "Flywheel Design",
            "Minimize flywheel mass for energy storage",
            3
        )

    def objective(self, x: np.ndarray) -> float:
        ri, ro, w = x
        rho = 7800  # Density of steel (kg/m^3)
        return np.pi * rho * w * (ro**2 - ri**2) / 1000  # Convert to kg

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(0.05, 0.3), (0.15, 0.6), (0.02, 0.15)]  # meters

    def get_constraints(self) -> List[Dict]:
        E_required = 5000  # Required energy (J)
        omega = 3000 * 2 * np.pi / 60  # Angular velocity (rad/s)
        rho = 7800  # kg/m^3
        sigma_max = 200e6  # Max stress (Pa)

        return [
            # Energy constraint (rotational kinetic energy)
            {'type': 'ineq', 'fun': lambda x: 0.25 * np.pi * rho * x[2] * (x[1]**4 - x[0]**4) * omega**2 - E_required},
            # Minimum wall thickness
            {'type': 'ineq', 'fun': lambda x: x[1] - x[0] - 0.05},
            # Stress limit (simplified)
            {'type': 'ineq', 'fun': lambda x: sigma_max - 0.5 * rho * omega**2 * x[1]**2}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([0.1, 0.3, 0.08])


class HydrostaticThrustBearingDesign(OptimizationProblem):
    """
    Problem 11: Hydrostatic Thrust Bearing Design
    Minimize power loss in bearing
    Variables: [step_location, flow_rate, recess_radius, oil_viscosity]
    """
    def __init__(self):
        super().__init__(
            "Hydrostatic Thrust Bearing",
            "Minimize power loss in thrust bearing",
            4
        )

    def objective(self, x: np.ndarray) -> float:
        R, Q, Rf, mu = x
        gamma = 0.0307  # Specific weight
        C = 0.5  # Discharge coefficient
        n = -3.55  # Rotational speed parameter
        W = 101000  # Load
        P0 = 1500  # Supply pressure
        Pmax = 1000  # Max pressure
        delT_max = 50  # Max temperature rise
        h_min = 0.001  # Min film thickness

        # Power loss
        Q0 = Q / (2 * np.pi * 1)  # Flow
        Ef = 9336 * Q0 * gamma * C * delT_max
        return (Q0 * P0 / 0.7 + Ef) * 1e-6

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(1.0, 16.0), (1.0, 16.0), (1.0, 16.0), (1e-6, 16e-6)]

    def get_constraints(self) -> List[Dict]:
        W = 101000
        return [
            {'type': 'ineq', 'fun': lambda x: x[2] - x[0]},
            {'type': 'ineq', 'fun': lambda x: 1000 - W / (np.pi * (x[2]**2 - x[0]**2) + 1e-6) + 0.001},
            {'type': 'ineq', 'fun': lambda x: 50 - 0.001}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([5.0, 5.0, 8.0, 5e-6])


class RollingElementBearingDesign(OptimizationProblem):
    """
    Problem 12: Rolling Element Bearing Design
    Minimize bearing volume
    Variables: [ball_diameter, pitch_diameter, number_of_balls]
    """
    def __init__(self):
        super().__init__(
            "Rolling Element Bearing",
            "Minimize volume of rolling element bearing",
            3
        )

    def objective(self, x: np.ndarray) -> float:
        Db, Dp, Z = x
        # Approximate bearing volume
        return Db**2 * Dp * Z

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(4.0, 50.0), (25.0, 150.0), (4, 50)]

    def get_constraints(self) -> List[Dict]:
        fc = 37.91  # Geometry factor
        D = 160  # Outer diameter
        d = 90  # Inner diameter
        C_required = 50000  # Required dynamic capacity

        return [
            {'type': 'ineq', 'fun': lambda x: fc * x[2]**(2/3) * x[0]**(1.8) - C_required},
            {'type': 'ineq', 'fun': lambda x: x[1] - 0.5 * (D + d)},
            {'type': 'ineq', 'fun': lambda x: 0.5 * (D + d) - x[1]},
            {'type': 'ineq', 'fun': lambda x: 0.5 * (D - d) - x[0]}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([15.0, 100.0, 10])


class RobotGripperDesign(OptimizationProblem):
    """
    Problem 13: Robot Gripper Design
    Minimize gripper force
    Variables: [link1, link2, link3, link4]
    """
    def __init__(self):
        super().__init__(
            "Robot Gripper Design",
            "Minimize gripper actuation force",
            4
        )

    def objective(self, x: np.ndarray) -> float:
        a, b, c, d = x
        # Force amplification (to be minimized)
        F_in = 100  # Input force
        return F_in * (a * c) / (b * d + 1e-6)

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(10.0, 150.0), (10.0, 150.0), (10.0, 200.0), (10.0, 200.0)]

    def get_constraints(self) -> List[Dict]:
        F_grip = 50  # Required grip force
        return [
            {'type': 'ineq', 'fun': lambda x: 100 * x[0] * x[2] / (x[1] * x[3] + 1e-6) - F_grip},
            {'type': 'ineq', 'fun': lambda x: x[0] + x[1] - 180},  # Total length constraint
            {'type': 'ineq', 'fun': lambda x: x[2] + x[3] - 250}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([50.0, 50.0, 100.0, 100.0])


class PistonLeverDesign(OptimizationProblem):
    """
    Problem 14: Piston Lever Design
    Minimize weight of piston lever
    Variables: [length, diameter, thickness, width]
    """
    def __init__(self):
        super().__init__(
            "Piston Lever Design",
            "Minimize weight of piston lever mechanism",
            4
        )

    def objective(self, x: np.ndarray) -> float:
        L, D, t, w = x
        rho = 7800
        # Weight of lever
        return rho * np.pi * D * t * L + rho * w * t * L * 0.5

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(10.0, 50.0), (5.0, 20.0), (1.0, 10.0), (5.0, 30.0)]

    def get_constraints(self) -> List[Dict]:
        F = 1000  # Force
        sigma_max = 150e6  # Max stress
        return [
            {'type': 'ineq', 'fun': lambda x: sigma_max - 32 * F * x[0] / (np.pi * x[1]**3 + 1e-6)},
            {'type': 'ineq', 'fun': lambda x: x[2] - 0.2 * x[1]}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([30.0, 10.0, 3.0, 15.0])


class CarSideImpactDesign(OptimizationProblem):
    """
    Problem 15: Car Side Impact Design (Simplified)
    Minimize weight of car side structure
    Variables: [thickness1, thickness2, thickness3]
    """
    def __init__(self):
        super().__init__(
            "Car Side Impact Design",
            "Minimize weight of car side impact structure",
            3
        )

    def objective(self, x: np.ndarray) -> float:
        # Total weight
        return 1.98 + 4.9 * x[0] + 6.67 * x[1] + 6.98 * x[2]

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(0.5, 1.5), (0.45, 1.35), (0.5, 1.5)]

    def get_constraints(self) -> List[Dict]:
        return [
            {'type': 'ineq', 'fun': lambda x: 32 - (1.16 - 0.3717 * x[1] * x[2] - 0.0092928 * x[2])},
            {'type': 'ineq', 'fun': lambda x: 32 - (0.261 - 0.0159 * x[0] * x[1] - 0.06486 * x[0])},
            {'type': 'ineq', 'fun': lambda x: 32 - 0.214}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([1.0, 0.9, 1.0])


class HeatExchangerDesign(OptimizationProblem):
    """
    Problem 16: Heat Exchanger Network Design
    Minimize total cost of heat exchanger
    Variables: [tube_diameter, tube_length, baffle_spacing]
    """
    def __init__(self):
        super().__init__(
            "Heat Exchanger Design",
            "Minimize cost of shell-and-tube heat exchanger",
            3
        )

    def objective(self, x: np.ndarray) -> float:
        D, L, B = x
        # Cost = Material + Pumping
        area = np.pi * D * L * 100  # 100 tubes
        return area * 50 + L * 10 + B * 5

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(0.01, 0.05), (1.0, 5.0), (0.1, 1.0)]

    def get_constraints(self) -> List[Dict]:
        Q_required = 100000  # Heat transfer required
        U = 500  # Overall heat transfer coefficient
        LMTD = 50  # Log mean temperature difference

        return [
            {'type': 'ineq', 'fun': lambda x: U * np.pi * x[0] * x[1] * 100 * LMTD - Q_required},
            {'type': 'ineq', 'fun': lambda x: x[1] / (x[2] + 1e-6) - 5},  # Minimum baffles
            {'type': 'ineq', 'fun': lambda x: 20 - x[1] / (x[2] + 1e-6)}  # Maximum baffles
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([0.025, 3.0, 0.3])


class TubularColumnDesign(OptimizationProblem):
    """
    Problem 17: Tubular Column Design
    Minimize weight of tubular column
    Variables: [diameter, thickness]
    """
    def __init__(self):
        super().__init__(
            "Tubular Column Design",
            "Minimize weight of tubular column under buckling",
            2
        )

    def objective(self, x: np.ndarray) -> float:
        D, t = x
        L = 3000  # Length in mm
        rho = 7800  # Density
        return np.pi * D * t * L * rho

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(50.0, 300.0), (2.0, 20.0)]

    def get_constraints(self) -> List[Dict]:
        P = 50000  # Load (N)
        E = 200e3  # Young's modulus (MPa)
        L = 3000  # Length (mm)
        sigma_y = 250  # Yield stress (MPa)

        return [
            # Buckling constraint
            {'type': 'ineq', 'fun': lambda x: np.pi**3 * E * (x[0]**4 - (x[0] - 2*x[1])**4) / (64 * L**2) - P},
            # Stress constraint
            {'type': 'ineq', 'fun': lambda x: sigma_y - P / (np.pi * x[0] * x[1] + 1e-6)},
            # Geometric constraint
            {'type': 'ineq', 'fun': lambda x: x[0] - 4 * x[1]}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([150.0, 10.0])


class DiscBrakeDesign(OptimizationProblem):
    """
    Problem 18: Disc Brake Design
    Minimize mass of brake disc
    Variables: [inner_radius, outer_radius, engaging_force, actuating_force]
    """
    def __init__(self):
        super().__init__(
            "Disc Brake Design",
            "Minimize mass of disc brake system",
            4
        )

    def objective(self, x: np.ndarray) -> float:
        ri, ro, F, s = x
        # Mass of disc
        rho = 7800
        thickness = 20  # mm
        return 4.9 * 1e-5 * (ro**2 - ri**2) * thickness * rho / 1000

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(55.0, 80.0), (75.0, 110.0), (90.0, 150.0), (2.5, 5.0)]

    def get_constraints(self) -> List[Dict]:
        Mf = 3.0  # Stopping time
        Iz = 55.0  # Mass moment of inertia
        mu = 0.5  # Friction coefficient
        n = 250  # Number of friction surfaces

        return [
            {'type': 'ineq', 'fun': lambda x: (x[1]**2 - x[0]**2) - 1000},
            {'type': 'ineq', 'fun': lambda x: 2.5 * (x[1]**2 - x[0]**2) - 3500},
            {'type': 'ineq', 'fun': lambda x: x[2] * x[3] * mu * (x[1]**3 - x[0]**3) / ((x[1]**2 - x[0]**2) + 1e-6) - Mf * Iz},
            {'type': 'ineq', 'fun': lambda x: x[1] - x[0] - 20}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([70.0, 90.0, 120.0, 3.5])


class CrashworthinessDesign(OptimizationProblem):
    """
    Problem 19: Vehicle Crashworthiness Design
    Minimize weight while maintaining crash safety
    Variables: [thickness1, thickness2, thickness3]
    """
    def __init__(self):
        super().__init__(
            "Crashworthiness Design",
            "Minimize vehicle weight for crash safety",
            3
        )

    def objective(self, x: np.ndarray) -> float:
        # Total mass
        return 1640.2823 + 2.3573285 * x[0] + 2.3220035 * x[1] + 4.5688768 * x[2]

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(1.0, 3.0), (1.0, 3.0), (1.0, 3.0)]

    def get_constraints(self) -> List[Dict]:
        return [
            {'type': 'ineq', 'fun': lambda x: 28 - (1.98 + 4.9 * x[0] + 6.67 * x[1] + 6.98 * x[2])},
            {'type': 'ineq', 'fun': lambda x: 33 - (2.354 + 4.1 * x[0] + 5.8 * x[1] + 7.5 * x[2])},
            {'type': 'ineq', 'fun': lambda x: 46 - (8.45 + 6.3 * x[0] + 7.8 * x[1] + 9.2 * x[2])}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([2.0, 2.0, 2.0])


class GasTransmissionCompressorDesign(OptimizationProblem):
    """
    Problem 20: Gas Transmission Compressor Design
    Minimize total cost of compressor
    Variables: [gear_ratio, shaft_diameter, shaft_length]
    """
    def __init__(self):
        super().__init__(
            "Gas Transmission Compressor",
            "Minimize cost of gas compressor system",
            3
        )

    def objective(self, x: np.ndarray) -> float:
        r, d, L = x
        # Total cost = gear cost + shaft cost + operational cost
        return 8.61 * 1e5 * r + 3.69 * 1e4 * d**2 * L + 2.5 * 1e4 * L

    def get_bounds(self) -> List[Tuple[float, float]]:
        return [(1.0, 5.0), (0.1, 0.5), (1.0, 5.0)]

    def get_constraints(self) -> List[Dict]:
        P = 1.5e6  # Power
        tau_max = 80e6  # Max shear stress
        omega = 3000 * 2 * np.pi / 60  # Angular velocity

        return [
            {'type': 'ineq', 'fun': lambda x: tau_max - 16 * P / (np.pi * x[1]**3 * omega * x[0] + 1e-6)},
            {'type': 'ineq', 'fun': lambda x: x[2] / (x[1] + 1e-6) - 20},  # Slenderness limit
            {'type': 'ineq', 'fun': lambda x: 100 - x[2] / (x[1] + 1e-6)}
        ]

    def get_initial_guess(self) -> np.ndarray:
        return np.array([2.5, 0.3, 3.0])


def get_all_problems():
    """Return all problem instances"""
    return [
        PressureVesselDesign(),
        WeldedBeamDesign(),
        SpringDesign(),
        SpeedReducerDesign(),
        ThreeBarTrussDesign(),
        TensionCompressionStringDesign(),
        CantileverBeamDesign(),
        SteppedCantileverBeam(),
        GearTrainDesign(),
        FlywheelDesign(),
        HydrostaticThrustBearingDesign(),
        RollingElementBearingDesign(),
        RobotGripperDesign(),
        PistonLeverDesign(),
        CarSideImpactDesign(),
        HeatExchangerDesign(),
        TubularColumnDesign(),
        DiscBrakeDesign(),
        CrashworthinessDesign(),
        GasTransmissionCompressorDesign()
    ]
