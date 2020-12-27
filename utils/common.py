from daos import Parameter


class Common:
    def get_prev_tasks(params: Parameter):
        prev_tasks = [[]]
        for _ in range(0, params.tasks):
            prev_tasks.append([])
        for item in params.D:
            prev_tasks[item[1]].append(item[0])
        return prev_tasks

    def printPop(populationInfo, numResource):
        x = len(populationInfo)
        print(populationInfo)
        print("\n Done \n Population include {} element ".format(x))
        ind = 0
        s = []
        numObj = 3
        for i in range(0, numObj):
            s.append(0.0)
        for ele, ob_constr in populationInfo:
            ind += 1
            if(ind > 0):
                machine = []
                human = []
                print("\n solution {}. \n".format(ind))
                for i in range(0, len(ele.t_human_assign)):
                    machine.append("({})".format("{0:b}".format(
                        ele.t_machine_assign[i])).zfill(numResource))
                    human.append("({})".format("{0:b}".format(
                        ele.t_human_assign[i])).zfill(numResource))

                print("t_m_assign  : {}".format(machine))
                print("t_h_assign  : {}".format(human))

            for i in range(0, numObj):
                s[i] += ob_constr[0][i]
            # print "constraint : ",ob_constr[1]
        print("\n Average values : [")
        for i in range(0, numObj):
            s[i] /= x
            print("{},".format(s[i]))
        print("]")