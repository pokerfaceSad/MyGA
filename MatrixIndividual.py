# -*- coding: utf-8 -*-
import numpy as np
import copy
import shelve
from constant_define import pc, pm
from constant_define import db_name
'''
    每个解都是一个01矩阵 矩阵的size取决于任务数量和节点数量
'''


class MatrixIndividual:
    """
    根据节点数量和任务数量随机生成一个解个体
    """

    def __init__(self, node_num, task_num):
        self.task_num = task_num
        self.node_num = node_num
        self.fitness = 0
        # 首先创建一个node_num行 task_num列的全0阵
        self.task_assign_matrix = np.mat(np.zeros((node_num, task_num)))
        for i in range(task_num):
            # 在每一列上随机的取一个1 表示该列任务分配到该行节点上
            node_no = np.random.randint(0, node_num)
            self.task_assign_matrix[node_no, i] = 1
        self.cal_fitness()

    '''
    交叉操作
    '''

    @staticmethod
    def crossover(matrix_individual1, matrix_individual2):
        # 随机选择交叉位置
        crossover_location = np.random.randint(0, matrix_individual1.task_num - 1)
        # 进行交叉操作
        # 将矩阵1的0至task_num/2-1列与矩阵2的0至(task_num/2-1)列交换
        tmp = matrix_individual1.task_assign_matrix[:, np.arange(0, crossover_location + 1)]
        matrix_individual1.task_assign_matrix[:, np.arange(0, crossover_location + 1)] \
            = matrix_individual2.task_assign_matrix[:, np.arange(0, crossover_location + 1)]
        matrix_individual2.task_assign_matrix[:, np.arange(0, crossover_location + 1)] = tmp

    '''
    变异操作
    '''

    def mutate(self):
        # 随机选择一列进行突变
        mutate_location = np.random.randint(0, self.task_num, size=1)
        self.task_assign_matrix[:, mutate_location] = np.zeros((self.node_num, 1))
        # print("突变列为%d" % mutate_location)
        node_no = np.random.randint(0, self.node_num, size=1)
        self.task_assign_matrix[node_no, mutate_location] = 1

    '''
    适应度
    
    node_state_list 是一个NodeState对象列表
    task_mem_requirement 是一个表示任务内存需求的matrix
    '''

    def cal_fitness(self):
        db = shelve.open(db_name)
        node_state_list = db['node_state_list']
        task_mem_list = db['task_mem_list']

        # 根据任务分配矩阵 和 任务内存需求矩阵 对应元素相乘得到 任务需求矩阵
        node_mem_requirement = self.task_assign_matrix * task_mem_list.T
        # 对node_state_list进行更新
        # 如果内存超出剩余怎么办
        # 1. 直接适应度降为零?

        new_node_state_list = copy.deepcopy(node_state_list)
        new_node_mem_usage_rate_list = list()
        sum_mem_usage_rate = 0
        for no, node_state in enumerate(node_state_list):
            new_node_state_list[no].mem_used = node_state.mem_used + node_mem_requirement[no]
            if new_node_state_list[no].mem_used > new_node_state_list[no].mem_tol:
                self.fitness = 0
                return
            else:
                # 计算出所有节点的资源利用率
                new_node_state_list[no].update_mem_usage_rate()
                sum_mem_usage_rate += new_node_state_list[no].mem_usage_rate
                new_node_mem_usage_rate_list.append(float(new_node_state_list[no].mem_usage_rate))
        # 集群平均资源利用率
        # print(self.task_assign_matrix)
        # avg_mem_usage_rate = sum_mem_usage_rate / self.node_num
        # print(new_node_mem_usage_rate_list)
        self.fitness = 1 - np.std(new_node_mem_usage_rate_list)

    '''
     选择
    
         从种群中选择出父代进行交叉遗传
         父代与子代 比较适应度 决定淘汰还是保留
         pc 交叉概率
         pm 变异概率
     '''

    @staticmethod
    def evolve(pops):
        # 获取种群规模
        pop_size = len(pops)
        # 初始化新种群
        new_individual_list = list()
        while len(new_individual_list) < pop_size:
            # 随机选择两个进行交叉、变异操作

            father = pops[np.random.randint(0, len(pops))]
            mother = pops[np.random.randint(0, len(pops))]
            # 按照交叉概率进行交叉
            child1 = copy.deepcopy(father)
            child2 = copy.deepcopy(mother)
            if np.random.rand() < pc:
                MatrixIndividual.crossover(child1, child2)
                child1.cal_fitness()
                child2.cal_fitness()
            select_list = [father, mother, child1, child2]
            select_list = sorted(select_list, key=lambda individual: individual.fitness, reverse=True)
            if np.random.rand() < pm:
                select_list[0].mutate()
            if np.random.rand() < pm:
                select_list[1].mutate()
            select_list[0].cal_fitness()
            select_list[1].cal_fitness()
            new_individual_list.append(select_list[0])
            new_individual_list.append(select_list[1])
        return new_individual_list

# if __name__ == '__main__':
#     import shelve
#     import matplotlib.pyplot as plt
#     '''
#     从Data_Generate引入全局变量
#     '''
#     from Data_Generate import node_num
#     from Data_Generate import task_num
#     from Data_Generate import pc
#     from Data_Generate import pm
#     db = shelve.open("db")
#     node_state_list = db['node_state_list']
#     task_mem_requirement = db['task_mem_requirment']
#     # 初始化种群
#     individual_list = list()
#     for i in range(100):
#         individual = MatrixIndividual(node_num, task_num)
#         individual_list.append(individual)
#
#     individual_list = sorted(individual_list, key=lambda x: x.fitness, reverse=True)
#     sum_fitness = reduce(lambda i1, i2: i1+i2.fitness, individual_list, 0)
#     avg_fitness = sum_fitness/len(individual_list)
#     print("初始种群 最优适应度%f  平均适应度%f" % (individual_list[0].fitness, avg_fitness))
#
#     '''
#     进化终止条件
#     如果连续十代最优适应度差异不超过0.000001 则停止进化
#     '''
#     stop_flag = 0
#     last_best_fitness = individual_list[0].fitness
#     # 每一代的个体最优适应度
#     best_fitness_list = list()
#     best_fitness_list.append(individual_list[0].fitness)
#     # 每一代的种群最优适应度
#     avg_fitness_list = list()
#     avg_fitness_list.append(avg_fitness)
#     for i in range(1000):
#         individual_list = MatrixIndividual.evolve(individual_list)
#         individual_list = sorted(individual_list, key=lambda x: x.fitness, reverse=True)
#         sum_fitness = reduce(lambda i1, i2: i1 + i2.fitness, individual_list, 0)
#         avg_fitness = sum_fitness / len(individual_list)
#         print("第%d代 最优适应度%f 平均适应度%f" % (i+1, individual_list[0].fitness, avg_fitness))
#         best_fitness_list.append(individual_list[0].fitness)
#         avg_fitness_list.append(avg_fitness)
#         if stop_flag == 10:
#             print("种群进化成熟，提前终止")
#             break
#         elif abs(best_fitness_list[-1] - best_fitness_list[-2]) <= 0.000001:
#             stop_flag += 1
#         else:
#             stop_flag = 0
#
#     '''
#     绘制进化过程
#     '''
#     T = list(range(len(best_fitness_list)))
#     plt.plot(T, best_fitness_list)
#     plt.plot(T, avg_fitness_list, 'r')
#     plt.show()
