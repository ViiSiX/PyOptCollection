"""
Optimizing function: f(x) = (1 - x)^2 + 100(y - x^2)^2
Finding: min
Boundaries:
- x: -3 -> 3
- y: -3 -> 3
"""

import argparse
import statistics
import csv
from py_opt_collection.optimization import MultipleSolving
from py_opt_collection.pso import PSO
from py_opt_collection.test_functions import ROSENBROCK
from multiprocessing.dummy import Pool


def calculate_success_rate(results, max_error=0.001):
    total_success = 0
    for r in results:
        if abs(r - ROSENBROCK['results'][0][0]) <= max_error:
            total_success += 1
    return total_success/float(len(results))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test optimization for'
                                                 'Rosenbrock function.')
    parser.add_argument('-a', '--algorithm', required=True)
    parser.add_argument('-o', '--output-file', required=True,
                        type=argparse.FileType('w'))
    args = parser.parse_args()

    if args.algorithm.lower() == 'pso':
        test_cases = []
        general_c1 = general_c2 = 2.0
        no_particles_suite = [10, 20, 50, 100]
        no_iter_steps_suite = [10, 20, 50, 100]
        for p in no_particles_suite:
            for i in no_iter_steps_suite:
                test_cases.append({
                    'no_particles': p, 'no_iteration_steps': i,
                    'c_1': general_c1, 'c_2': general_c2
                })

        writer = csv.writer(args.output_file)
        writer.writerow(['#Particles', '#IterSteps', 'Mean',
                         'Median', 'StdDev', 'SuccessRate'])

        for test_case in test_cases:
            pso = PSO(
                optimization_object=ROSENBROCK['optimization'],
                **test_case
            )
            ms = MultipleSolving(pso, 200)
            ms.run(Pool())
            writer.writerow([
                # Particles
                test_case['no_particles'],
                # IterSteps
                test_case['no_iteration_steps'],
                # Mean
                statistics.mean(ms.results_value_only),
                # Median
                statistics.median(ms.results_value_only),
                # StdDev
                statistics.stdev(ms.results_value_only),
                # SuccessRate
                calculate_success_rate(ms.results_value_only, max_error=0.05)
            ])

        args.output_file.close()
