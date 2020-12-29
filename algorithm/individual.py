from daos import Parameter
from utils import Common
import numpy as np
import random
from utils import Common


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

        for i in range(0, params.tasks):
            self.t_human_assign[i] = random.randint(
                1, (1 << params.humans) - 1)
            self.t_machine_assign[i] = random.randint(
                1, (1 << params.machines) - 1)
            t_h_bit_assign = params.valid_human[i]
            t_h_bit_string = "0"*params.humans
            t_m_bit_assign = params.valid_machine[i]
            t_m_bit_string = "0"*params.machines
            if Common.rand_pos(t_h_bit_assign) is not None:
                t_h_bit_string_list = list(t_h_bit_string)
                t_h_bit_string_list[Common.rand_pos(t_h_bit_assign)] = "1"
                t_h_bit_string = "".join(t_h_bit_string_list)
            if Common.rand_pos(t_m_bit_assign) is not None:
                t_m_bit_string_list = list(t_m_bit_string)
                t_m_bit_string_list[Common.rand_pos(t_m_bit_assign)] = "1"
                t_m_bit_string = "".join(t_m_bit_string_list)
            self.t_human_assign[i] = int(t_h_bit_string, 2)
            self.t_machine_assign[i] = int(t_m_bit_string, 2)

    def set(self, t_h, t_m):
        self.t_human_assign = t_h
        self.t_machine_assign = t_m
