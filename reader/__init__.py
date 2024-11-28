import time
from PIL import Image
import pyautogui
import Quartz
import cv2
import numpy as np
from lib import ChallengeSelect
from lib.logger import init_logger



class InfoReader:
    def __init__(self):
        self.app_name = "百炼英雄"
        self.img_win_name = "ImageAnalysis"   
        self.logger = init_logger(self.app_name)
        self.cs = ChallengeSelect()

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

    # 获得窗口的信息
    def get_win_info(self):
        window = self.get_specific_window_info()
        if(window == None): raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
        window_bounds = window.get('kCGWindowBounds', {})
        winX, winY = window_bounds.get('X', 0), window_bounds.get('Y', 0)
        winWidth, winHeight = window_bounds.get('Width', 0), window_bounds.get('Height', 0)
        return winX, winY, winWidth, winHeight


    def print_color(self, text, r, g, b):
        print(f"\033[48;2;{r};{g};{b}m{text}\033[0m")


    def print_img(self, mat_image):
        for row in range(mat_image.shape[0]):  # 遍历行
            for col in range(mat_image.shape[1]):  # 遍历列
                b, g, r = mat_image[row, col]  # 获取像素的 BGR 值
                self.print_color(f"{r},{g},{b}", r, g, b)


    def print_img_by_rgb(self, mat_image):
        for row in range(mat_image.shape[0]):  # 遍历行
            for col in range(mat_image.shape[1]):  # 遍历列
                r, g, b = mat_image[row, col]  # 获取像素的 BGR 值
                self.print_color(f"{r},{g},{b}", r, g, b)


    def is_full_from_img(self, meatPosList):
        # 读取指定位置
        screenshot = pyautogui.screenshot(region=(meatPosList))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)

        # 定义目标颜色并转换为 BGR 格式
        target_rgb = (253, 219, 84)   # RGB 格式
        target_bgr = target_rgb[::-1]      # 转换为 BGR 格式

        # 定义颜色的容差上下界，并转换为 uint8 类型
        lower_bound = np.array(target_bgr) - 20
        upper_bound = np.array(target_bgr) + 20

        # 创建掩码，找到接近目标颜色的区域
        mask = cv2.inRange(mat_image, lower_bound, upper_bound)

        # 检查掩码中是否包含目标颜色
        return cv2.countNonZero(mask) > 0



    # 读截图
    # 直接判断是不是黄色，黄色，就是打满了的情况
    def read_screen(self):
        window = self.get_specific_window_info()
        if(window == None):
            raise RuntimeError('Err', f"Window not found")
    
        meatPosList = (221, 113, 45, 13)
        isMeatFull = self.is_full_from_img(meatPosList)

        blueMinePosList = (301, 113, 45, 13)
        isBlueMineFull = self.is_full_from_img(blueMinePosList)

        return isMeatFull, isBlueMineFull


    # 判断工会任务是否完成, false的情况下是完成了，true的情况下是没完成
    def is_task_complete(self):
        self.cs.openTaskList()
        time.sleep(1)

        btnPos = (320, 365, 90, 37)
        # 读取指定位置
        screenshot = pyautogui.screenshot(region=(btnPos))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)

        # 定义目标颜色并转换为 BGR 格式
        target_rgb = (225, 204, 77)   # RGB 格式
        target_bgr = target_rgb[::-1]      # 转换为 BGR 格式

        # 定义颜色的容差上下界，并转换为 uint8 类型
        lower_bound = np.array(target_bgr) - 20
        upper_bound = np.array(target_bgr) + 20

        # 创建掩码，找到接近目标颜色的区域
        mask = cv2.inRange(mat_image, lower_bound, upper_bound)

        # 检查掩码中是否包含目标颜色
        return cv2.countNonZero(mask) == 0


    # 关闭按钮点击
    def close_task_menu(self, is_click_complete = False):
        if(is_click_complete): 
            self.cs.completeUnionTask()
            self.logger.info(f"点击已完成工会副本按钮.")
        self.cs.closeWin()
        time.sleep(.3)


    # 是否有显示回城图标
    def is_show_back2town_btn(self):
        btnPos = (410, 785, 38, 27)
        # 读取指定位置
        screenshot = pyautogui.screenshot(region=(btnPos))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)

        # 定义目标颜色并转换为 BGR 格式
        target_rgb = (89,106,116)   # RGB 格式
        target_bgr = target_rgb[::-1]      # 转换为 BGR 格式

        # 定义颜色的容差上下界，并转换为 uint8 类型
        lower_bound = np.array(target_bgr) - 20
        upper_bound = np.array(target_bgr) + 20

        # 创建掩码，找到接近目标颜色的区域
        mask = cv2.inRange(mat_image, lower_bound, upper_bound)

        # 检查掩码中是否包含目标颜色
        return cv2.countNonZero(mask) > 0



    # 判读是不是死了
    def is_dead(self):
        btnPos = (100, 720, 100, 40)
        # 读取指定位置
        screenshot = pyautogui.screenshot(region=(btnPos))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)

        target_rgb = (225,204,77)   # RGB 格式
        target_bgr = target_rgb[::-1]      # 转换为 BGR 格式

        lower_bound = np.array(target_bgr)
        upper_bound = np.array(target_bgr)

        mask = cv2.inRange(mat_image, lower_bound, upper_bound)
        is_contain_reborn_btn = cv2.countNonZero(mask) > 0


        btnPos = (280, 720, 100, 40)
        # 读取指定位置
        screenshot = pyautogui.screenshot(region=(btnPos))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)

        target_rgb = (219,88,79)   # RGB 格式
        target_bgr = target_rgb[::-1]      # 转换为 BGR 格式

        lower_bound = np.array(target_bgr)
        upper_bound = np.array(target_bgr)

        mask = cv2.inRange(mat_image, lower_bound, upper_bound)
        is_contain_give_up_btn = cv2.countNonZero(mask) > 0

        return is_contain_reborn_btn and is_contain_give_up_btn


    # 等待传送完成
    def wait_tranported(self):
        start_time = time.time()  # 记录开始时间
        timeout = 60  # 超时时间，单位为秒

        while True:
            elapsed_time = time.time() - start_time  # 计算已过去的时间
            if elapsed_time > timeout:
                raise TimeoutError("加载超时: 未在一分钟内传送完成。")

            window = self.get_specific_window_info()
            if(window == None): 
                raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
            
            window_bounds = window.get('kCGWindowBounds', {})
            winX, winY = window_bounds.get('X', 0), window_bounds.get('Y', 0)
            winWidth, winHeight = window_bounds.get('Width', 0), window_bounds.get('Height', 0)
            # 获取目标定位
            flagPos = (int((winWidth // 2) - 150 + winX), int((winHeight // 2) - 150 + winY), 300, 300)
            screenshot = pyautogui.screenshot(region=(flagPos))
            mat_image = np.array(screenshot)
            mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)
            target_rgb = (102, 193, 82)   # RGB 格式

            # cv2.imshow("123", mat_image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            target_bgr = target_rgb[::-1]      # 转换为 BGR 格式
            lower_bound = np.array(target_bgr)
            upper_bound = np.array(target_bgr)
            mask = cv2.inRange(mat_image, lower_bound, upper_bound)
            if(cv2.countNonZero(mask) > 0):
                return



    # 是否游戏加载成功
    def is_game_loaded(self, isContainsAds = False):
        self.logger.debug("等待游戏加载...")
        start_time = time.time()  # 记录开始时间
        timeout = 60  # 超时时间，单位为秒

        while True:
            elapsed_time = time.time() - start_time  # 计算已过去的时间
            if elapsed_time > timeout:
                raise TimeoutError("加载超时: 游戏未在1分钟内加载完成。")

            window = self.get_specific_window_info()
            if(window == None): 
                raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
            
            window_bounds = window.get('kCGWindowBounds', {})
            winX, winY = window_bounds.get('X', 0), window_bounds.get('Y', 0)
            # 获取目标定位
            flagPos = (int(287 + winX), int(53 + winY), 20, 20)
            screenshot = pyautogui.screenshot(region=(flagPos))
            mat_image = np.array(screenshot)
            mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)

            target_rgb = (246,199,77)   # RGB 格式
            if(isContainsAds): 
                target_rgb = (88,81,21)

            target_bgr = target_rgb[::-1]      # 转换为 BGR 格式

            lower_bound = np.array(target_bgr)
            upper_bound = np.array(target_bgr)

            mask = cv2.inRange(mat_image, lower_bound, upper_bound)
            if(cv2.countNonZero(mask) > 0):
                self.logger.debug("加载完毕！")
                return
        