# -*- coding: utf-8 -*-

'''

节点的状态

1. 总内存
2. 已使用内存
3. 内存占用率
'''


class NodeState:

    def __init__(self, mem_tol, mem_used):
        self.mem_tol = mem_tol
        self.mem_used = mem_used
        self.mem_usage_rate = mem_used/mem_tol

    def update_mem_usage_rate(self):
        self.mem_usage_rate = self.mem_used/self.mem_tol

    def __str__(self):
        return '(Node: %d, %d, %f)' % (self.mem_tol, self.mem_used, self.mem_usage_rate*100)
