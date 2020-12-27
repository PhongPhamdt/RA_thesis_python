from daos.parameter import Parameter
from .individual import Individual


class Population:
    def make_pop(self, params: Parameter, pop_size=100):
        pop = []
        for _ in range(0, pop_size):
            individual = Individual()
            individual.randomize(params)
            pop.append(individual)
        return pop
