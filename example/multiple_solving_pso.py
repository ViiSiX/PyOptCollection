"""
Optimizing function: f(x) = x^4 + x^3 - 3x^2 + 1
Finding: min
Constraints:
- x^4 + x^3 -2x^2 + 2 >= 0
- x^4 + x^3 -2x^2 + 0.1 <= 0
"""

from py_opt_collection.optimization import Optimization, MultipleSolving
from py_opt_collection.pso import PSO


optimization = Optimization(
    optimizing_function=lambda x: x[0] ** 4 + x[0] ** 3 - 3 * (x[0] ** 2) + 1,
    boundaries=[
        (-3.0, 3.0)
    ],
    no_dimensions=1,
    find_max=True
)
optimization.add_constraint(lambda x: x[0]**4 + x[0]**3 - 2*(x[0] ** 2) + 2 >= 0)
optimization.add_constraint(lambda x: x[0]**4 + x[0]**3 - 2*(x[0] ** 2) + 0.1 <= 0)
pso = PSO(
    optimization_object=optimization,
    no_particles=10,
    no_iteration_steps=20,
    c_1=2.0,
    c_2=2.0
)

ms = MultipleSolving(pso, 10)
ms.run()
print(ms)
for r in ms.results_value_only:
    print(r)
