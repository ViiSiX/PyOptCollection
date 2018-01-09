"""
Optimizing function: f(x) = (1 - x)^2 + 100(y - x^2)^2
Finding: min
Boundaries:
- x: -3 -> 3
- y: -3 -> 3
"""

from py_opt_collection.optimization import MultipleSolving
from py_opt_collection.pso import PSO
from py_opt_collection.test_functions import ROSENBROCK
from multiprocessing.dummy import Pool


pso = PSO(
    optimization_object=ROSENBROCK['optimization'],
    no_particles=100,
    no_iteration_steps=230,
    c_1=1.222,
    c_2=1.542
)

ms = MultipleSolving(pso, 10)
ms.run(Pool())
print(ms)
