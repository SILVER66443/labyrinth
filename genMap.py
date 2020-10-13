
def gen_map(self, max_x=10, max_y=10):
    """ 生成迷宫 """
    self.max_x, self.max_y = max_x, max_y  # 设置地图大小
    self.mmap = [[None for j in range(self.max_y)] for i in range(self.max_x)]  # 生成原始地图
    self.solution = []  # 迷宫解法
    block_stack = [Block(self, 0, 0)]  # 从0,0开始生成迷宫（同时将这点作为起点），将起点放到栈里
    while block_stack:
        block = block_stack.pop()  #取出当前所在的房间
        next_block = block.get_next_block()  # 获取下一个要去的房间
        if next_block:  # 如果成功获取下一走发，将走过的房间放回到栈里
            block_stack.append(block)
            block_stack.append(next_block)
            if next_block.x == self.max_x - 1 and next_block.y == self.max_y - 1:  # 走到终点了，栈里的路径就是解法
                for o in block_stack:
                    self.solution.append((o.x, o.y))