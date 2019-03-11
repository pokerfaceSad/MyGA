import shelve
import matplotlib.pyplot as plt
from functools import reduce
from MatrixIndividual import MatrixIndividual
from constan_define import db_name, node_num, task_num, is_paint, is_save
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
    return 1
