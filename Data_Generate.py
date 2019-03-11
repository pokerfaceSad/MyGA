import shelve
from NodeState import NodeState
import numpy as np
from constant_define import task_num, node_num, db_name

print("数据生成")
# 初始化节点
node_state_list = list()
# 节点内存使用率为 正态分布随机数 均值为0至0.7的随机数 方差0.05
mu = np.random.uniform(0, 0.7)
sigma = 0.05
mem_usage_rate = np.random.normal(mu, sigma, node_num)
for i in range(node_num):
    node_state_list.append(NodeState(262144, 262144*mem_usage_rate[i]))

# 初始化任务内存需求
task_mem_list = np.random.randint(512, 1024, size=(1, task_num))

# 将任务条件持久化
db = shelve.open(db_name)
db['node_state_list'] = node_state_list
db['task_mem_list'] = task_mem_list
db.close()
