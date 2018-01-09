"""
This is an example using PSO to solve a problem. Very simple ones.

Optimizing function: f(x) = 2x sin(x^2)
Finding: max
No constraints
"""

import math
from py_opt_collection.optimization import Optimization, MultipleSolving
from py_opt_collection.pso import PSO


optimization = Optimization(
    optimizing_function=lambda x: 2 * x[0] * math.sin(x[0] ** 2),
    boundaries=[
        (-3.0, 3.0)
    ],
    no_dimensions=1,
    find_max=True
)
pso = PSO(
    optimization_object=optimization,
    no_particles=45,
    no_iteration_steps=20,
    c_1=2.99,
    c_2=1.81
)
print(pso.solve())

ms = MultipleSolving(pso, 20)
ms.run()
print(ms)
print(ms.results_value_only)
