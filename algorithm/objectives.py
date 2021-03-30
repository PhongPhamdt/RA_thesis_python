from algorithm.individual import Individual
from daos.parameter import Parameter
from utils import Common
import numpy as np


class Objectives:
    def __init__(self):
        self.w_duration = 0.2
        self.w_assignment = 0.5
        self.w_cost = 0.3

    def f_duration(self, individual: Individual, params: Parameter):
        prev_tasks = Common.get_prev_tasks(params)
        t_start = np.empty(shape=params.tasks, dtype=int)
        t_finish = np.empty(shape=params.tasks, dtype=int)
        real_duration = np.empty(shape=params.tasks, dtype=int)
        project_finish = 0
        for i in range(0, params.tasks):
            t_start[i] = 0
            h_aff = 0
            m_aff = 1
            sum_prod = 0
            new_mreq = 0
            for j in range(0, params.skills):
                sum_exp = 0
                for k in range(1, params.humans):
                    if (individual.t_human_assign[i] & (1 << (params.humans - k))) != 0:
                        sum_exp += params.LEXP[k-1][j]
                if (sum_exp != 0):
                    h_aff = max(h_aff, params.TREQ[i][j] / sum_exp)
            for k in range(0, params.machines):
                if (params.MREQ[i][k] == 1):
                    new_mreq += 1
                    if (individual.t_machine_assign[i] & (1 << (params.machines - k))) != 0:
                        sum_prod += params.m_prod[k]
            if (sum_prod != 0):
                m_aff = new_mreq / sum_prod

            real_duration[i] = m_aff * h_aff * params.t_duration[i]
        for i in range(0, params.tasks):
            if len(prev_tasks[i]) == 0:
                t_finish[i] = t_start[i] + real_duration[i]
            else:
                for j in prev_tasks[i]:
                    t_finish[i] = t_finish[j] + real_duration[i]
            project_finish = max(project_finish, t_finish[i])
        return project_finish

    def f_assignment(self, individual:  Individual, params: Parameter):
        prev_tasks = Common.get_prev_tasks(params)
        t_start = np.empty(shape=params.tasks, dtype=int)
        t_finish = np.empty(shape=params.tasks, dtype=int)
        real_duration = np.empty(shape=params.tasks, dtype=int)
        for i in range(0, params.tasks):
            t_start[i] = 0
            h_aff = 0
            m_aff = 1
            sum_prod = 0
            new_mreq = 0
            for j in range(0, params.skills):
                sum_exp = 0
                for k in range(1, params.humans):
                    if (individual.t_human_assign[i] & (1 << (params.humans - k))) != 0:
                        sum_exp += params.LEXP[k-1][j]
                if (sum_exp != 0):
                    h_aff = max(h_aff, params.TREQ[i][j] / sum_exp)
            for k in range(0, params.machines):
                if (params.MREQ[i][k] == 1):
                    new_mreq += 1
                    if (individual.t_machine_assign[i] & (1 << (params.machines - k))) != 0:
                        sum_prod += params.m_prod[k]
            if (sum_prod != 0):
                m_aff = new_mreq / sum_prod

            real_duration[i] = m_aff * h_aff * params.t_duration[i]
        for i in range(0, params.tasks):
            if len(prev_tasks[i]) == 0:
                t_finish[i] = t_start[i] + real_duration[i]
            else:
                for j in prev_tasks[i]:
                    t_finish[i] = t_finish[j] + real_duration[i]

        # t_start = np.zeros(shape=params.tasks, dtype=int)
        # t_finish = np.zeros(shape=params.tasks, dtype=int)
        h_conflict = np.zeros(shape=params.tasks, dtype=float)
        m_conflict = np.zeros(shape=params.tasks, dtype=float)
        total_h_conflict = 0
        total_m_conflict = 0
        h_working_time = np.zeros(shape=params.humans, dtype=float)
        m_working_time = np.zeros(shape=params.machines, dtype=float)
        for u in range(0, params.tasks):
            for v in range(u+1, params.tasks):
                task_conflict = max(
                    0, (min(t_finish[u], t_finish[v]) - max(t_start[u], t_start[v])))
                # print(task_conflict)
                common_h_allocate = individual.t_human_assign[u] & individual.t_human_assign[v]
                common_m_allocate = individual.t_machine_assign[u] & individual.t_machine_assign[v]
                for i in range(1, params.humans + 1):
                    if(common_h_allocate & (1 << (params.humans - i))) != 0:
                        h_conflict[i-1] += task_conflict
                for i in range(1, params.machines + 1):
                    if(common_m_allocate & (1 << (params.machines - i))) != 0:
                        m_conflict[i-1] += task_conflict
        for u in range(0, params.tasks):
            for i in range(1, params.humans + 1):
                if ((individual.t_human_assign[u] & (1 << (params.humans - i))) != 0):
                    h_working_time += params.t_duration[u]
            for i in range(1, params.machines + 1):
                if ((individual.t_machine_assign[u] & (1 << (params.machines - i))) != 0):
                    m_working_time += params.t_duration[u]
        for i in range(0, params.humans):
            total_h_conflict += h_conflict[i] / h_working_time[i]
        for i in range(0, params.machines):
            total_m_conflict += m_conflict[i] / m_working_time[i]
        return total_h_conflict / params.humans + total_m_conflict / params.machines

    def f_cost(self, individual: Individual, params: Parameter):
        h_cost = 0
        m_cost = 0
        h_working_time = np.zeros(shape=params.humans, dtype=float)
        m_working_time = np.zeros(shape=params.machines, dtype=float)
        for u in range(0, params.tasks):
            for i in range(1, params.humans + 1):
                if ((individual.t_human_assign[u] & (1 << (params.humans - i))) != 0):
                    h_working_time += params.t_duration[u]
            for i in range(1, params.machines + 1):
                if ((individual.t_machine_assign[u] & (1 << (params.machines - i))) != 0):
                    m_working_time += params.t_duration[u]

        for i in range(0, params.humans):
            wage = 0
            for k in range(0, params.skills):
                wage += params.LEXP[i][k]
            h_cost += params.h_salary[i] * wage * h_working_time[i]
        for i in range(0, params.machines):
            m_cost += params.m_consuming[i] * m_working_time[i]
        return h_cost / params.humans + m_cost / params.machines

    def objectives_constraints(self, individual, params: Parameter):
        objectives = []
        objectives.append(-self.f_duration(individual, params))
        objectives.append(-self.f_assignment(individual, params))
        objectives.append(-self.f_cost(individual, params))
        constraints = []
        return objectives, constraints

    def fitness(self, individual: Individual, params: Parameter):
        return self.w_duration*self.f_duration(individual, params) + self.w_assignment*self.f_assignment(individual, params) + self.w_cost*self.f_cost(individual, params)
