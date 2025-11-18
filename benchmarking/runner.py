"""
Benchmark Runner
Executes optimization algorithms on test problems and collects results
"""

import numpy as np
import time
import json
from typing import List, Dict
from datetime import datetime
import os


class BenchmarkRunner:
    """Runs optimization algorithms on test problems and collects results"""

    def __init__(self, algorithms, problems, results_dir='results'):
        """
        Initialize benchmark runner

        Args:
            algorithms: List of optimizer instances
            problems: List of problem instances
            results_dir: Directory to save results
        """
        self.algorithms = algorithms
        self.problems = problems
        self.results_dir = results_dir
        self.results = []

        # Create results directory if it doesn't exist
        os.makedirs(results_dir, exist_ok=True)

    def run_single(self, algorithm, problem, max_iter=1000, tol=1e-6, timeout=300):
        """
        Run a single algorithm on a single problem

        Args:
            algorithm: Optimizer instance
            problem: Problem instance
            max_iter: Maximum iterations
            tol: Tolerance
            timeout: Timeout in seconds

        Returns:
            Dictionary with results
        """
        print(f"  Running {algorithm.name} on {problem.name}...")

        # Get problem details
        x0 = problem.get_initial_guess()
        bounds = problem.get_bounds()
        constraints = problem.get_constraints()

        # Run optimization with timeout
        start_time = time.time()
        try:
            result = algorithm.optimize(
                objective=problem.objective,
                x0=x0,
                bounds=bounds,
                constraints=constraints,
                max_iter=max_iter,
                tol=tol
            )
            elapsed_time = time.time() - start_time

            # Check if timeout exceeded
            if elapsed_time > timeout:
                result.success = False
                result.message = "Timeout exceeded"

        except Exception as e:
            elapsed_time = time.time() - start_time
            result = type('obj', (object,), {
                'x': x0,
                'fun': problem.objective(x0),
                'success': False,
                'message': f"Error: {str(e)}",
                'nit': 0,
                'nfev': 0,
                'history': []
            })()

        # Evaluate constraint violations at final solution
        constraint_violation = 0.0
        is_feasible = True
        if constraints:
            for constraint in constraints:
                c_val = constraint['fun'](result.x)
                if constraint['type'] == 'ineq':
                    if c_val < -1e-6:
                        constraint_violation += abs(c_val)
                        is_feasible = False
                else:  # 'eq'
                    if abs(c_val) > 1e-6:
                        constraint_violation += abs(c_val)
                        is_feasible = False

        # Store results (ensure all values are JSON serializable)
        result_dict = {
            'algorithm': algorithm.name,
            'problem': problem.name,
            'success': bool(result.success),
            'feasible': bool(is_feasible),
            'objective_value': float(result.fun),
            'constraint_violation': float(constraint_violation),
            'iterations': int(result.nit),
            'function_evaluations': int(result.nfev),
            'time_seconds': float(elapsed_time),
            'convergence_history': [float(h) for h in result.history] if result.history else [],
            'final_solution': result.x.tolist(),
            'message': str(result.message)
        }

        return result_dict

    def run_all(self, max_iter=1000, tol=1e-6, timeout=300, repetitions=1):
        """
        Run all algorithms on all problems

        Args:
            max_iter: Maximum iterations per run
            tol: Tolerance
            timeout: Timeout per run in seconds
            repetitions: Number of times to repeat each combination

        Returns:
            List of result dictionaries
        """
        print(f"\n{'='*80}")
        print(f"Starting Benchmark: {len(self.algorithms)} algorithms × {len(self.problems)} problems")
        print(f"{'='*80}\n")

        self.results = []
        total_runs = len(self.algorithms) * len(self.problems) * repetitions
        current_run = 0

        for problem in self.problems:
            print(f"\nProblem: {problem.name}")
            print(f"{'-'*80}")

            for algorithm in self.algorithms:
                for rep in range(repetitions):
                    current_run += 1
                    print(f"  [{current_run}/{total_runs}] ", end='')

                    result = self.run_single(
                        algorithm=algorithm,
                        problem=problem,
                        max_iter=max_iter,
                        tol=tol,
                        timeout=timeout
                    )
                    result['repetition'] = rep
                    self.results.append(result)

                    # Print brief result
                    status = "✓" if result['success'] and result['feasible'] else "✗"
                    print(f"    {status} f={result['objective_value']:.6e} ({result['time_seconds']:.2f}s)")

        print(f"\n{'='*80}")
        print(f"Benchmark Complete!")
        print(f"{'='*80}\n")

        return self.results

    def save_results(self, filename=None):
        """Save results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}.json"

        filepath = os.path.join(self.results_dir, filename)

        with open(filepath, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'num_algorithms': len(self.algorithms),
                'num_problems': len(self.problems),
                'results': self.results
            }, f, indent=2)

        print(f"Results saved to: {filepath}")
        return filepath

    def get_summary_statistics(self):
        """Generate summary statistics from results"""
        if not self.results:
            return None

        summary = {
            'by_algorithm': {},
            'by_problem': {},
            'overall': {}
        }

        # Group by algorithm
        for algo_name in set(r['algorithm'] for r in self.results):
            algo_results = [r for r in self.results if r['algorithm'] == algo_name]
            summary['by_algorithm'][algo_name] = {
                'total_runs': len(algo_results),
                'successful_runs': sum(1 for r in algo_results if r['success']),
                'feasible_runs': sum(1 for r in algo_results if r['feasible']),
                'avg_objective': np.mean([r['objective_value'] for r in algo_results if r['feasible']]) if any(r['feasible'] for r in algo_results) else float('inf'),
                'avg_time': np.mean([r['time_seconds'] for r in algo_results]),
                'avg_iterations': np.mean([r['iterations'] for r in algo_results]),
                'avg_function_evaluations': np.mean([r['function_evaluations'] for r in algo_results])
            }

        # Group by problem
        for prob_name in set(r['problem'] for r in self.results):
            prob_results = [r for r in self.results if r['problem'] == prob_name]
            summary['by_problem'][prob_name] = {
                'total_runs': len(prob_results),
                'successful_runs': sum(1 for r in prob_results if r['success']),
                'feasible_runs': sum(1 for r in prob_results if r['feasible']),
                'best_objective': min([r['objective_value'] for r in prob_results if r['feasible']]) if any(r['feasible'] for r in prob_results) else float('inf'),
                'worst_objective': max([r['objective_value'] for r in prob_results if r['feasible']]) if any(r['feasible'] for r in prob_results) else float('inf')
            }

        # Overall statistics
        summary['overall'] = {
            'total_runs': len(self.results),
            'successful_runs': sum(1 for r in self.results if r['success']),
            'feasible_runs': sum(1 for r in self.results if r['feasible']),
            'avg_time': np.mean([r['time_seconds'] for r in self.results]),
            'total_time': sum(r['time_seconds'] for r in self.results)
        }

        return summary

    def print_summary(self):
        """Print a formatted summary of results"""
        summary = self.get_summary_statistics()
        if not summary:
            print("No results to summarize")
            return

        print("\n" + "="*80)
        print("BENCHMARK SUMMARY")
        print("="*80)

        print("\nOverall Statistics:")
        print(f"  Total Runs: {summary['overall']['total_runs']}")
        print(f"  Successful: {summary['overall']['successful_runs']} ({100*summary['overall']['successful_runs']/summary['overall']['total_runs']:.1f}%)")
        print(f"  Feasible: {summary['overall']['feasible_runs']} ({100*summary['overall']['feasible_runs']/summary['overall']['total_runs']:.1f}%)")
        print(f"  Average Time: {summary['overall']['avg_time']:.2f}s")
        print(f"  Total Time: {summary['overall']['total_time']:.2f}s")

        print("\n" + "-"*80)
        print("Algorithm Performance:")
        print("-"*80)
        print(f"{'Algorithm':<35} {'Success Rate':<15} {'Avg Objective':<15} {'Avg Time':<10}")
        print("-"*80)
        for algo_name, stats in sorted(summary['by_algorithm'].items()):
            success_rate = 100 * stats['feasible_runs'] / stats['total_runs']
            avg_obj = stats['avg_objective']
            avg_time = stats['avg_time']
            print(f"{algo_name:<35} {success_rate:>6.1f}%{'':<8} {avg_obj:>14.6e} {avg_time:>9.2f}s")

        print("\n" + "-"*80)
        print("Problem Difficulty:")
        print("-"*80)
        print(f"{'Problem':<35} {'Success Rate':<15} {'Best Objective':<20}")
        print("-"*80)
        for prob_name, stats in sorted(summary['by_problem'].items()):
            success_rate = 100 * stats['feasible_runs'] / stats['total_runs']
            best_obj = stats['best_objective']
            print(f"{prob_name:<35} {success_rate:>6.1f}%{'':<8} {best_obj:>19.6e}")

        print("="*80 + "\n")
