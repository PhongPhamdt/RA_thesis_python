import numpy as np


class Parameter:
    def __init__(self):
        self.tasks = 0
        self.humans = 0
        self.h_salary = []
        self.machines = 0
        self.m_consuming = []
        self.skills = 0
        self.t_duration = []
        self.max_t_duration = 0
        self.sizeD = 0
        self.machines_type = 0
        self.D = []
        self.TREQ = []
        self.LEXP = []
        self.MREQ = []
        self.MEXP = []
        self.valid_human = []
        self.valid_machine = []

    def process(self, filename):
        f = open(filename, "r")
        f.readline()
        f.readline()
        self.tasks = int(f.readline())
        f.readline()
        self.humans = int(f.readline())
        f.readline()
        self.h_salary = list(map(int, f.readline().split()))
        f.readline()
        self.machines = int(f.readline())
        f.readline()
        self.m_consuming = list(map(float, f.readline().split()))
        f.readline()
        self.m_prod = list(map(float, f.readline().split()))
        f.readline()
        self.skills = int(f.readline())
        f.readline()
        self.machines_type = int(f.readline())
        f.readline()
        self.t_duration = list(map(int, f.readline().split()))
        for t in self.t_duration:
            self.max_t_duration = max(self.max_t_duration, t)
        f.readline()
        f.readline()
        self.sizeD = int(f.readline())
        for _ in range(0, self.sizeD):
            line = f.readline()
            t_dependency = list(map(int, line.split()))
            self.D.append(t_dependency)
        line = f.readline()
        for _ in range(0, self.tasks):
            line = f.readline()
            self.TREQ.append(list(map(int, line.split())))
        f.readline()
        for _ in range(0, self.humans):
            line = f.readline()
            self.LEXP.append(list(map(float, line.split())))
        f.readline()
        for _ in range(0, self.tasks):
            line = f.readline()
            self.MREQ.append(list(map(int, line.split())))
        f.readline()
        for _ in range(0, self.humans):
            line = f.readline()
            self.MEXP.append(list(map(float, line.split())))
        self.valid_human = np.zeros((self.tasks, self.humans), dtype=int)
        self.valid_machine = np.zeros((self.tasks, self.machines), dtype=int)
        for i in range(0, self.tasks):
            for j in range(0, self.humans):
                for k in range(0, self.skills):
                    if self.TREQ[i][k] == 1 and self.LEXP[j][k] > 0:
                        self.valid_human[i][j] = 1
                        break
                for l in range(0, self.machines):
                    if self.MREQ[i][l] == 1 and self.MEXP[j][l] > 0:
                        self.valid_machine[i][l] = 1
                        break
