from daos import Parameter
from utils import Common
from algorithm import Individual, Population, NSGA

params = Parameter()

filename = input("Please input data file name (Ex: data.txt): \n")

params.process(f"data/{filename}")

pop = Individual()
pop.randomize(params=params)

pop_init = Population().make_pop(params=params)
best_allocate = NSGA().run(params=params, pop_init=pop_init)
Common.printPop(best_allocate, params.humans, params.machines)
