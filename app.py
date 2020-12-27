from daos import Parameter
from utils import Common
from algorithm import Individual, Objectives, Population, NSGA

params = Parameter()

params.process("data/data.txt")

# print(params.t_duration)
# print(Common.get_prev_tasks(params))
pop = Individual()
pop.randomize(params=params)

pop_init = Population().make_pop(params=params)
best_allocate = NSGA().run(params=params, pop_init=pop_init)
Common.printPop(best_allocate, params.tasks)
# func = Objectives()
# print(func.f_cost(individual=pop, params=params))
# print(1 << param.humans)
# print(pop.t_sched)
