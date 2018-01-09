"""Finding best PSO parameters for problems."""

import math
from py_opt_collection.optimization import \
    Optimization, MultipleSolving
from py_opt_collection.pso import PSO
from py_opt_collection.test_functions import HIMMELBLAU as OPT_TARGET
from multiprocessing.dummy import Pool


# TODO: using Singleton
# Standard variables:
# x[0]: no_particles
# x[1]: no_iteration_steps
# x[2]: local learning factor
# x[3]: global learning factor


class PSO4PSO(object):
    def __init__(self, optimization_object,
                 no_tries,
                 max_runtime_in_seconds=5.0,
                 max_particles=200,
                 max_iteration=200,
                 max_learning_factor=3.0,
                 max_multi_solving_thread=1):
        self.ori_opt_object = optimization_object
        self.no_tries = no_tries
        self.max_runtime_in_seconds = max_runtime_in_seconds
        self.max_particles = max_particles
        self.max_iteration = max_iteration
        self.max_learning_factor = max_learning_factor
        self.max_ms_thread = max_multi_solving_thread

    def _ms_gen(self, x):
        core_pso = PSO(
            optimization_object=self.ori_opt_object,
            no_particles=math.ceil(x[0]),
            no_iteration_steps=math.ceil(x[1]),
            c_1=x[2],
            c_2=x[3]
        )
        core_ms = \
            MultipleSolving(algorithm_obj=core_pso,
                            no_tries=self.no_tries)
        return core_ms

    def _constraint_function(self, x):
        ms = self._ms_gen(x)
        if self.max_ms_thread > 1:
            ms.run(Pool(self.max_ms_thread))
        else:
            ms.run()
        return ms.stat['average_runtime'] <= self.max_runtime_in_seconds

    def _optimizing_function(self, x):
        ms = self._ms_gen(x)
        ms.run()
        return ms.stat['variance']

    def run(self, **kwargs):
        no_particles = kwargs.get('no_particles', 10)
        no_iterations = kwargs.get('no_iterations', 20)
        c_1 = kwargs.get('c_1', 2.0)
        c_2 = kwargs.get('c_2', 2.0)
        opt_obj = Optimization(
            optimizing_function=self._optimizing_function,
            boundaries=[
                (0, self.max_particles),
                (0, self.max_iteration),
                (0, self.max_learning_factor),
                (0, self.max_learning_factor)
            ],
            no_dimensions=4,
            find_max=False
        )
        opt_obj.add_constraint(self._constraint_function)
        pso = PSO(
            optimization_object=opt_obj,
            no_particles=no_particles,
            no_iteration_steps=no_iterations,
            c_1=c_1, c_2=c_2,
            verbose=True
        )
        ms = MultipleSolving(algorithm_obj=pso,
                             no_tries=kwargs.get('no_tries', 5))
        max_thread = kwargs.get('max_thread', 0)
        ms.run(pool=Pool(max_thread if max_thread else None))
        return ms


if __name__ == '__main__':
    pso_for_pso = PSO4PSO(optimization_object=OPT_TARGET['optimization'],
                          no_tries=10,
                          max_runtime_in_seconds=5,
                          max_particles=150,
                          max_iteration=250,
                          max_learning_factor=4.0,
                          max_multi_solving_thread=4)
    p4p_result = pso_for_pso.run(
        no_particles=8,
        no_iterations=5,
        no_tries=5,
        c_1=1.5,
        c_2=1.0
    )
    for result in p4p_result.results:
        print(result)
