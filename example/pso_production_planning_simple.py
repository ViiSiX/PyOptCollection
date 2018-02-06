"""
The problem is provided by IBM ILOG CPLEX Optimization Studio on their
knowledge center site. Information about formulas and constraints in this
module can be found there.
"""

from py_opt_collection.optimization import Optimization, MultipleSolving
from py_opt_collection.pso import PSO


# Maximize profit of a plan that produce Gaz and Chloride
# with the following rules
############
# Resource:
# - N: 50
# - H: 180
# - Cl: 40
# Price
# - Gaz: 40
# - Chloride: 50


def optimizing_function(x):
    """
    x[0]: 1st year gaz
    x[1]: 1st year gaz
    x[2]: 2nd year gaz
    x[3]: 2nd year gaz
    """

    return x[0] * 40 + x[1] * 50


def constraint(x):
    return (x[0] + x[1] <= 50) & \
           (x[0] * 3 + x[1] * 4 <= 180) & \
           (x[1] <= 40)


optimization = Optimization(
    optimizing_function=optimizing_function,
    boundaries=[(0, 100), (0, 100)],
    no_dimensions=2,
    find_max=True
)

optimization.add_constraint(constraint)

pso = PSO(
    optimization_object=optimization,
    no_particles=10,
    no_iteration_steps=20,
    c_1=2.0,
    c_2=2.0
)

ms = MultipleSolving(pso, 20)
ms.run()
print(ms)
