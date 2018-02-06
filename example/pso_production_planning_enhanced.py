"""
This example is two expansions of the problem in
example/pso_simple_production_planning.py.
While the first case turns our simple problem into an non-linear ones,
the second case keeps its linearity, however expands its search space
into an 6-dimensional problem. Both examples show the advantages of PSO
on optimizing problems in non-linear and large search space.
"""

import math
from py_opt_collection.optimization import Optimization, MultipleSolving
from py_opt_collection.pso import PSO


# Class(es)
class ProducePeriod(object):
    """
    Represent one period of production, which intakes an amount of resources
    at the beginning and leaves leftover at the end of the period.
    """
    def __init__(self, resources,
                 predicted_prices,
                 profit_calculator,
                 last_period=None):
        """
        :param resources: list of resources prepared at the start of period.
        :type resources: list(float)
        :param predicted_prices: list of predicted products' prices.
        :type predicted_prices: list(float)
        :param profit_calculator: A function take products' quantities and
        return a total profit.
        :type profit_calculator: (list(float)) -> float
        :param last_period: last produce period which may has some leftover
        resources.
        :type last_period: ProducePeriod
        """
        self.resources = resources
        self.predicted_prices = predicted_prices
        self.profit_calculator = profit_calculator
        self.last_period = last_period
        self.resource_consumers = list()

    def add_consumer(self, consumer):
        """
        :type consumer: (list(float)) -> float
        """
        self.resource_consumers.append(consumer)

    def calculate_profit(self, products_quantities):
        """
        Calculate the total profit of this period.

        :param products_quantities: list of products' quantities will be
        produce in this period.
        :type products_quantities: list(float)
        :return: total profit.
        :rtype: float
        """
        if self.last_period:
            total_profit = \
                self.last_period.calculate_profit(
                    products_quantities[len(self.predicted_prices):]
                )
        else:
            total_profit = 0.0
        total_profit += self.profit_calculator(
            products_quantities[0:len(self.predicted_prices)],
            self.predicted_prices
        )
        return total_profit

    def _consume(self, products_quantities):
        if self.last_period:
            result, last_left_over = self.last_period._consume(
                products_quantities[len(self.predicted_prices):]
            )
        else:
            result = True
            last_left_over = [0.0] * len(self.resources)
        if not result:
            return False, None
        left_over = list()
        for i in range(len(self.resources)):
            left_over.append(self.resource_consumers[i](
                products_quantities[0:len(self.predicted_prices)],
                self.resources[i] + last_left_over[i]
            ))
            result &= left_over[i] >= 0.0

        return result, left_over

    def check_consumption(self, products_quantities):
        """
        :param products_quantities: list of products' quantities will be
        produce in this period.
        :type products_quantities: list(float)
        :return: products' quantities meet the constraints or not.
        :rtype: bool
        """
        return self._consume(products_quantities)[0]


# 1st case: 2 years production planning with non-linear profit model.
def profit_calculator_1st(x, prices):
    """
    :type x: list(float)
    :type prices: list(float)
    :rtype: float
    """
    if len(x) == len(prices):
        total = 0.0
        for i in range(len(x)):
            total += math.log(x[i], 10) ** 2 * prices[i] * 10
        return total
    else:
        raise ValueError("Mismatch number of products' quantities and price!")


def consumer_1st_n(x, resource):
    """
    :type x: list(float)
    :type resource: float
    :rtype: float
    """
    return resource - (x[0] + x[1])


def consumer_1st_h(x, resource):
    """
    :type x: list(float)
    :type resource: float
    :rtype: float
    """
    return resource - (x[0] * 3 + x[1] * 4)


def consumer_1st_ch(x, resource):
    """
    :type x: list(float)
    :type resource: float
    :rtype: float
    """
    return resource - x[1]


year_1 = ProducePeriod(
    resources=[50, 180, 40],
    predicted_prices=[40, 50],
    profit_calculator=profit_calculator_1st
)
year_1.add_consumer(consumer_1st_n)
year_1.add_consumer(consumer_1st_h)
year_1.add_consumer(consumer_1st_ch)

year_2 = ProducePeriod(
    resources=[50, 180, 40],
    predicted_prices=[40, 50],
    profit_calculator=profit_calculator_1st,
    last_period=year_1
)
year_2.add_consumer(consumer_1st_n)
year_2.add_consumer(consumer_1st_h)
year_2.add_consumer(consumer_1st_ch)

optimization_2_years = Optimization(
    optimizing_function=year_2.calculate_profit,
    boundaries=[
        (5, 100.0),
        (5, 100.0),
        (5, 100.0),
        (5, 100.0),
    ],
    no_dimensions=4,
    find_max=True
)
optimization_2_years.add_constraint(year_2.check_consumption)

pso_1st = PSO(
    optimization_object=optimization_2_years,
    no_particles=40,
    no_iteration_steps=20,
    c_1=2.0,
    c_2=2.0
)
print("Result for 1st case:")
ms_1st = MultipleSolving(pso_1st, 10)
ms_1st.run()
print(ms_1st)


# 2nd case: 3 year production planning with linear profit model
def profit_calculator_2nd(x, prices):
    """
    :type x: list(float)
    :type prices: list(float)
    :rtype: float
    """
    if len(x) == len(prices):
        total = 0.0
        for i in range(len(x)):
            total += x[i] * prices[i]
        return total
    else:
        raise ValueError("Mismatch number of products' quantities and price!")


consumer_2nd_n = consumer_1st_n
consumer_2nd_h = consumer_1st_h
consumer_2nd_ch = consumer_1st_ch

year_1 = ProducePeriod(
    resources=[50, 180, 40],
    predicted_prices=[40, 50],
    profit_calculator=profit_calculator_2nd
)
year_1.add_consumer(consumer_2nd_n)
year_1.add_consumer(consumer_2nd_h)
year_1.add_consumer(consumer_2nd_ch)

year_2 = ProducePeriod(
    resources=[50, 180, 40],
    predicted_prices=[40, 50],
    profit_calculator=profit_calculator_2nd,
    last_period=year_1
)
year_2.add_consumer(consumer_2nd_n)
year_2.add_consumer(consumer_2nd_h)
year_2.add_consumer(consumer_2nd_ch)

year_3 = ProducePeriod(
    resources=[50, 180, 40],
    predicted_prices=[40, 50],
    profit_calculator=profit_calculator_2nd,
    last_period=year_2
)
year_3.add_consumer(consumer_2nd_n)
year_3.add_consumer(consumer_2nd_h)
year_3.add_consumer(consumer_2nd_ch)

optimization_3_years = Optimization(
    optimizing_function=year_3.calculate_profit,
    boundaries=[
        (0, 100.0),
        (0, 100.0),
        (0, 100.0),
        (0, 100.0),
        (0, 100.0),
        (0, 100.0),
    ],
    no_dimensions=6,
    find_max=True
)
optimization_3_years.add_constraint(year_3.check_consumption)

pso_2nd = PSO(
    optimization_object=optimization_3_years,
    no_particles=40,
    no_iteration_steps=20,
    c_1=2.0,
    c_2=2.0
)
print("Result for 2nd case:")
ms_2nd = MultipleSolving(pso_2nd, 10)
ms_2nd.run()
print(ms_2nd)
