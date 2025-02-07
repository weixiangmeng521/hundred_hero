import time
import cv2
import numpy as np
import pyautogui
from employee.human import Human
from exception.game_status import GameStatusError
from instance.union_task import UnionTask
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader
from lib.logger import init_logger
from lib.move_controller import MoveControll
from lib.virtual_map import init_virtual_map
from lib.visual_track import VisualTrack

# 卡牌大师
class CardsMaster(Human):
    color_map = {
        0: "\033[47m",  # 黑色背景
        1: "\033[44m",  # 蓝色背景
        2: "\033[45m",  # 紫色背景
        3: "\033[43m",  # 黄色背景（替代橙色）
        4: "\033[41m",  # 红色背景
    }    
    card_map = {
        0: "垃圾",
        1: "蓝卡",
        2: "紫卡",
        3: "橙卡",
        4: "红卡",
    }

    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.app_name = config["APP"]["Name"]
        self.reader = InfoReader(config)
        self.cs = ChallengeSelect(config)
        self.logger = init_logger(config)
        self.mc = MoveControll(config)
        self.vt = VisualTrack(config)
        self.unionTask = UnionTask(config)
        self.virtual_map = init_virtual_map(config)


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


    # 是否进入界面
    def is_entered(self):
        winX, winY, winWidth, winHeight = self.reader.get_win_info()
        screenshot = pyautogui.screenshot(region=(int(winX), int(winY), int(winWidth), int(winHeight)))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)
        x1, y1, x2, y2 = 55, 795, 105, 845
        clip = mat_image[y1:y2, x1:x2]

        lower_bound, upper_bound= self.conver((43,55,66), 0)
        mask = cv2.inRange(clip, lower_bound, upper_bound)
        gray_color = cv2.countNonZero(mask) > 0
    
        lower_bound, upper_bound= self.conver((230,232,236), 0)
        mask = cv2.inRange(clip, lower_bound, upper_bound)
        white_color = cv2.countNonZero(mask) > 0        

        return gray_color and white_color


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
    def conver(self, target_rgb, offset = 5):
        target_bgr = target_rgb[::-1]  # 转换为 BGR 格式
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
    def is_contains_high_level_card(self):
        cards_list = self.read_three_cards()
        # 判断是否有橙卡（3）或红卡（4）
        if 4 in cards_list or 3 in cards_list:
            return True
        return False


    # 是否不能继续
    # 如果需要消耗绿砖，就不能继续
    def is_cost_green_mine(self):
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



    # 打印带颜色的卡牌列表
    def print_colored_cards(self, card_list):
        # 颜色输出
        mapped_list = [
            f"{self.color_map.get(card, '\033[40m')}{self.card_map.get(card, '未知卡')}\033[0m"
            for card in card_list
        ]
        print(f"当前卡为：{' '.join(mapped_list)}")

        # 记录到日志
        cards_list = [
            f"{self.card_map.get(card, '未知卡')}"
            for card in card_list
        ]
        self.logger.info(f"当前卡为: {', '.join(cards_list)}")



    # 是否抽完
    def is_use_up_money(self):
        is_cost_green = self.is_cost_green_mine()
        
        # 是否有红字
        winX, winY, winWidth, winHeight = self.reader.get_win_info()
        screenshot = pyautogui.screenshot(region=(int(winX), int(winY), int(winWidth), int(winHeight)))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)
        x1, y1, x2, y2 = 327 - 91, 285 + 380, 357 - 91, 300 + 380
        clip = mat_image[y1:y2, x1:x2]

        lower_bound, upper_bound= self.conver((237,51,35), 15)
        mask = cv2.inRange(clip, lower_bound, upper_bound)
        is_no_more_money = cv2.countNonZero(mask) > 0

        return (not is_cost_green and is_no_more_money)
        
    
    # 判断是不是能正常抽卡，判断是不是进入了在抽卡结束后，进入下一轮抽卡的垃圾时间里
    def wait_avaliable_click(self):
        start_time = time.time()  # 记录开始时间
        timeout = 60  # 超时时间，单位为秒

        while True:
            elapsed_time = time.time() - start_time  # 计算已过去的时间
            if elapsed_time > timeout:
                raise TimeoutError("加载超时: 未能识别抽卡")

            window = self.reader.get_specific_window_info()
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
            target_bgr = target_rgb[::-1]      # 转换为 BGR 格式
            lower_bound = np.array(target_bgr)
            upper_bound = np.array(target_bgr)

            mask = cv2.inRange(mat_image, lower_bound, upper_bound)
            if(cv2.countNonZero(mask) > 0):
                return        


    # 获取被招募的英雄的index
    def get_recruited_hero_index(self):
        winX, winY, winWidth, winHeight = self.reader.get_win_info()

        screenshot = pyautogui.screenshot(region=(int(winX + 215), int(winY + 490 - 35), int(30), int(30)))
        middle_check_area = np.array(screenshot)
        middle_check_area = cv2.cvtColor(middle_check_area, cv2.COLOR_RGB2BGR)

        # Point(x=87, y=443)
        screenshot = pyautogui.screenshot(region=(int(winX + 87), int(winY + 453 - 35), int(30), int(30)))
        left_check_area = np.array(screenshot)
        left_check_area = cv2.cvtColor(left_check_area, cv2.COLOR_RGB2BGR)        

        # Point(x=352, y=445)
        screenshot = pyautogui.screenshot(region=(int(winX + 352), int(winY + 455 - 35), int(30), int(30)))
        right_check_area = np.array(screenshot)
        right_check_area = cv2.cvtColor(right_check_area, cv2.COLOR_RGB2BGR)        

        # 采样颜色
        sample1_color = (117, 220, 71)
        sample2_color = (119, 224, 72)
        sample3_color = (118, 221, 71)

        checked_area_list = [left_check_area, middle_check_area, right_check_area]
        for index, area in enumerate(checked_area_list):
            condition1 = self.reader.is_target_area(area, sample1_color)
            condition2 = self.reader.is_target_area(area, sample2_color)
            condition3 = self.reader.is_target_area(area, sample3_color)
            if(condition1 and condition2 and condition3):
                return index
        return -1


    # 点击招募
    def auto_recruit_btn(self):
        card_list = self.read_three_cards()
        # 如果有未知卡，就重新读
        if(-1 in card_list):
            return
            
        # 判断是否三倍
        if(self.is_contains_high_level_card()):
            self.click_max_btn()
            time.sleep(.1)

        # 如果没有钱了，就退出循环
        if(self.is_use_up_money()):
            raise GameStatusError("没钱了，不抽了")

        # 是否消耗绿矿
        is_contine = self.is_cost_green_mine()

        # 自动放弃
        if is_contine:
            # 获取选中英雄的信息
            selected_index = self.get_recruited_hero_index()
            if(selected_index > -1):
                selected_card = card_list[selected_index]
                self.logger.debug(f"抽卡结果: [{self.card_map[selected_card]}] 被选中.")            

            self.click_give_up()

        # 不消耗绿矿，招募
        if not is_contine:
            # 输出
            self.print_colored_cards(card_list)
            pyautogui.click(250, 690)

            

    # 放弃按钮点击
    def click_give_up(self):
        pyautogui.click(235, 745)
        time.sleep(.1)
        # 点击确认
        pyautogui.click(295, 545)
        time.sleep(.1)


    # 自动抽卡
    def work(self):
        self.logger.info("准备抽卡...")
        coin_threshold = int(self.config["TASK"]["GaChaCoinThreshold"])
        # 如果是None,说明识别失败,所以保存到sample
        coin_num = self.reader.get_coin_num(is_debug = True)
        if(coin_threshold > coin_num):
            self.logger.info(f"当前金币为{coin_num},低于抽卡设定的阈值{coin_threshold}.")
            return

        # 找到位置
        self.logger.debug("准备移动到招募大厅...")
        self.virtual_map.move2recruit()
        # 定位到，点击绿色泡泡
        self.cs.clickGreenPop()
        time.sleep(.3)

        while True:
            # 如果不能点击了，就结束
            try:
                self.auto_recruit_btn()
            except GameStatusError as e:
                self.logger.debug(e.get_error_info())
                break

        # 关闭抽卡，返回
        self.reader.close_task_menu()
        time.sleep(.1)

