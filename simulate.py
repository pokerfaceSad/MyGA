# -*- coding: utf-8 -*-

"""

仿真过程

1、 生成数据
2、 求最优解
3、 将集群状态（节点总内存、已使用内存）、任务资源需求（任务需求内存）、最优解（任务分配矩阵）写入文件
"""
import os
import main

sim_num = 1
i = 0
while i < sim_num:
    print("第%d次仿真" % (i+1))
    # os.system("python Data_Generate.py")
    os.system("python Data_Test.py")
    # 如果产生了有效解则加1
    if main.run(i) == 1:
        i += 1
