# 寻宝
import time

import cv2
import numpy as np
import pyautogui
from exception.game_status import GameStatusError
from instance.two_centipede import TwoCentipede
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader
from lib.logger import init_logger

# 每日30个箱子
class TreasureHunt:
    
    def __init__(self, config):
        self.config = config
        self.logger = init_logger(config)
        self.cs = ChallengeSelect(config)
        self.reader = InfoReader(config)

    
    # 死亡处理
    def dead_hander(self):
        if(self.reader.is_dead()):
            raise GameStatusError("泼街了，准备复活。")

    
    # 移动到双虫
    def move_2_two_centipede(self):
        self.cs.selectTwoCentipede()
        self.reader.wait_tranported()

        instance = TwoCentipede(self.config)
        instance.move_to_front_of_BOSS()
        self.logger.info("已经移动到BOSS面前")

        # killboss, till find two of treasure
        self.reader.till_find_treasure()
        self.logger.info("成功击杀双蜈蚣")

        treasure_list = self.reader.find_treasure_case()
        self.click_treasure(treasure_list)
        time.sleep(1.2)

        self.cs.back2Town()
        

    # 点击宝箱
    # 点击，因为旁边有小怪，也可能失效，点击不上
    def click_treasure(self, treasure_list):
        start_time = time.time()  # 记录开始时间
        timeout = 60 * 120 # 超时时间，单位为秒

        elapsed_time = time.time() - start_time  # 计算已过去的时间
        if elapsed_time > timeout:
            raise TimeoutError(f"点击宝箱时: 未在{timeout}s点击宝箱。")            
        
        for btn in treasure_list:
            pyautogui.click(btn[0], btn[1] + 20)
            time.sleep(2.4)
            self.reader.click_rewards()
            time.sleep(.3)
            self.cs.clearAds(5)


    
    # 工作
    def work(self):
        while True:
            try:
                self.move_2_two_centipede()
                self.reader.wait_tranported()
                time.sleep(3)

            except GameStatusError as e:
                self.logger.info(f"{e}\n准备到附近传送点。")
                self.cs.clickGiveUpRebornBtn()
                time.sleep(8)
                self.logger.info("已到达复活传送点，准备回城。")
                self.cs.back2Town()
                self.logger.info("已经回到城镇。")
                time.sleep(10)
        

        