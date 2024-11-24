
# 抽卡
import time
import cv2
import numpy as np
import pyautogui
from reader import InfoReader


class Gacha:
    card_map = {
        0: "垃圾卡",
        1: "蓝卡",
        2: "紫卡",
        3: "橙卡",
        4: "红卡",
    }

    def __init__(self):
        self.reader = InfoReader()


    # 显示三张图片
    def display_three_cards(self, card1_img, card2_img, card3_img):
        card1_mat = cv2.cvtColor(card1_img, cv2.COLOR_RGB2BGR)
        card2_mat = cv2.cvtColor(card2_img, cv2.COLOR_RGB2BGR)
        card3_mat = cv2.cvtColor(card3_img, cv2.COLOR_RGB2BGR)

        # 水平拼接
        result = cv2.hconcat([card1_mat, card2_mat, card3_mat])

        # 显示结果
        cv2.imshow('Merged Image', result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # 定位三个坐标
    def read_three_cards(self):
        winX, winY, winWidth, winHeight = self.reader.get_win_info()
        screenshot = pyautogui.screenshot(region=(int(winX), int(winY), int(winWidth), int(winHeight)))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)

        # 截取卡片区域
        cards = []
        type_list = []
        coords = [
            (65, 283, 95, 320),            # 卡1区域
            (65 + 127, 283 + 33, 95 + 127, 320 + 33),  # 卡2区域
            (65 + 262, 283, 95 + 262, 320),  # 卡3区域
        ]
        for x1, y1, x2, y2 in coords:
            card = mat_image[y1:y2, x1:x2]
            cards.append(card)

        # 判断每张卡的颜色
        for _, card in enumerate(cards):
            card_type = self.get_cards_color(card)
            type_list.append(card_type)
        return type_list


    # 获取两个bound
    def conver(self, target_rgb):
        target_bgr = target_rgb[::-1]  # 转换为 BGR 格式
        offset = 20
        lower_bound = np.clip(np.array(target_bgr) - offset, 0, 255)
        upper_bound = np.clip(np.array(target_bgr) + offset, 0, 255)
        return lower_bound, upper_bound


    # 判断卡片颜色
    def get_cards_color(self, card):
        color_map = {
            (172, 168, 160): 0,  # 垃圾卡
            (73, 141, 209): 1,   # 蓝卡
            (171, 70, 251): 2,   # 紫卡
            (246, 193, 70): 3,   # 橙卡
            (203, 55, 62): 4,    # 红卡
        }
        # 判断颜色
        for target_rgb, card_type in color_map.items():
            lower_bound, upper_bound = self.conver(target_rgb)
            mask = cv2.inRange(card, lower_bound, upper_bound)
            if cv2.countNonZero(mask) > 0:
                return card_type
        return -1


    # 是否有红，紫，橙卡
    def is_contains_quality_cards(self):
        # 获取卡片列表
        cards_list = self.read_three_cards()
        # 判断是否包含橙卡 (3), 红卡 (4), 或 紫卡 (2)
        if any(card in cards_list for card in [2, 3, 4]):
            return True
        return False


    # 收否有红卡
    def is_contains_red_cards(self):
        cards_list = self.read_three_cards()
        # 判断是否有橙卡（3）或红卡（4）
        if 4 in cards_list:
            return True
        return False


    # 是否不能继续
    # 如果需要消耗绿砖，就不能继续
    def is_cannot_contine(self):
        winX, winY, winWidth, winHeight = self.reader.get_win_info()
        screenshot = pyautogui.screenshot(region=(int(winX), int(winY), int(winWidth), int(winHeight)))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)
        x1, y1, x2, y2 = 327 - 124, 280 + 380, 357 - 124, 305 + 380
        clip = mat_image[y1:y2, x1:x2]

        lower_bound, upper_bound= self.conver((251,226,76))
        mask = cv2.inRange(clip, lower_bound, upper_bound)
        if cv2.countNonZero(mask) <= 0:
            return True
        return False


    # 点击最大
    def click_max_btn(self):
        pyautogui.click(355, 645)
        time.sleep(.3)


    # 点击招募
    def click_recruit_btn(self):
        card_list = self.read_three_cards()
        mapped_list = [self.card_map.get(card, "未知卡") for card in card_list]
        print(f"当前卡为：{mapped_list}")
        
        if(self.is_contains_red_cards()):
            self.click_max_btn()
            time.sleep(.3)

        # 收否可继续
        is_contine = self.is_cannot_contine()

        # 点击招募
        if(is_contine == False):
            pyautogui.click(250, 690)
            time.sleep(.6)

        # 自动放弃
        if(is_contine):
            self.click_give_up()


    # 放弃按钮点击
    def click_give_up(self):
        pyautogui.click(235, 745)
        time.sleep(.3)
        # 点击确认
        pyautogui.click(295, 545)
        time.sleep(.3)




