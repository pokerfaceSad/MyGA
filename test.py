import shelve
import numpy as np
db = shelve.open("./data/result5")
node_state_list = db['node_state_list']
task_mem_list = db['task_mem_list']
solution = db['solution']
r = 0
# for i in range(len(solution.task_assign_matrix.tolist())):
#     print(solution.task_assign_matrix * task_mem_list.T)
# for task in task_mem_list:

# print(type(task_mem_list))
# print(type(node_state_list))
# print(type(solution))

x = np.random.randint(0, 3, size=(2, 2))
y = np.random.randint(0, 2, size=(2, 1))
print(x)
print(y)
print(x*y)