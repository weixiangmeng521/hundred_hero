import time
import Quartz
import cv2
import numpy as np
import pyautogui

from lib.info_reader import InfoReader


class SelectHero:
    
    def __init__(self, config):
        self.app_name = config['APP']['Name']
        self.config = config
        self.reader = InfoReader(config)

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
        
    
    # 显示英雄选择面板
    def show_hero_select_panel(self):
        winX, winY, winWidth, winHeight = self.get_win_info()
        # Point(x=37, y=794)
        pyautogui.click(int(winX + 40), int(winY + 800 - 35))
        time.sleep(.3)


    # 选择阵营
    def select_camp(self):
        winX, winY, winWidth, winHeight = self.get_win_info()
        # Point(x=354, y=761)
        pyautogui.click(int(winX + 354), int(winY + 761 - 35))
        time.sleep(.3)


    # 一件上阵
    def click_all_hero_in(self):
        winX, winY, winWidth, winHeight = self.get_win_info()
        # Point(x=359, y=278)
        pyautogui.click(int(winX + 359), int(winY + 288 - 35))
        time.sleep(.3)


    # 让选择了的英雄进入头排
    def let_selected_hero_to_top(self):
        winX, winY, winWidth, winHeight = self.get_win_info()
        # Point(x=344, y=390)
        pyautogui.click(int(winX + 344), int(winY + 390 - 35))
        time.sleep(.3)
        self.click_all_hero_in()



    # 向下滑动
    def slide_down(self, is_sleep=True):
        slide_down_duration = .1

        winX, winY, winWidth, winHeight = self.get_win_info()
        screenshot = pyautogui.screenshot(region=(int(63 + winX), int(winY + 479 - 35), (400 - 63), 5))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)
        # Point(x=319, y=714)
        pyautogui.moveTo(int(319), int(winY + 714 - 35))
        pyautogui.dragTo(int(319), int(winY + 714 - 35 - 1), slide_down_duration, button='left')
        pyautogui.click(int(319), int(winY + 714 - 35))
        if(is_sleep): time.sleep(.1)


    # 向上滑动
    def slide_up(self):
        slide_down_duration = .1

        winX, winY, winWidth, winHeight = self.get_win_info()
        screenshot = pyautogui.screenshot(region=(int(63 + winX), int(winY + 479 - 35), (400 - 63), 5))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)
        # Point(x=319, y=714)
        pyautogui.moveTo(int(319), int(winY + 714 - 35))
        pyautogui.dragTo(int(319), int(winY + 714 - 35 + 1), slide_down_duration, button='left')
        pyautogui.click(int(319), int(winY + 714 - 35))
        time.sleep(.1)


    # 上标准线是不是空的，还是监测到了有卡片进入
    def is_top_window_baseline_empty(self):
        winX, winY, winWidth, winHeight = self.get_win_info()
        screenshot = pyautogui.screenshot(region=(int(64 + winX), int(winY + 495 - 35), (398 - 64), 1))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)
        # self.reader.print_img(mat_image)
        return self.is_all_pixel_same_color(mat_image)


    # 写一个函数。判断里面所有的像素点的颜色是否相同    
    def is_all_pixel_same_color(self, mat_image):
        # 检查输入是否是一个 NumPy 数组
        if not isinstance(mat_image, np.ndarray):
            raise ValueError("输入必须是一个 NumPy 数组。")

        # 获取图像形状
        shape = mat_image.shape

        # 处理灰度图像
        if len(shape) == 2:  # 灰度图，形状为 (height, width)
            return np.all(mat_image == mat_image[0, 0])

        # 处理彩色图像
        elif len(shape) == 3:  # 彩色图，形状为 (height, width, channels)
            first_pixel = mat_image[0, 0]
            return np.all(mat_image == first_pixel)

        else:
            raise ValueError("不支持的图像格式。")



    # 让卡组贴合上标准线
    def fit_to_top_baseline(self):
        top_base_line = self.is_top_window_baseline_empty()
        print("贴合baseline中...")
        # 移动到top baseline的位置
        while(top_base_line):
            self.slide_down()
            top_base_line = self.is_top_window_baseline_empty()

            
    # 让卡组贴合上标准线
    def cross_cards(self):
        top_base_line = self.is_top_window_baseline_empty()
        print("跨过卡片组中...")
        # 移动到top baseline的位置
        while(not top_base_line):
            self.slide_down(is_sleep = False)
            top_base_line = self.is_top_window_baseline_empty()


    # 滑动窗口
    def slide_window(self):
        # 递归
        def recur(selct_cards_round):
            if(selct_cards_round > 3): return 
            print(f"第{selct_cards_round}轮英雄卡帕扫码...")

            self.fit_to_top_baseline()
            # Point(x=398, y=484)
            print('进入卡牌区,扫码卡...')
            self.cross_cards()
            # 下一轮
            selct_cards_round += 1            
            recur(selct_cards_round)

        recur(0)
        print("英雄卡帕扫码结束...")


    



    # 关闭英雄选择面板
    def close_hero_select_panel(self):
        winX, winY, winWidth, winHeight = self.get_win_info()
        # Point(x=37, y=794)
        pyautogui.click(int(winX + 40), int(winY + 800 - 35))
        time.sleep(.3)





    def test(self):

        self.show_hero_select_panel()
        self.select_camp()
        self.let_selected_hero_to_top()

        self.slide_window()

        # self.close_hero_select_panel()