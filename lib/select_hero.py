import re
import time
import Quartz
import cv2
import mss
import numpy as np
import pyautogui

from lib.info_reader import InfoReader
from lib.logger import init_logger


class SelectHero:
    
    def __init__(self, config):
        self.app_name = config['APP']['Name']
        self.config = config
        self.reader = InfoReader(config)
        self.logger = init_logger(config)
        
    
    # 显示英雄选择面板
    def show_hero_select_panel(self):
        winX, winY, winWidth, winHeight = self.reader.get_win_info()
        # 如果已经显示了，就先关闭
        if(self.is_displayed_panel()): 
            self.close_hero_select_panel()
            time.sleep(.3)
        
        # Point(x=37, y=794)
        pyautogui.click(int(winX + 40), int(winY + 800 - 35))
        time.sleep(.3)


    # 选择阵营
    def select_camp(self):
        winX, winY, winWidth, winHeight = self.reader.get_win_info()
        # Point(x=354, y=761)
        pyautogui.click(int(winX + 354), int(winY + 761 - 35))
        time.sleep(.3)


    # 一件上阵
    def click_all_hero_in(self):
        winX, winY, winWidth, winHeight = self.reader.get_win_info()
        # Point(x=359, y=278)
        pyautogui.click(int(winX + 359), int(winY + 288 - 35))
        time.sleep(.3)


    # 让选择了的英雄进入头排
    def let_selected_hero_to_top(self):
        winX, winY, winWidth, winHeight = self.reader.get_win_info()
        # Point(x=344, y=390)
        pyautogui.click(int(winX + 344), int(winY + 390 - 35))
        time.sleep(.3)
        self.click_all_hero_in()



    # 是否已经显示了窗口
    def is_displayed_panel(self):
        # Point(x=99, y=219)
        winX, winY, winWidth, winHeight = self.reader.get_win_info()
        screenshot = pyautogui.screenshot(region=(int(99 + winX), int(winY + 219 - 35), 2, 2))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)
        return self.reader.is_target_area(mat_image, (67,148,130)) or self.reader.is_target_area(mat_image, (58,131,115))

        

    # 向下滑动
    def slide_down(self, is_sleep=True):
        slide_down_duration = .1

        winX, winY, winWidth, winHeight = self.reader.get_win_info()
        screenshot = pyautogui.screenshot(region=(int(63 + winX), int(winY + 479 - 35), (400 - 63), 5))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)
        # Point(x=318, y=714)
        pyautogui.moveTo(int(318), int(winY + 714 - 35))
        pyautogui.dragTo(int(318), int(winY + 714 - 35 - 1), slide_down_duration, button='left')
        pyautogui.click(int(318), int(winY + 714 - 35))
        if(is_sleep): time.sleep(.1)


    # 向上滑动
    def slide_up(self):
        slide_down_duration = .1

        winX, winY, winWidth, winHeight = self.reader.get_win_info()
        screenshot = pyautogui.screenshot(region=(int(63 + winX), int(winY + 479 - 35), (400 - 63), 5))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)
        # Point(x=318, y=714)
        pyautogui.moveTo(int(318), int(winY + 714 - 35))
        pyautogui.dragTo(int(318), int(winY + 714 - 35 + 1), slide_down_duration, button='left')
        pyautogui.click(int(318), int(winY + 714 - 35))
        time.sleep(.1)


    # 上标准线是不是空的，还是监测到了有卡片进入
    def is_top_window_baseline_empty(self):
        winX, winY, winWidth, winHeight = self.reader.get_win_info()
        screenshot = pyautogui.screenshot(region=(int(64 + winX), int(winY + 495 - 35), (398 - 64), 1))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)
        # self.reader.self.logger.debug_img(mat_image)
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
        self.logger.debug("贴合baseline中...")
        # 移动到top baseline的位置
        while(top_base_line):
            self.slide_down()
            top_base_line = self.is_top_window_baseline_empty()

            
    # 让卡组贴合上标准线
    def cross_cards(self):
        top_base_line = self.is_top_window_baseline_empty()
        self.logger.debug("跨过卡片组中...")
        # 移动到top baseline的位置
        while(not top_base_line):
            self.slide_down(is_sleep = False)
            top_base_line = self.is_top_window_baseline_empty()


    # 获得横排的英雄
    def scan_row_hero(self):
        winX, winY, winWidth, winHeight = self.reader.get_win_info()
        screenshot = pyautogui.screenshot(region=(int(64 + winX), int(winY + 495 - 35), (398 - 64), 100))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)

        h, w, *channel = mat_image.shape
        padding = 9
        card_width = int((w - (padding * 3)) // 4)

        hero1 = mat_image[:h, :card_width]
        hero2 = mat_image[:h, card_width + padding + 4: card_width * 2 + padding]
        hero3 = mat_image[:h, card_width * 2 + padding * 2 + 5: card_width * 3 + padding * 2]
        hero4 = mat_image[:h, card_width * 3 + padding * 4 : card_width * 4 + padding * 5] 
        return hero1, hero2, hero3, hero4


    # 选择卡片
    def select_target_cards(self, cards):
        # 卡的中线点位置
        cards_position = [
            (100, 539),
            (187, 540),
            (274, 534),
            (359, 538),
        ]
        # 判断每张卡的颜色
        for index, card in enumerate(cards):
            card_height, card_width = card.shape[:2]
            center_point = (int(card_width // 2), int(card_height // 2))
            # 卡牌的种类的位置，力量，智力，敏捷
            card_type_area = card[4:19, 1:20]
            # 卡牌的中心位置
            center_area = card[center_point[1]-10:center_point[1]+10, center_point[0]-10:center_point[0]+10]
            # 卡牌的左边的位置
            left_area = card[center_point[1]-10:center_point[1]+10, center_point[0]-35:center_point[0]-15]
            right_area = card[center_point[1]-20:center_point[1], center_point[0]+15:center_point[0]+35]


            red_hero_card_color = (93, 23, 26)
            golden_hero_card_color = (124, 93, 43)
            # 判断是否为敏捷卡
            swift_hero_type_color = (54, 103, 32)
            # 是否有绿色的勾
            green_check = (117, 220, 71)

            # 是否是红卡
            is_red_card = round(self.reader.get_color_ratio(card, red_hero_card_color), 2) >= 0.1
            # 是否是黄卡
            is_golden_card = round(self.reader.get_color_ratio(card, golden_hero_card_color), 2) >= 0.1
            is_swift_hero = round(self.reader.get_color_ratio(card_type_area, swift_hero_type_color), 2) >= 0.1

            # 判断是否被选中
            is_checked = self.reader.is_target_area(center_area, green_check)

            # 是不是李白
            libai_knife_sample1_color = (105, 121, 122)
            libai_knife_sample2_color = (104, 120, 122)
            libai_knife_sample3_color = (56, 75, 86)
            libai_knife_sample4_color = (84, 115, 117)
            libai_knife_sample5_color = (106, 119, 121)
            libai_knife_sample6_color = (78, 109, 113)

            libai_condition1 = self.reader.is_target_area(left_area, libai_knife_sample1_color)
            libai_condition2 = self.reader.is_target_area(left_area, libai_knife_sample2_color)
            libai_condition3 = self.reader.is_target_area(left_area, libai_knife_sample3_color)
            libai_condition4 = self.reader.is_target_area(right_area, libai_knife_sample4_color)
            libai_condition5 = self.reader.is_target_area(right_area, libai_knife_sample5_color)
            libai_condition6 = self.reader.is_target_area(right_area, libai_knife_sample6_color)
            is_libai = libai_condition1 and libai_condition2 and libai_condition3 and libai_condition4 and libai_condition5 and libai_condition6

            # 是不是卡卡西
            kakashi_weapon_sample1_color = (124, 111, 102)
            kakashi_weapon_sample2_color = (122, 99, 36)
            kakashi_weapon_sample3_color = (112, 76, 36)
            kakashi_condition1 = self.reader.is_target_area(right_area, kakashi_weapon_sample1_color)
            kakashi_condition2 = self.reader.is_target_area(right_area, kakashi_weapon_sample2_color)
            kakashi_condition3 = self.reader.is_target_area(right_area, kakashi_weapon_sample3_color)
            is_kakashi = kakashi_condition1 and kakashi_condition2 and kakashi_condition3

            # 赛选卡牌
            if (is_red_card and is_swift_hero):
                if(is_libai):
                    self.logger.debug(f"第{index + 1}张卡片为李白")
                    continue

                if(is_kakashi):
                    self.logger.debug(f"第{index + 1}张卡片为卡卡西")
                    continue
            
            # 把选上的英雄取消掉
            if(is_checked):
                pos = cards_position[index]
                pyautogui.click(pos[0], pos[1])
                time.sleep(0.3)



    # 滑动窗口
    def slide_window(self):
        # 最大滑动行数
        max_rows = 5
        # 递归
        for i in range(max_rows):
            self.logger.debug(f"第{i}轮英雄卡扫描中...")

            self.fit_to_top_baseline()
            self.logger.debug('进入卡牌区,选择需要的卡牌...')
            hero_list = self.scan_row_hero()
            self.select_target_cards(hero_list)
            self.logger.debug('操作结束')

            if(self.read_dispatched_hero_num() == 2):
                self.logger.debug("已经选择了2个英雄, 准备退出...")
                return

            self.cross_cards()
            # 下一轮

        self.logger.debug("英雄卡牌扫描结束...")



    # 关闭英雄选择面板
    def close_hero_select_panel(self):
        winX, winY, winWidth, winHeight = self.reader.get_win_info()
        # Point(x=37, y=794)
        pyautogui.click(int(winX + 40), int(winY + 800 - 35))
        time.sleep(.3)


    # 读取已经上阵的英雄数量
    def read_dispatched_hero_num(self):
        winX, winY, winWidth, winHeight = self.reader.get_win_info()
        with mss.mss() as sct:
            region = {
                "top": int(winY + 233 - 35), 
                "left": int(winX + 372),
                "width": int(13), 
                "height": int(15)
            }
            # 截取屏幕
            screenshot = sct.grab(region)
            mat_image = np.array(screenshot)
            return self.reader.recognize_number_text(mat_image)     


    # 读取sample里面的图片，做分析
    def analysis_sample(self):
        # 读取图片
        sample_img = cv2.imread('static/sample/6a5f5b4fdf654b4e4cc5906befa5873d.png')
        # 读取图片
        # sample_img = cv2.cvtColor(sample_img, cv2.COLOR_RGBA2BGR)
        self.reader.count_colors(sample_img, 100)


    # 让所有英雄全部上阵
    def dispatch_all_hero(self):
        self.show_hero_select_panel()
        self.select_camp()
        self.let_selected_hero_to_top()
        self.close_hero_select_panel()
        self.logger.debug("已上阵全部英雄!")


    # 选择目标英雄
    def dispatch_target_hero(self):
        self.show_hero_select_panel()
        self.select_camp()
        self.let_selected_hero_to_top()
        self.slide_window()
        self.close_hero_select_panel()
        self.logger.debug("已经选择卡卡西和李白!")
