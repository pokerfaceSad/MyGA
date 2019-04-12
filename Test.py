import copy
import numpy as np
import shelve
import matplotlib.pyplot as plt
db = shelve.open("./data/result0")
node_state_list = db['node_state_list']
task_mem_list = db['task_mem_list']
solution = db['solution']

# 绘制节点初始情况
mem_usage_rate_list = [node_state.mem_usage_rate for node_state in node_state_list]
mem_usage_rate_list = sorted(mem_usage_rate_list, reverse=False)
x = list(range(len(mem_usage_rate_list)))
plt.scatter(x, mem_usage_rate_list)
plt.show()
score = 1 - np.std([x * 100 for x in mem_usage_rate_list])
print(score)

node_mem_requirement = solution.task_assign_matrix * task_mem_list.T
new_node_state_list = copy.deepcopy(node_state_list)
new_node_mem_usage_rate_list = list()
sum_mem_usage_rate = 0
for no, node_state in enumerate(node_state_list):
    new_node_state_list[no].mem_used = node_state.mem_used + node_mem_requirement[no]
    if new_node_state_list[no].mem_used > new_node_state_list[no].mem_tol:
        print("无效结果")
    else:
        # 计算出所有节点的资源利用率
        new_node_state_list[no].update_mem_usage_rate()
        sum_mem_usage_rate += new_node_state_list[no].mem_usage_rate
        new_node_mem_usage_rate_list.append(float(new_node_state_list[no].mem_usage_rate))


score = 1 - np.std([x * 100 for x in new_node_mem_usage_rate_list])
print(score)
plt.scatter(x, new_node_mem_usage_rate_list)
plt.show()

