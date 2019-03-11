import shelve
import numpy as np
from constant_define import db_name

db = shelve.open(db_name)
node_state_list = db['node_state_list']
task_mem_list = db['task_mem_list']

node_mem_usage_rate_list = list()
sum_mem_reminder = 0
for node in node_state_list:
    sum_mem_reminder += (node.mem_tol - node.mem_used)
    node_mem_usage_rate_list.append(node.mem_usage_rate)

print("节点数量%d" % len(node_mem_usage_rate_list))
print("任务数量%d" % len(task_mem_list.tolist()[0]))
print("节点初始均衡度%f" % (1 - np.std(node_mem_usage_rate_list)))
print("节点剩余内存%d" % sum_mem_reminder)
print("任务需求内存%d" % sum(task_mem_list.tolist()[0]))
