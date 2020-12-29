from daos import Parameter
from algorithm import Individual

params = Parameter()

params.process("data/data.txt")

# print(params.humans)

# print("{0:b}".format((1 << params.humans) - 1))
# print(params.machines)

# print("{0:b}".format((1 << params.machines) - 1))

test_invd = Individual()
test_invd.randomize(params)

# print(test_invd.t_human_assign)
# print(test_invd.t_machine_assign)

# for assign in test_invd.t_human_assign:
#     # print(assign)
#     for bit in range(0, params.humans):
#         print((1 << bit))
#         print((1 << bit) & assign)

# print(test_invd.t_human_assign[0])
# print(1 << 1)
# print((1 << 1) & test_invd.t_human_assign[0])
