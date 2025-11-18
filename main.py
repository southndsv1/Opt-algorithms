"""
Main script to run comprehensive optimization algorithm benchmark

This script:
1. Loads 10 state-of-the-art optimization algorithms
2. Loads 20 mechanical engineering optimization problems
3. Runs all algorithms on all problems
4. Generates convergence plots
5. Generates performance summaries
"""

import sys
import argparse
from datetime import datetime

# Import algorithms
from algorithms import (
    SQP,
    AugmentedLagrangian,
    PenaltyMethod,
    InteriorPoint,
    TrustRegionConstrained,
    BayesianOpt,
    ParticleSwarmConstrained,
    DifferentialEvolutionConstrained,
    GeneticAlgorithmConstrained,
    COBYLA
)

# Import problems
from problems import get_all_problems

# Import benchmarking tools
from benchmarking import BenchmarkRunner, BenchmarkVisualizer


def main():
    """Main function to run the benchmark"""

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run optimization algorithm benchmark')
    parser.add_argument('--max-iter', type=int, default=500,
                        help='Maximum iterations per algorithm (default: 500)')
    parser.add_argument('--timeout', type=int, default=300,
                        help='Timeout per run in seconds (default: 300)')
    parser.add_argument('--tol', type=float, default=1e-6,
                        help='Convergence tolerance (default: 1e-6)')
    parser.add_argument('--quick', action='store_true',
                        help='Quick test mode (fewer iterations, subset of problems)')
    parser.add_argument('--no-plots', action='store_true',
                        help='Skip generating plots')
    args = parser.parse_args()

    # Adjust settings for quick mode
    if args.quick:
        print("\n*** QUICK TEST MODE ***\n")
        max_iter = 100
        timeout = 60
        problem_limit = 5
    else:
        max_iter = args.max_iter
        timeout = args.timeout
        problem_limit = None

    print("="*80)
    print(" "*20 + "OPTIMIZATION ALGORITHM BENCHMARK")
    print("="*80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Max Iterations: {max_iter}")
    print(f"Timeout: {timeout}s")
    print(f"Tolerance: {args.tol}")
    print("="*80 + "\n")

    # Initialize algorithms
    print("Initializing algorithms...")
    algorithms = [
        SQP(),
        AugmentedLagrangian(),
        PenaltyMethod(),
        InteriorPoint(),
        TrustRegionConstrained(),
        BayesianOpt(),
        ParticleSwarmConstrained(),
        DifferentialEvolutionConstrained(),
        GeneticAlgorithmConstrained(),
        COBYLA()
    ]
    print(f"  ✓ Loaded {len(algorithms)} algorithms")

    # Initialize problems
    print("\nInitializing problems...")
    all_problems = get_all_problems()
    if problem_limit:
        problems = all_problems[:problem_limit]
        print(f"  ✓ Loaded {len(problems)} problems (limited from {len(all_problems)} for quick test)")
    else:
        problems = all_problems
        print(f"  ✓ Loaded {len(problems)} problems")

    # Print algorithm list
    print("\nAlgorithms:")
    for i, algo in enumerate(algorithms, 1):
        print(f"  {i:2d}. {algo.name}")

    # Print problem list
    print("\nProblems:")
    for i, prob in enumerate(problems, 1):
        print(f"  {i:2d}. {prob.name} ({prob.dim}D)")

    # Create benchmark runner
    runner = BenchmarkRunner(algorithms, problems)

    # Run benchmark
    try:
        results = runner.run_all(
            max_iter=max_iter,
            tol=args.tol,
            timeout=timeout
        )

        # Save results
        print("\nSaving results...")
        results_file = runner.save_results()

        # Print summary
        runner.print_summary()

        # Generate visualizations
        if not args.no_plots:
            visualizer = BenchmarkVisualizer(results)
            visualizer.generate_all_plots()
        else:
            print("\nSkipping plot generation (--no-plots flag set)")

        print("\n" + "="*80)
        print(" "*25 + "BENCHMARK COMPLETE!")
        print("="*80)
        print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Results saved to: {results_file}")
        if not args.no_plots:
            print(f"Plots saved to: results/")
        print("="*80 + "\n")

        return 0

    except KeyboardInterrupt:
        print("\n\nBenchmark interrupted by user!")
        print("Partial results may have been saved.")
        return 1

    except Exception as e:
        print(f"\n\nERROR: Benchmark failed with exception:")
        print(f"  {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
