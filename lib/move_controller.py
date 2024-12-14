from pynput.mouse import Controller
import pyautogui
import Quartz
import math
from lib.logger import init_logger



# 控制类
class MoveControll:

    def __init__(self, config, taskQueue = None):
        curX, curY = pyautogui.position()
        self.config = config
        self.app_name = config["APP"]["Name"]
        self.curPos = [curX, curY]
        self.logger = init_logger(config)
        self.mouse = Controller()
        self.cPos = [262 , 696]
        self.xPos = self.cPos[0]
        self.yPos = self.cPos[1]
        self.taskQueue = taskQueue
        # self.get_window_info()

    # TODO: 检查任务队列
    def check_task_queue(self):
        if(not self.taskQueue): 
            return


    # 获取窗口信息
    def get_specific_window_info(self):
        # 获取所有在屏幕上的窗口信息
        options = Quartz.kCGWindowListOptionOnScreenOnly
        window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)

        # 查找指定窗口
        for window in window_list:
            window_name = window.get('kCGWindowName', '')
            if self.app_name in window_name:
                return window  # 返回指定窗口的信息
        return None


    # 计算两点距离
    def get_point_distance(self, x1, y1, x2, y2):
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance


    def recover(self):
        pyautogui.moveTo(self.curPos[0], self.curPos[1])
        self.logger.info(f"x = {self.curPos[0]}, y = {self.curPos[1]}")


    def move_before_check(self):
        if(self.get_specific_window_info() == None): raise RuntimeError('Err', f"{self.app_name}`s window is not found.")


    def get_window_info(self):
        self.move_before_check()
        pyautogui.move(self.xPos, self.yPos)
        # pyautogui.click(self.xPos, self.yPos)


    def move_up(self, sec):
        self.move_before_check()
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos), int(self.yPos) - 50, sec, button='left')


    def move_top(self, sec):
        self.move_before_check()
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos), int(self.yPos) - 50, sec, button='left')


    def move_top_fast(self, sec):
        self.move_before_check()
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos), int(self.yPos) - 150, sec, button='left')


    def move_down(self, sec):
        self.move_before_check()
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos), int(self.yPos) + 50, sec, button='left')


    def move_down_fast(self, sec):
        self.move_before_check()
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos), int(self.yPos) + 150, sec, button='left')


    def move_left(self, sec):
        self.move_before_check()
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos) - 50, int(self.yPos), sec, button='left')

    def move_right(self, sec):
        self.move_before_check()        
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos) + 50, int(self.yPos), sec, button='left')


    def move_left_down(self, sec):
        self.move_before_check()        
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos) - 78, int(self.yPos + 50), sec, button='left')


    def move_left_top(self, sec):
        self.move_before_check()        
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos) - 78, int(self.yPos - 50), sec, button='left')


    def move_right_top(self, sec):
        self.move_before_check()        
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos) + 78, int(self.yPos - 50), sec, button='left')

    def move_right_down(self, sec):
        self.move_before_check()        
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos) + 78, int(self.yPos + 50), sec, button='left')


    def move(self, x, y, tX, tY):
        self.move_before_check()       
        distance = self.get_point_distance(x, y, tX, tY) 
        # 计算移动时间
        speed = 50 / 0.27      
        # 移动所需要的时间

        dx = self.cPos[0] - x
        dy = self.cPos[1] - y
        dX = tX + dx
        dY = tY + dy

        sec = distance / speed
        pyautogui.moveTo(self.cPos[0], self.cPos[1])
        pyautogui.dragTo(int(dX), int(dY), sec, button='left')



    def pointer_move_to(self, x, y):
        self.move_before_check()
        pyautogui.moveTo(int(x), int(y))

