"""
Benchmark Visualization
Creates convergence plots and performance comparisons
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from typing import List, Dict
import seaborn as sns


class BenchmarkVisualizer:
    """Creates visualizations for benchmark results"""

    def __init__(self, results, output_dir='results'):
        """
        Initialize visualizer

        Args:
            results: List of result dictionaries from BenchmarkRunner
            output_dir: Directory to save plots
        """
        self.results = results
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")

    def plot_convergence_by_problem(self, problem_name, save=True):
        """
        Plot convergence curves for all algorithms on a specific problem

        Args:
            problem_name: Name of the problem
            save: Whether to save the plot
        """
        # Filter results for this problem
        problem_results = [r for r in self.results if r['problem'] == problem_name]

        if not problem_results:
            print(f"No results found for problem: {problem_name}")
            return

        fig, ax = plt.subplots(figsize=(12, 8))

        for result in problem_results:
            if result['convergence_history'] and result['feasible']:
                history = result['convergence_history']
                # Use log scale if values span multiple orders of magnitude
                ax.plot(history, label=result['algorithm'], linewidth=2, alpha=0.8)

        ax.set_xlabel('Function Evaluations', fontsize=12)
        ax.set_ylabel('Objective Value', fontsize=12)
        ax.set_title(f'Convergence Comparison: {problem_name}', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_yscale('log')

        plt.tight_layout()

        if save:
            filename = f"convergence_{problem_name.replace(' ', '_')}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")

        plt.close()

    def plot_all_convergences(self):
        """Plot convergence curves for all problems"""
        problems = list(set(r['problem'] for r in self.results))

        print(f"\nGenerating {len(problems)} convergence plots...")
        for i, problem in enumerate(problems, 1):
            print(f"  [{i}/{len(problems)}] {problem}")
            self.plot_convergence_by_problem(problem)

    def plot_performance_heatmap(self, metric='objective_value', save=True):
        """
        Create a heatmap showing algorithm performance across problems

        Args:
            metric: Metric to visualize ('objective_value', 'time_seconds', 'iterations')
            save: Whether to save the plot
        """
        # Get unique algorithms and problems
        algorithms = sorted(list(set(r['algorithm'] for r in self.results)))
        problems = sorted(list(set(r['problem'] for r in self.results)))

        # Create matrix
        matrix = np.zeros((len(problems), len(algorithms)))

        for i, problem in enumerate(problems):
            for j, algorithm in enumerate(algorithms):
                # Get results for this combination
                matching = [r for r in self.results
                            if r['problem'] == problem and r['algorithm'] == algorithm]

                if matching:
                    # Use mean if multiple repetitions
                    values = [r[metric] for r in matching if r['feasible']]
                    if values:
                        if metric == 'objective_value':
                            # Use log scale for objective values
                            matrix[i, j] = np.log10(np.mean(values) + 1e-10)
                        else:
                            matrix[i, j] = np.mean(values)
                    else:
                        matrix[i, j] = np.nan
                else:
                    matrix[i, j] = np.nan

        # Create heatmap
        fig, ax = plt.subplots(figsize=(14, 10))

        # Truncate long names for display
        display_problems = [p[:30] + '...' if len(p) > 30 else p for p in problems]
        display_algorithms = [a[:25] + '...' if len(a) > 25 else a for a in algorithms]

        im = ax.imshow(matrix, cmap='viridis', aspect='auto')

        # Set ticks
        ax.set_xticks(np.arange(len(algorithms)))
        ax.set_yticks(np.arange(len(problems)))
        ax.set_xticklabels(display_algorithms, rotation=45, ha='right', fontsize=9)
        ax.set_yticklabels(display_problems, fontsize=9)

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        if metric == 'objective_value':
            cbar.set_label('log10(Objective Value)', fontsize=11)
            title = 'Algorithm Performance: log10(Objective Value)'
        elif metric == 'time_seconds':
            cbar.set_label('Time (seconds)', fontsize=11)
            title = 'Algorithm Performance: Computation Time'
        else:
            cbar.set_label(metric.replace('_', ' ').title(), fontsize=11)
            title = f'Algorithm Performance: {metric.replace("_", " ").title()}'

        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()

        if save:
            filename = f"heatmap_{metric}.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")

        plt.close()

    def plot_success_rate_comparison(self, save=True):
        """
        Plot success rates for each algorithm

        Args:
            save: Whether to save the plot
        """
        algorithms = sorted(list(set(r['algorithm'] for r in self.results)))

        success_rates = []
        feasible_rates = []

        for algo in algorithms:
            algo_results = [r for r in self.results if r['algorithm'] == algo]
            total = len(algo_results)
            successful = sum(1 for r in algo_results if r['success'])
            feasible = sum(1 for r in algo_results if r['feasible'])

            success_rates.append(100 * successful / total if total > 0 else 0)
            feasible_rates.append(100 * feasible / total if total > 0 else 0)

        # Truncate long names
        display_names = [a[:30] + '...' if len(a) > 30 else a for a in algorithms]

        fig, ax = plt.subplots(figsize=(12, 8))

        x = np.arange(len(algorithms))
        width = 0.35

        ax.bar(x - width/2, success_rates, width, label='Success Rate', alpha=0.8)
        ax.bar(x + width/2, feasible_rates, width, label='Feasibility Rate', alpha=0.8)

        ax.set_xlabel('Algorithm', fontsize=12)
        ax.set_ylabel('Rate (%)', fontsize=12)
        ax.set_title('Algorithm Success and Feasibility Rates', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(display_names, rotation=45, ha='right', fontsize=9)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim(0, 105)

        plt.tight_layout()

        if save:
            filename = "success_rates.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")

        plt.close()

    def plot_computation_time_comparison(self, save=True):
        """
        Plot average computation time for each algorithm

        Args:
            save: Whether to save the plot
        """
        algorithms = sorted(list(set(r['algorithm'] for r in self.results)))

        avg_times = []
        std_times = []

        for algo in algorithms:
            algo_results = [r for r in self.results if r['algorithm'] == algo]
            times = [r['time_seconds'] for r in algo_results]
            avg_times.append(np.mean(times))
            std_times.append(np.std(times))

        # Truncate long names
        display_names = [a[:30] + '...' if len(a) > 30 else a for a in algorithms]

        fig, ax = plt.subplots(figsize=(12, 8))

        x = np.arange(len(algorithms))
        ax.bar(x, avg_times, yerr=std_times, capsize=5, alpha=0.8)

        ax.set_xlabel('Algorithm', fontsize=12)
        ax.set_ylabel('Average Time (seconds)', fontsize=12)
        ax.set_title('Average Computation Time by Algorithm', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(display_names, rotation=45, ha='right', fontsize=9)
        ax.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()

        if save:
            filename = "computation_times.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")

        plt.close()

    def plot_objective_comparison_by_problem(self, save=True):
        """
        Create box plots comparing algorithm performance on each problem

        Args:
            save: Whether to save the plot
        """
        problems = sorted(list(set(r['problem'] for r in self.results)))[:5]  # Limit to 5 for readability

        fig, axes = plt.subplots(len(problems), 1, figsize=(14, 4 * len(problems)))
        if len(problems) == 1:
            axes = [axes]

        for idx, problem in enumerate(problems):
            problem_results = [r for r in self.results
                               if r['problem'] == problem and r['feasible']]

            if not problem_results:
                continue

            # Group by algorithm
            algorithms = sorted(list(set(r['algorithm'] for r in problem_results)))
            data = []
            labels = []

            for algo in algorithms:
                values = [r['objective_value'] for r in problem_results
                          if r['algorithm'] == algo]
                if values:
                    data.append(values)
                    labels.append(algo[:25] + '...' if len(algo) > 25 else algo)

            if data:
                axes[idx].boxplot(data, labels=labels)
                axes[idx].set_ylabel('Objective Value', fontsize=11)
                axes[idx].set_title(problem, fontsize=12, fontweight='bold')
                axes[idx].tick_params(axis='x', rotation=45, labelsize=9)
                axes[idx].grid(True, alpha=0.3, axis='y')
                axes[idx].set_yscale('log')

        plt.tight_layout()

        if save:
            filename = "objective_comparison_boxplots.png"
            filepath = os.path.join(self.output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Saved: {filepath}")

        plt.close()

    def generate_all_plots(self):
        """Generate all visualization plots"""
        print("\n" + "="*80)
        print("Generating Visualizations")
        print("="*80 + "\n")

        print("1. Convergence plots for all problems...")
        self.plot_all_convergences()

        print("\n2. Performance heatmap (objective values)...")
        self.plot_performance_heatmap('objective_value')

        print("\n3. Performance heatmap (computation time)...")
        self.plot_performance_heatmap('time_seconds')

        print("\n4. Success rate comparison...")
        self.plot_success_rate_comparison()

        print("\n5. Computation time comparison...")
        self.plot_computation_time_comparison()

        print("\n6. Objective value comparison (box plots)...")
        self.plot_objective_comparison_by_problem()

        print("\n" + "="*80)
        print("All visualizations generated!")
        print("="*80 + "\n")
