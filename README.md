# Constrained Optimization Algorithms Benchmark

A comprehensive benchmarking suite for state-of-the-art constrained optimization algorithms tested on mechanical engineering problems.

## Overview

This project implements and compares 10 advanced optimization algorithms on 20 real-world mechanical engineering optimization problems. It provides detailed performance metrics, convergence analysis, and visualization tools.

## Features

- **10 State-of-the-Art Optimization Algorithms**
- **20 Mechanical Engineering Problems**
- **Comprehensive Performance Analysis**
- **Convergence Plots**
- **Statistical Summaries**
- **Automated Benchmarking Framework**

## Algorithms Implemented

1. **SQP (Sequential Quadratic Programming)** - One of the most effective gradient-based methods
2. **Augmented Lagrangian** - Handles constraints through Lagrange multipliers and penalty terms
3. **Penalty Method** - Converts constrained to unconstrained optimization
4. **Interior Point Method** - Uses barrier functions for inequality constraints
5. **Trust Region Constrained** - Trust region approach for constrained problems
6. **Bayesian Optimization** - Black-box optimization using Gaussian Processes
7. **Particle Swarm Optimization** - Population-based metaheuristic with constraint handling
8. **Differential Evolution** - Evolutionary algorithm for global optimization
9. **Genetic Algorithm** - Evolutionary approach with tournament selection
10. **COBYLA** - Derivative-free constrained optimization

## Mechanical Engineering Problems

1. **Pressure Vessel Design** - Minimize cost of cylindrical pressure vessel
2. **Welded Beam Design** - Minimize cost of welded beam structure
3. **Spring Design** - Minimize weight of tension/compression spring
4. **Speed Reducer Design** - Minimize weight of speed reducer gearbox
5. **Three-Bar Truss Design** - Minimize volume of 3-bar truss structure
6. **Tension/Compression String** - Minimize volume of helical spring
7. **Cantilever Beam Design** - Minimize weight of cantilever beam
8. **Stepped Cantilever Beam** - Minimize volume of 5-segment beam
9. **Gear Train Design** - Minimize gear ratio error
10. **Flywheel Design** - Minimize mass for energy storage
11. **Hydrostatic Thrust Bearing** - Minimize power loss
12. **Rolling Element Bearing** - Minimize bearing volume
13. **Robot Gripper Design** - Minimize gripper actuation force
14. **Piston Lever Design** - Minimize weight of piston lever
15. **Car Side Impact Design** - Minimize weight of side structure
16. **Heat Exchanger Design** - Minimize cost of heat exchanger
17. **Tubular Column Design** - Minimize weight under buckling
18. **Disc Brake Design** - Minimize mass of brake disc
19. **Crashworthiness Design** - Minimize vehicle weight for crash safety
20. **Gas Transmission Compressor** - Minimize cost of compressor system

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd Opt-algorithms

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run Full Benchmark

```bash
python main.py
```

### Quick Test Mode

```bash
python main.py --quick
```

### Custom Configuration

```bash
python main.py --max-iter 1000 --timeout 600 --tol 1e-8
```

### Available Options

- `--max-iter N`: Maximum iterations per algorithm (default: 500)
- `--timeout N`: Timeout per run in seconds (default: 300)
- `--tol X`: Convergence tolerance (default: 1e-6)
- `--quick`: Quick test mode (fewer iterations, subset of problems)
- `--no-plots`: Skip generating plots

## Output

The benchmark generates:

1. **JSON Results File** (`results/benchmark_results_TIMESTAMP.json`)
   - Detailed results for each algorithm-problem combination
   - Objective values, constraint violations, computation time
   - Convergence histories

2. **Convergence Plots** (one per problem)
   - Shows how each algorithm converges over iterations
   - Saved as `results/convergence_PROBLEM_NAME.png`

3. **Performance Heatmaps**
   - `heatmap_objective_value.png` - Algorithm performance across problems
   - `heatmap_time_seconds.png` - Computation time comparison

4. **Statistical Plots**
   - `success_rates.png` - Success and feasibility rates
   - `computation_times.png` - Average computation time per algorithm
   - `objective_comparison_boxplots.png` - Distribution of objective values

5. **Console Summary**
   - Overall statistics
   - Algorithm performance rankings
   - Problem difficulty assessment

## Project Structure

```
Opt-algorithms/
├── algorithms/              # Optimization algorithm implementations
│   ├── __init__.py
│   ├── base.py             # Base optimizer class
│   ├── sequential_quadratic_programming.py
│   ├── augmented_lagrangian.py
│   ├── penalty_method.py
│   ├── interior_point.py
│   ├── trust_region_constrained.py
│   ├── bayesian_optimization.py
│   ├── particle_swarm_constrained.py
│   ├── differential_evolution_constrained.py
│   ├── genetic_algorithm_constrained.py
│   └── cobyla.py
├── problems/               # Optimization problem definitions
│   ├── __init__.py
│   └── mechanical_engineering.py
├── benchmarking/           # Benchmarking framework
│   ├── __init__.py
│   ├── runner.py          # Benchmark execution
│   └── visualization.py   # Plotting utilities
├── results/               # Output directory (created automatically)
├── main.py               # Main execution script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Example Results

After running the benchmark, you can expect output like:

```
================================================================================
BENCHMARK SUMMARY
================================================================================

Overall Statistics:
  Total Runs: 200
  Successful: 185 (92.5%)
  Feasible: 178 (89.0%)
  Average Time: 12.45s
  Total Time: 2490.23s

--------------------------------------------------------------------------------
Algorithm Performance:
--------------------------------------------------------------------------------
Algorithm                           Success Rate    Avg Objective      Avg Time
--------------------------------------------------------------------------------
SQP (Sequential Quadratic...)        95.0%         2.345678e+03       8.23s
Augmented Lagrangian                 90.0%         2.456789e+03      15.67s
...
```

## Performance Metrics

Each algorithm is evaluated on:

- **Success Rate**: Percentage of successful optimizations
- **Feasibility Rate**: Percentage of solutions satisfying constraints
- **Objective Value**: Quality of solution found
- **Computation Time**: Average time to convergence
- **Function Evaluations**: Number of objective function calls
- **Convergence Speed**: How quickly the algorithm approaches optimum

## Customization

### Adding New Algorithms

1. Create a new file in `algorithms/`
2. Inherit from `BaseOptimizer`
3. Implement the `optimize` method
4. Add to `algorithms/__init__.py`

### Adding New Problems

1. Add a new class to `problems/mechanical_engineering.py`
2. Inherit from `OptimizationProblem`
3. Implement required methods: `objective`, `get_bounds`, `get_constraints`, `get_initial_guess`
4. Add to `get_all_problems()` function

## Requirements

- Python 3.7+
- NumPy
- SciPy
- Matplotlib
- Seaborn

## License

This project is provided for educational and research purposes.

## Citation

If you use this benchmarking suite in your research, please cite:

```
@software{opt_algorithms_benchmark,
  title={Constrained Optimization Algorithms Benchmark},
  author={Your Name},
  year={2024},
  description={Benchmark suite for constrained optimization algorithms on mechanical engineering problems}
}
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests with:
- New optimization algorithms
- Additional benchmark problems
- Performance improvements
- Bug fixes
- Documentation enhancements

## Contact

For questions or issues, please open an issue on the repository.
