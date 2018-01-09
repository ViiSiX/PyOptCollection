import math
from py_opt_collection.optimization import Optimization, MultipleSolving
from py_opt_collection.pso import PSO


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


# 1st year:
############
# Resource:
# - N: 5000
# - H: 18000
# - Cl: 8000
# Price
# Gaz: 40
# Chloride: 50

# 2nd year:
############
# Resource:
# - N: 6000
# - H: 15000
# - Cl: 6000
# Price
# Gaz: 50
# Chloride: 60


# Variable declare
amount_n = {'1': 5000, '2': 6000}
amount_h = {'1': 18600, '2': 15000}
amount_cl = {'1': 2000, '2': 2000}
price_gaz = {'1': 100, '2': 110}
prize_chloride = {'1': 80, '2': 80}


# 2nd year
############


def second_year_leftover(x):
    """
    x[0]: 1st year gaz
    x[1]: 1st year gaz
    x[2]: 2nd year gaz
    x[3]: 2nd year gaz
    """

    return {
        'n': amount_n['1'] - (x[0] + x[1]),
        'h': amount_h['1'] - (x[0] * 3 + x[1] * 4),
        'cl': amount_cl['1'] - x[1]
    }


def optimizing_function(x):
    """
    x[0]: 1st year gaz
    x[1]: 1st year gaz
    x[2]: 2nd year gaz
    x[3]: 2nd year gaz
    """

    # return math.log(x[0], 2) * price_gaz['1'] + \
    #     math.log(x[1], 2) * prize_chloride['1'] + \
    #     math.log(x[2], 2) * price_gaz['2'] + \
    #     math.log(x[3], 2) * prize_chloride['2']
    # return x[0] * price_gaz['1'] + \
    #     x[1] * prize_chloride['1'] + \
    #     x[2] * price_gaz['2'] + \
    #     x[3] * prize_chloride['2']
    total_1st_year = x[0] * price_gaz['1'] + x[1] * price_gaz['1']
    total_2nd_year = x[2] * price_gaz['2'] + x[3] * price_gaz['2']
    return total_1st_year + total_2nd_year


def constraint_1st(x):
    return (x[0] + x[1] <= amount_n['1']) & \
           (x[0] * 3 + x[1] * 4 <= amount_h['1']) & \
           (x[1] <= amount_cl['1'])


def constraint_2nd(x):
    leftover = second_year_leftover(x)
    return (x[2] + x[3] <= amount_n['2'] + leftover['n']) & \
           (x[2] * 3 + x[3] * 4 <= amount_h['2'] + leftover['h']) & \
           (x[3] <= amount_cl['2'] + leftover['cl'])


optimization_2nd = Optimization(
    optimizing_function=optimizing_function,
    boundaries=[
        (1000.0, 10000.0),
        (1000.0, 10000.0),
        (1500.0, 10000.0),
        (1500.0, 10000.0),
    ],
    no_dimensions=4,
    find_max=True
)
optimization_2nd.add_constraint(constraint_1st)
optimization_2nd.add_constraint(constraint_2nd)

pso = PSO(
    optimization_object=optimization_2nd,
    no_particles=40,
    no_iteration_steps=40,
    c_1=4.0,
    c_2=2.0
)
print(pso.solve())

ms = MultipleSolving(pso, 20)
ms.run()
print(ms)
