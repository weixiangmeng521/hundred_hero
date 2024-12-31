

# 虚拟map
import queue
import heapq

import numpy as np
from defined import DOWN_MOVE_CMD, FIND_ARENA, FIND_PORTAL, FIND_RECRUIT_NPC, FIND_TOWER, FIND_TRAINING_NPC, LEFT_MOVE_CMD, RIGHT_MOVE_CMD, UP_MOVE_CMD
from lib.logger import init_logger
from lib.move_controller import MoveControll


virtual_map_instance = None
# 单例模式
def init_virtual_map(config):
    global virtual_map_instance 
    if(virtual_map_instance):
        return virtual_map_instance
    virtual_map_instance = VirtualMap(config)
    virtual_map_instance.find_initial_position()
    return virtual_map_instance


# 虚拟map
class VirtualMap:
    
    def __init__(self, config):
        self.config = config
        self.mc = MoveControll(config)
        self.cell = 0.28
        self.logger = init_logger(config)
        self.cur_position = (0, 0)
        
        # 9 初始位置
        # 0 是障碍
        # 2 是训练营NPC
        # 3 是招募大厅
        # 4 传送阵
        # 5 竞技场
        # 6 塔
        # NPC的matrix
        self.npc_map_matrix = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],    
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],                                                                     
        ]
        # 人物移动matrix
        # self.map_matrix = np.full_like(self.npc_map_matrix, 1)


    # 重新设置出生地定位，在发生传送事件后，就会出现这种事情，出生地会变成传送口
    def reposition(self):
        pos = self.find_NPC_target(4)
        self.cur_position = pos


    # 找到初始位置
    def find_initial_position(self):
        pos = self.find_NPC_target(9)
        if(pos == None):
            raise ValueError("Err: matrix里找不到指定对象")
        self.cur_position = pos
        self.logger.debug(f"初始位置{pos}")


    # 找到标记过的指定目标
    def find_NPC_target(self, target_num):
        # 遍历矩阵的每个元素及其索引
        for i, row in enumerate(self.npc_map_matrix):
            for j, element in enumerate(row):
                if element == target_num:  # 找到值为9的位置
                    return (j, i)  # 更新当前位置
        return None



    # 曼哈顿启发函数
    def heuristic(self, a, b):
        if a is None or b is None:
            self.logger.debug("Invalid input to heuristic function:", a, b)
            return float('inf')  # 返回一个大的值，表示不合法
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    # 寻路算法
    def a_star(self, end):
        start = self.cur_position
        grid = self.npc_map_matrix
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        rows, cols = len(grid), len(grid[0])
        open_list = []
        heapq.heappush(open_list, (0 + self.heuristic(start, end), 0, start))  # (f, g, position)
        came_from = {}
        g_score = {start: 0}  # 起点到当前节点的实际距离
        f_score = {start: self.heuristic(start, end)}  # 起点到终点的估算距离
        
        while open_list:
            _, g, current = heapq.heappop(open_list)
            
            # 如果找到了终点，回溯路径
            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]  # 返回反转后的路径
            
            x, y = current
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and self.npc_map_matrix[ny][nx] != 0:
                    tentative_g_score = g + 1  # 假设每一步的代价是1
                    if (nx, ny) not in g_score or tentative_g_score < g_score[(nx, ny)]:
                        came_from[(nx, ny)] = (x, y)
                        g_score[(nx, ny)] = tentative_g_score
                        f_score[(nx, ny)] = tentative_g_score + self.heuristic((nx, ny), end)
                        heapq.heappush(open_list, (f_score[(nx, ny)], tentative_g_score, (nx, ny)))
        
        return None  # 如果没有路径


    # 转换路径为移动命令
    def path_to_commands(self, path):
        commands = []
        for i in range(len(path) - 1):
            current = path[i]
            next_step = path[i + 1]
            
            # 根据相邻节点的坐标差异决定移动命令
            if next_step[0] == current[0] and next_step[1] < current[1]:
                commands.append(UP_MOVE_CMD)  # 向上
            elif next_step[0] == current[0] and next_step[1] > current[1]:
                commands.append(DOWN_MOVE_CMD)  # 向下
            elif next_step[0] < current[0] and next_step[1] == current[1]:
                commands.append(LEFT_MOVE_CMD)  # 向左
            elif next_step[0] > current[0] and next_step[1] == current[1]:
                commands.append(RIGHT_MOVE_CMD)  # 向右
        return commands


    # 更新当前的position
    def update_postion(self, cmd):
        cur_position = self.cur_position

        # 定义位置的变化：字典方式简化
        move_map = {
            UP_MOVE_CMD: (-1, 0),  # 向上移动，y减少
            DOWN_MOVE_CMD: (1, 0),  # 向下移动，y增加
            LEFT_MOVE_CMD: (0, -1),  # 向左移动，x减少
            RIGHT_MOVE_CMD: (0, 1),  # 向右移动，x增加
        }

        # 如果命令有效，更新位置
        if cmd in move_map:
            dy, dx = move_map[cmd]  # 获取位置变化
            new_position = (cur_position[0] + dx, cur_position[1] + dy)
            # 更新地图
            self.cur_position = new_position  # 更新当前位置
            

    # 找到训练营NPC
    def move2training_npc(self):
        end = self.find_NPC_target(2)
        if(end == None):
            self.logger.debug(f"未找到[训练营NPC]坐标, cur:{self.cur_position} tar:{end}")
            return

        path = self.a_star(end)
        self.logger.debug(f"cur:{self.cur_position} tar:{end}, path:{path}")        
        if(path == None):
            self.logger.debug(f"未找到[训练营NPC]路径, cur:{self.cur_position} tar:{end}")
            return
                    
        cmd_list = self.path_to_commands(path)
        for event in cmd_list:
            self.event_mappper(event)


    # 找到传送口
    def move2protal(self):
        end = self.find_NPC_target(4)
        if(end == None):
            self.logger.debug("未找到[传送口]坐标")
            return

        path = self.a_star(end)
        self.logger.debug(f"cur:{self.cur_position} tar:{end}, path:{path}")        
        if(path == None):
            self.logger.debug("未找到[传送口]路径")
            return
        
        cmd_list = self.path_to_commands(path)
        for event in cmd_list:
            self.event_mappper(event)


    # 找到招募大厅
    def move2recruit(self):
        end = self.find_NPC_target(3)
        if(end == None):
            self.logger.debug("未找到[招募大厅]坐标")
            return

        path = self.a_star(end)
        self.logger.debug(f"cur:{self.cur_position} tar:{end}, path:{path}")
        if(path == None):
            self.logger.debug("未找到[招募大厅]路径")       
            return
                
        cmd_list = self.path_to_commands(path)
        for event in cmd_list:
            self.event_mappper(event)



    # 找到竞技场
    def move2arena(self):
        end = self.find_NPC_target(5)
        if(end == None):
            self.logger.debug("未找到[竞技场]坐标")
            return

        path = self.a_star(end)
        self.logger.debug(f"cur:{self.cur_position} tar:{end}, path:{path}")        
        if(path == None):
            self.logger.debug("未找到[竞技场]路径")       
            return
                
        cmd_list = self.path_to_commands(path)
        for event in cmd_list:
            self.event_mappper(event)


    # 找到塔
    def move2tower(self):
        end = self.find_NPC_target(6)
        if(end == None):
            self.logger.debug("未找到[塔]坐标")
            return

        path = self.a_star(end)
        self.logger.debug(f"cur:{self.cur_position} tar:{end}, path:{path}")        
        if(path == None):
            self.logger.debug("未找到[塔]路径")       
            return
                
        cmd_list = self.path_to_commands(path)
        for event in cmd_list:
            self.event_mappper(event)


    # 打印matrix
    def print_matrix(self):
        for row in self.map_matrix:
            print(" ".join(map(str, row)))  # 将每个元素转为字符串并用空格连接


    # 向上移动
    def move_up(self):
        self.update_postion(UP_MOVE_CMD)
        self.mc.move_up(self.cell)


    # 向右移动
    def move_right(self):
        self.update_postion(RIGHT_MOVE_CMD)
        self.mc.move_right(self.cell)


    # 向左移动
    def move_left(self):
        self.update_postion(LEFT_MOVE_CMD)
        self.mc.move_left(self.cell)


    # 向下移动
    def move_down(self):
        self.update_postion(DOWN_MOVE_CMD)
        self.mc.move_down(self.cell)


    # 指令转换
    def event_mappper(self, event):
        if event is UP_MOVE_CMD:
            self.move_up()
            
        if event is RIGHT_MOVE_CMD:
            self.move_right()
            
        if event is LEFT_MOVE_CMD:
            self.move_left()
            
        if event is DOWN_MOVE_CMD:
            self.move_down()

        if event is FIND_TRAINING_NPC:
            self.move2training_npc()

        if event is FIND_RECRUIT_NPC:
            self.move2recruit()

        if event is FIND_PORTAL:
            self.move2protal()

        if event is FIND_ARENA:
            self.move2arena()

        if event is FIND_TOWER:
            self.move2tower()

    # 启动
    def work(self, event_queue:queue.Queue):
        self.find_initial_position()

        while True:
            event = event_queue.get()  # 从队列中取消息（阻塞方式）
            self.event_mappper(event)
            event_queue.task_done()  # 标记任务完成
