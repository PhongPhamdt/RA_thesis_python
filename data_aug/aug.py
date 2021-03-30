import numpy as np
import random


def gen_TREQ(f, num, tasks, skills):
    # Process with real skill later
    f.write(f" - TREQ matrix : size {tasks}x{skills} \n")
    str_array = ["1 1 0 0 0", "1 1 0 0 0", "1 0 0 0 0", "0 0 1 0 0", "0 0 0 1 0", "0 0 0 0 1", "1 0 0 0 0", "1 0 0 0 0", "1 0 0 0 0",
                 "0 0 1 0 0", "0 0 0 0 1", "1 0 0 0 0", "1 0 0 0 0", "1 1 0 0 0", "0 0 1 0 0", "0 0 1 0 0", "0 0 0 0 1", "1 0 0 0 0", "0 0 0 0 1"]

    for i in range(0, num):
        for j in str_array:
            f.write(f"{j}\n")


def gen_LEXP(f, human_resource, officers, workers, skills):
    # Process with real lexp later
    f.write(f" - LEXP matrix : size {human_resource}x{skills}\n")
    officer_array = ["0.97 0.86 0.00 0.00 0.00", "0.86 0.97 0.00 0.00 0.00"]
    worker_array = ["0.00 0.00 0.5 0.52 0.9", "0.00 0.00 0.91 0.91 0.95"]

    for _ in range(0, officers):
        f.write(f"{random.choice(officer_array)}\n")

    for _ in range(0, workers):
        f.write(f"{random.choice(worker_array)}\n")


def gen_MREQ(f, num, tasks, machine_resource):
    # Process with real machine later
    f.write(f" - MREQ matrix : size {tasks}x{machine_resource} \n")
    str_array = ["1 1 0 0 0", "1 1 0 0 0", "1 0 0 0 0", "0 0 1 0 0", "0 0 0 1 0", "0 0 0 0 1", "1 0 0 0 0", "1 0 0 0 0", "1 0 0 0 0",
                 "0 0 1 0 0", "0 0 0 0 1", "1 0 0 0 0", "1 0 0 0 0", "1 1 0 0 0", "0 0 1 0 0", "0 0 1 0 0", "0 0 0 0 1", "1 0 0 0 0", "0 0 0 0 1"]

    for i in range(0, num):
        for j in str_array:
            f.write(f"{j}\n")


def gen_MEXP(f, human_resource, officers, workers, machine_resource):
    # Process with real lexp later
    f.write(f" - MEXP matrix : size {human_resource}x{machine_resource}\n")
    officer_array = ["0.97 0.86 0.00 0.00 0.00", "0.86 0.97 0.00 0.00 0.00"]
    worker_array = ["0.00 0.00 0.5 0.52 0.9", "0.00 0.00 0.91 0.91 0.95"]

    for _ in range(0, officers):
        f.write(f"{random.choice(officer_array)}\n")

    for _ in range(0, workers):
        f.write(f"{random.choice(worker_array)}\n")


def gen_dependency(f, num):
    for i in range(0, num):
        f.write(f"{1 + 19*i} {2 + 19*i}\n")
        f.write(f"{2 + 19*i} {3 + 19*i}\n")
        f.write(f"{3 + 19*i} {4 + 19*i}\n")
        f.write(f"{4 + 19*i} {5 + 19*i}\n")
        f.write(f"{5 + 19*i} {6 + 19*i}\n")
        f.write(f"{5 + 19*i} {7 + 19*i}\n")
        f.write(f"{7 + 19*i} {8 + 19*i}\n")
        f.write(f"{8 + 19*i} {9 + 19*i}\n")
        f.write(f"{6 + 19*i} {10 + 19*i}\n")
        f.write(f"{10 + 19*i} {11 + 19*i}\n")
        f.write(f"{11 + 19*i} {12 + 19*i}\n")
        f.write(f"{12 + 19*i} {13 + 19*i}\n")
        f.write(f"{13 + 19*i} {14 + 19*i}\n")
        f.write(f"{14 + 19*i} {15 + 19*i}\n")
        f.write(f"{15 + 19*i} {16 + 19*i}\n")
        f.write(f"{16 + 19*i} {17 + 19*i}\n")
        f.write(f"{16 + 19*i} {18 + 19*i}\n")
        f.write(f"{17 + 19*i} {19 + 19*i}\n")


def main():
    filename = input("Please input data file name (Ex: gen-data.txt): \n")

    f = open(f"data/{filename}", "w+")
    f.write("Data for problem : Optimize assignment and schedule\n")
    f.write(" - number of task : \n")

    num_tasks = input("Please input number of the shipment arrived\n")

    tasks = 19 * int(num_tasks)
    f.write(f"{tasks}\n")

    officers = input("Please input number of the officers\n")

    workers = input("Please input number of the workers\n")

    human_resource = int(officers) + int(workers)

    f.write(" - number of human resources :\n")
    f.write(f"{human_resource}\n")

    officers_salary = ""
    workers_salary = ""

    for _ in range(0, int(officers)):
        officers_salary += "120 "
    for _ in range(0, int(workers)):
        workers_salary += "40 "

    human_salary = officers_salary + workers_salary

    f.write(" - human salary :\n")
    f.write(f"{human_salary.rstrip()}\n")

    # machine_resource = input("Please input number of the machines\n")
    machine_resource = 5
    f.write(" - number of machine resources :\n")
    f.write(f"{machine_resource}\n")

    f.write(" - consuming of machine :\n")
    machine_consuming_str = ""
    for i in range(0, int(machine_resource)):
        machine_consuming = input(
            f"Please input the consuming of machine {i+1} \n")
        machine_consuming_str += f"{machine_consuming} "

    f.write(f"{machine_consuming_str.rstrip()}\n")

    f.write(" - productivity of machine :\n")
    machine_prod_str = ""
    for i in range(0, int(machine_resource)):
        machine_prod = input(
            f"Please input the productivity ratio of machine {i+1} \n")
        machine_prod_str += f"{machine_prod} "
    f.write(f"{machine_prod_str.rstrip()}\n")

    f.write(" - number of skills :\n")
    # skills = input("Please input number of skills\n")
    skills = 5
    f.write(f"{skills}\n")

    f.write(" - number of machine type :\n")
    # machine_type = input("Please input number of machine type\n")
    f.write(f"{machine_resource}\n")

    f.write(" - task duration , 1D array len = tasks number\n")
    task_durations = "1 1 2 5 2 5 2 2 1 5 2 2 2 1 5 2 5 2 5 "
    task_durations_str = task_durations * int(num_tasks)
    f.write(f"{task_durations_str.rstrip()}\n")

    f.write(" - dependency relationship : D = (t_i,t_j) \n")
    f.write(" - size D : \n")

    sizeD = 18 * int(num_tasks)
    f.write(f"{sizeD}\n")
    gen_dependency(f, int(num_tasks))
    gen_TREQ(f, int(num_tasks), tasks, int(skills))
    gen_LEXP(f, human_resource, int(officers), int(workers), int(skills))
    gen_MREQ(f, int(num_tasks), tasks, int(machine_resource))
    gen_MEXP(f, human_resource, int(officers),
             int(workers), int(machine_resource))
    f.close()

    print(f"\nFile is located at data/{filename}")


if __name__ == "__main__":
    main()
