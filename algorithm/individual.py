from daos import Parameter
from utils import Common
import numpy as np
import random


class Individual:
    def __init__(self):
        # self.t_sched = []
        self.t_human_assign = []
        self.t_machine_assign = []

    def randomize(self, params: Parameter):
        # self.t_sched = np.empty(shape=params.tasks, dtype=int)
        self.t_human_assign = np.zeros(shape=params.tasks, dtype=int)
        self.t_machine_assign = np.zeros(shape=params.tasks, dtype=int)
        # prev_tasks = Common.get_prev_tasks(params)
        # for j in range(1, params.tasks+1):
        #     tj_sched = 1
        #     for i in prev_tasks[j]:
        #         tj_sched = max(
        #             tj_sched, self.t_sched[i-1] + params.t_duration[i-1])
        #     self.t_sched[j-1] = tj_sched + \
        #         random.randint(0, params.max_t_duration)

        valid_human = np.zeros((params.tasks, params.humans), dtype=int)
        valid_machine = np.zeros((params.tasks, params.machines), dtype=int)
        for i in range(0, params.tasks):
            for j in range(0, params.humans):
                for k in range(0, params.skills):
                    if params.TREQ[i][k] == 1 and params.LEXP[j][k] > 0:
                        valid_human[i][j] = 1
                        break
                for l in range(0, params.machines):
                    if params.MREQ[i][l] == 1 and params.MEXP[j][l] > 0:
                        valid_machine[i][l] = 1
                        break
        print(valid_human)
        print(valid_machine)
        for i in range(0, params.tasks):
            self.t_human_assign[i] = random.randint(
                1, (1 << params.humans) - 1)
            self.t_machine_assign[i] = random.randint(
                1, (1 << params.machines) - 1)

            # for bit in range(0, params.humans):
            #     if ((1 << bit & self.t_human_assign[i]) > 0) and (valid_human[i][bit]):
            #         self.t_human_assign[i] -= 1 << bit

            # for bit in range(0, params.machines):
            #     if ((1 << bit & self.t_machine_assign[i]) > 0) and (valid_machine[i][bit]):
            #         self.t_machine_assign[i] -= 1 << bit

        print(list(map(np.binary_repr, self.t_human_assign)))
        print(self.t_machine_assign)

    def set(self, t_h, t_m):
        self.t_human_assign = t_h
        self.t_machine_assign = t_m
