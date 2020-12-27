from algorithm.individual import Individual
from algorithm.objectives import Objectives
from daos.parameter import Parameter
import numpy as np
import random
INFINITY = 10000


class NSGA:
    def run(self, params: Parameter, pop_init, pop_size=100, Pc=0.9, Pm=0.1, max_gen=1000):
        population_info = []
        for i in range(0, pop_size):
            population_info.append(
                (
                    pop_init[i],
                    Objectives().objectives_constraints(pop_init[i], params)
                )
            )
        P = [population_info]
        Q = [[]]
        print("Running generations ... :")
        percent = 0
        for t in range(0, max_gen):
            if(t >= percent*max_gen/100):
                print("...{}%".format(percent))
                percent += 10
            Rt = P[t] + Q[t]
            new_P = self.selection(Rt, pop_size)
            P.append(new_P)
            Q.append(self.make_new_pop(new_P, Pc, Pm, params))
        return P[max_gen]

    def selection(self, population_info, pop_size):
        obj_constrs = []
        for data, obj_constr in population_info:
            obj_constrs.append(obj_constr)

        F = self.fast_nondominated_sort(obj_constrs)
        n_front = len(F)
        result = []
        for i in range(0, n_front):
            current_len = len(result)
            if current_len < pop_size:
                result += self.crowding_distance_selection(
                    obj_constrs, F[i], pop_size - current_len)
            break
        ans = []
        for index in result:
            ans.append(population_info[index])
        return ans

    def fast_nondominated_sort(self, obj_constr):
        # obj_constr[i] contain all objective and constraint value of i-th element
        # return the indices after sorted by front
        # F[i-1] is the indices of i-th non-dominated front of population
        size = len(obj_constr)
        # n[i-1] : number of current element dominate the i-th element
        n = np.zeros(shape=size)
        S = []
        first_front = []
        for i in range(0, size):
            S.append([])
        for i in range(0, size):
            for j in range(0, size):
                if i == j:
                    continue
                comp = self.get_dominate_state(obj_constr[i], obj_constr[j])
                if comp == 1:
                    S[i].append(j)
                elif comp == -1:
                    n[i] += 1
            if n[i] == 0:
                first_front.append(i)

        F = []
        ind = 0
        next_front = first_front
        while len(next_front) > 0:
            F.append(next_front)
            next_front = []
            for i in F[ind]:
                for j in S[i]:
                    n[j] -= 1
                    if n[j] == 0:
                        next_front.append(j)
            ind += 1

        return F

    def get_dominate_state(self, obj_constr1, obj_constr2):
        # 1 dominate 2 : return 1
        # 2 dominate 1 : return -1
        # ono-dominate : return 0
        obj1, constr1 = obj_constr1
        obj2, constr2 = obj_constr2
        first_dominate = False
        second_dominate = False
        for i in range(0, len(obj1)):
            if obj1[i] > obj2[i]:
                first_dominate = True
            if obj2[i] > obj1[i]:
                second_dominate = True
        # for i in range(0,constr1.__len__()):
        #     if constr1[i] > constr2[i]:
        #         first_dominate = True
        #     if constr2[i] > constr1[i]:
        #         second_dominate = True
        if first_dominate == True and second_dominate == False:
            return 1
        if second_dominate == True and first_dominate == False:
            return -1
        return 0

    def crowding_distance_selection(self, obj_constrs, front_ind, max_element):
        # select max_element best element
        if len(front_ind) <= max_element:
            return front_ind

        # sort and select
        obj_constrs_front = []
        cnt = 0
        mapping = np.empty(shape=len(front_ind), dtype=int)
        for index in front_ind:
            obj_constrs_front.append(obj_constrs[index])
            mapping[cnt] = index
            cnt += 1

        sorted_ind = self.sort_by_crowding_distance(obj_constrs_front)
        ans = []
        for i in range(0, max_element):
            ans.append(mapping[sorted_ind[i]])
        return ans

    def sort_by_crowding_distance(self, obj_constr):
        # obj_constr[i] contain all objective and constraint value of i-th element
        # return the indices after sorted by crowing distance
        # TODO : implement
        objects = []
        constraints = []
        for obj, constr in obj_constr:
            objects.append(obj)
            constraints.append(constr)
        m = len(objects[0])
        pop_size = len(objects)
        distance = np.zeros(pop_size)
        for t in range(0, m):
            def cmp(ind1, ind2):
                diff = objects[ind1][t] - objects[ind2][t]
                if diff > 0:
                    return 1
                if diff < 0:
                    return -1
                return 0
            # init array 0,1,2,..,pop_size
            sortedIndices = list(range(pop_size))
            sortedIndices.sort(cmp)
            distance[sortedIndices[0]] += INFINITY
            distance[sortedIndices[pop_size-1]] += INFINITY
            for i in range(1, pop_size-1):
                distance[sortedIndices[i]] += objects[sortedIndices[i+1]
                                                      ][t] + objects[sortedIndices[i-1]][t]

        def cmp_by_distance(ind1, ind2):
            diff = distance[ind1] - distance[ind2]
            if diff < 0:
                return 1
            if diff > 0:
                return -1
            return 0
        sortedIndices = list(range(pop_size))
        sortedIndices.sort(cmp_by_distance)
        return sortedIndices

    def make_new_pop(self, population_info, Pc, Pm, params):
        # expect Pc + Pm <= 1
        def copyParent(p_data):
            t_h_assign = []
            t_m_assign = []
            for i in range(0, len(p_data.t_human_assign)):
                t_h_assign.append(p_data.t_human_assign[i])
                t_m_assign.append(p_data.t_machine_assign[i])
            return [t_h_assign, t_m_assign]

        def find2DifferentRandomPos(maxPos):
            pos1 = random.randint(0, maxPos-1)
            pos2 = random.randint(1, maxPos-1)
            if pos2 == pos1:
                pos2 = 0
            if pos1 > pos2:
                temp = pos1
                pos1 = pos2
                pos2 = temp
            return pos1, pos2
        new_pop_info = []
        pop_size = len(population_info)
        indices = list(range(pop_size))
        random.shuffle(indices)
        numCross = int(pop_size*Pc/2)
        numMutate = int(pop_size*Pm)

        for i in range(0, numCross):
            ind1 = indices[(2 * i) % pop_size]
            ind2 = indices[(2 * i + 1) % pop_size]
            data1, _ = population_info[ind1]
            data2, _ = population_info[ind2]
            # dont change data1 and data2, make the copy and cross it
            child1 = copyParent(data1)
            child2 = copyParent(data2)
            t_h_assign1, t_m_assign1 = child1
            t_h_assign2, t_m_assign2 = child2
            n = len(t_h_assign1)
            pos1, pos2 = find2DifferentRandomPos(n)
            for pos in range(pos1, pos2):
                # switch t_assign
                temp = t_m_assign1[pos]
                t_m_assign1[pos] = t_m_assign2[pos]
                t_m_assign2[pos] = temp
                temp2 = t_h_assign1[pos]
                t_h_assign1[pos] = t_h_assign2[pos]
                t_h_assign2[pos] = temp2
            child_ind1 = Individual()
            child_ind1.set(t_h_assign1, t_m_assign1)
            child_ind2 = Individual()
            child_ind2.set(t_h_assign2, t_m_assign2)
            new_pop_info.append(
                (child_ind1, Objectives().objectives_constraints(child_ind1, params)))
            new_pop_info.append(
                (child_ind2, Objectives().objectives_constraints(child_ind2, params)))
        for i in range(0, numMutate):
            ind = indices[(2 * numCross + i) % pop_size]
            data, _ = population_info[ind]
            child = copyParent(data)
            t_h_assign, t_m_assign = child
            n = len(t_h_assign)
            pos = random.randint(0, n-1)
            if pos >= len(t_h_assign):
                print("pos {}    {}".format(pos, len(t_h_assign)))
            t_h_assign[pos] = random.randint(1, (1 << n) - 1)
            t_m_assign[pos] = random.randint(1, (1 << n) - 1)
            child_ind = Individual()
            child_ind.set(t_h_assign, t_m_assign)
            new_pop_info.append(
                (child_ind, Objectives().objectives_constraints(child_ind, params)))

        return new_pop_info
