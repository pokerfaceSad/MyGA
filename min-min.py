import shelve
import numpy as np
import matplotlib.pyplot as plt

'''
将节点按内存情况排序 将任务按内存需求情况排序
规则：将内存需求最小的节点先行分配在内存剩余最多的节点上
'''

db = shelve.open("./data.db")
node_state_list = db['node_state_list']
task_mem_list = db['task_mem_list']
# solution = db['solution']

node_state_list = sorted(node_state_list, key=lambda node_state: node_state.mem_usage_rate, reverse=False)

task_mem_list = task_mem_list[0].tolist()
task_mem_list = sorted(task_mem_list, reverse=False)
for task_mem in task_mem_list:
    node_state_list = sorted(node_state_list, key=lambda node_state: node_state.mem_usage_rate, reverse=False)
    node_state_list[0].mem_used = node_state_list[0].mem_used + task_mem
    node_state_list[0].mem_usage_rate = node_state_list[0].mem_used/node_state_list[0].mem_tol


# 计算得分
mem_usage_rate_list = list()
for node_state in node_state_list:
    mem_usage_rate_list.append(node_state.mem_usage_rate)


# score = 100 - np.std([x * 100 for x in mem_usage_rate_list])
# score = np.std(np.log10(mem_usage_rate_list))
score = 1 - np.std([x * 100 for x in mem_usage_rate_list])

print(score)

mem_usage_rate_list = sorted(mem_usage_rate_list, reverse=False)

x = list(range(len(mem_usage_rate_list)))
plt.scatter(x, mem_usage_rate_list)
plt.show()