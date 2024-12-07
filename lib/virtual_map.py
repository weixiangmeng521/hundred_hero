

# 虚拟map
import queue

from lib.logger import init_logger

# 虚拟map
class VirtualMap:
    
    def __init__(self, config):
        self.config = config
        self.logger = init_logger(config)
    



    # 向上移动
    def move_up(self):
        self.logger.info("向上移动")


    # 向右移动
    def move_right(self):
        self.logger.info("向右移动")


    # 向左移动
    def move_left(self):
        self.logger.info("向左移动")


    # 向下移动
    def move_down(self):
        self.logger.info("向下移动")


    # 启动
    def work(self, event_queue:queue.Queue):
        while True:
            event = event_queue.get()  # 从队列中取消息（阻塞方式）
            
            if event is "1":
                self.move_up()
                

            if event is "2":
                self.move_right()
                

            if event is "3":
                self.move_left()
                

            if event is "4":
                self.move_down()
                

            event_queue.task_done()  # 标记任务完成
