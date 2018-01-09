"""
Optimizing function: f(x) = (x^2 + y - 11)^2 + (x + y^2 -7)^2
Finding: min
Boundaries:
x: -5 -> 5
y: -5 -> 5
"""

from py_opt_collection.optimization import MultipleSolving
from py_opt_collection.pso import PSO
from py_opt_collection.test_functions import HIMMELBLAU


pso = PSO(
    optimization_object=HIMMELBLAU['optimization'],
    no_particles=140,
    no_iteration_steps=225,
    c_1=1.0520,
    c_2=0.8791
)

ms = MultipleSolving(pso, 10)
ms.run()
print(ms)
