import shelve
from NodeState import NodeState
import numpy as np
from constant_define import task_num, node_num, db_name

print("生成数据...")
data_effective = False

while not data_effective:
    # 初始化节点
    node_state_list = list()
    # 节点内存使用率为 正态分布随机数 均值为0至0.7的随机数 方差0.05
    mu = np.random.uniform(0, 0.8)
    sigma = 0.1
    mem_usage_rate = abs(np.random.normal(mu, sigma, node_num))

    for i in range(node_num):
        node_state_list.append(NodeState(262144, 262144*mem_usage_rate[i]))

    # 初始化任务内存需求
    task_mem_list = np.random.randint(1, 7, size=(1, task_num))*512

    # 测试数据有效性
    node_mem_usage_rate_list = list()
    sum_mem_reminder = 0
    for node in node_state_list:
        sum_mem_reminder += (node.mem_tol - node.mem_used)
        node_mem_usage_rate_list.append(node.mem_usage_rate)

    if sum_mem_reminder > sum(task_mem_list.tolist()[0]):
        data_effective = True

print("节点数量%d" % len(node_mem_usage_rate_list))
print("任务数量%d" % len(task_mem_list.tolist()[0]))
print("节点初始均衡度%f" % (1 - np.std(node_mem_usage_rate_list)))
print("节点剩余内存%d" % sum_mem_reminder)
print("任务需求内存%d" % sum(task_mem_list.tolist()[0]))



# 将任务条件持久化
db = shelve.open(db_name)
db['node_state_list'] = node_state_list
db['task_mem_list'] = task_mem_list
db.close()
