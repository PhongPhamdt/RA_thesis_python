from algorithm.individual import Individual
from algorithm.objectives import Objectives
from daos.parameter import Parameter
from functools import cmp_to_key
from utils import Common
import numpy as np
import random
INFINITY = 10000


class GA:
    def __init__(self):
        self.NASH = None

    def run(self, params: Parameter, pop_init, pop_size=100, Pc=0.9, Pm=0.1, max_gen=100):
        population_info = []
        for i in range(0, pop_size):
            population_info.append(
                (
                    pop_init[i],
                    Objectives().fitness(pop_init[i], params)
                )
            )
        print("Running generations ... :")
        percent = 0
        for t in range(0, max_gen):
            if(t >= percent*max_gen/100):
                print("...{}%".format(percent))
                percent += 10
            # TODO: Do genetic here
            # self.
        pass

    def selection(self, population_info, pop_size):
        pass

    def mutation(self):
        pass

    def crossover(self):
        pass
