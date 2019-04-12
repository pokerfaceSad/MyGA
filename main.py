import copy
import shelve
import matplotlib.pyplot as plt
from functools import reduce
from MatrixIndividual import MatrixIndividual
from constant_define import db_name, node_num, task_num, is_paint, is_save
'''
从Data_Generate引入全局变量
'''


def run(sim_no):
    db = shelve.open(db_name)
    node_state_list = db['node_state_list']
    task_mem_list = db['task_mem_list']
    # 初始化种群
    individual_list = list()
    for i in range(100):
        individual_list.append(MatrixIndividual(node_num, task_num))
    individual_list = sorted(individual_list, key=lambda ind: ind.fitness, reverse=True)
    sum_fitness = reduce(lambda i1, i2: i1 + i2.fitness, individual_list, 0)
    avg_fitness = sum_fitness / len(individual_list)
    print("初始种群 最优适应度%f  平均适应度%f" % (individual_list[0].fitness, avg_fitness))

    '''
    进化终止条件
    如果连续十代最优适应度差异不超过0.000001 则停止进化
    '''
    stop_flag = 0
    # 每一代的个体最优适应度
    best_fitness_list = list()
    best_fitness_list.append(individual_list[0].fitness)
    # 每一代的种群最优适应度
    avg_fitness_list = list()
    avg_fitness_list.append(avg_fitness)
    for i in range(500):
        individual_list = MatrixIndividual.evolve(individual_list)
        individual_list = sorted(individual_list, key=lambda ind: ind.fitness, reverse=True)
        sum_fitness = reduce(lambda i1, i2: i1 + i2.fitness, individual_list, 0)
        avg_fitness = sum_fitness / len(individual_list)
        print("第%d代 最优适应度%f 平均适应度%f" % (i + 1, individual_list[0].fitness, avg_fitness))
        best_fitness_list.append(individual_list[0].fitness)
        avg_fitness_list.append(avg_fitness)
        if stop_flag == 10:
            if individual_list[0].fitness == 0:
                print("无可行解")
                return 0
            print("种群进化成熟，提前终止")
            break
        elif abs(best_fitness_list[-1] - best_fitness_list[-2]) <= 0.000001:
            stop_flag += 1
        else:
            stop_flag = 0

    '''
    绘制进化过程
    '''
    if is_paint:
        x = list(range(len(best_fitness_list)))
        plt.plot(x, best_fitness_list)
        plt.plot(x, avg_fitness_list, 'r')
        plt.show()

    '''
    数据持久化
    '''
    if is_save:
        # 从命令行读取仿真序号
        db = shelve.open('./data/result%s' % sim_no)
        db['node_state_list'] = node_state_list
        db['task_mem_list'] = task_mem_list
        db['solution'] = individual_list[0]
        db.close()



    db = shelve.open(db_name)
    node_state_list = db['node_state_list']
    task_mem_list = db['task_mem_list']

    # 根据任务分配矩阵 和 任务内存需求矩阵 对应元素相乘得到 任务需求矩阵
    node_mem_requirement = individual_list[0].task_assign_matrix * task_mem_list.T
    # 对node_state_list进行更新
    # 如果内存超出剩余怎么办
    # 1. 直接适应度降为零?

    new_node_state_list = copy.deepcopy(node_state_list)
    new_node_mem_usage_rate_list = list()
    sum_mem_usage_rate = 0
    for no, node_state in enumerate(node_state_list):
        new_node_state_list[no].mem_used = node_state.mem_used + node_mem_requirement[no]
        # 计算出所有节点的资源利用率
        new_node_state_list[no].update_mem_usage_rate()
        sum_mem_usage_rate += new_node_state_list[no].mem_usage_rate
        new_node_mem_usage_rate_list.append(float(new_node_state_list[no].mem_usage_rate))

    new_node_mem_usage_rate_list = sorted(new_node_mem_usage_rate_list, reverse=False)
    x = list(range(len(new_node_mem_usage_rate_list)))
    plt.scatter(x, new_node_mem_usage_rate_list)
    plt.show()

    return 1
