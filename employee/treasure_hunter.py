# 寻宝
import time

import cv2
import numpy as np
import pyautogui
from defined import IS_DALIY_CASE_FINISHED
from exception.game_status import GameStatusError
from instance.two_centipede import TwoCentipede
from lib.cache import get_cache_manager_instance
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader
from lib.logger import init_logger
from lib.virtual_map import init_virtual_map

# 每日30个箱子
class TreasureHunt:
    
    def __init__(self, config):
        self.config = config
        self.logger = init_logger(config)
        self.cs = ChallengeSelect(config)
        self.reader = InfoReader(config)
        self.cache = get_cache_manager_instance(config)
        self.virtual_map = init_virtual_map(config)
        # 最大等待击杀怪物时间
        self.wait_max_time = 60 * 2
        
    
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
        self.reader.till_find_treasure(treasure_num = 2, wait_max_time = self.wait_max_time)
        self.logger.info("成功击杀双蜈蚣")
        # 等到获得宝箱的东西
        self.till_get_treasure()
        time.sleep(1.2)

        self.cs.back2Town()
        

    # 点击宝箱
    # 点击，因为旁边有小怪，也可能失效，点击不上
    # TODO: 判断今日是否已经领取完30个奖励
    def till_get_treasure(self):
        start_time = time.time()  # 记录开始时间
        timeout = 60 * 2  # 超时时间，单位为秒
        
        # 如果出现五次，点击，宝箱没有消失，就说明，30次到期了
        over_time = 0

        while True:
            elapsed_time = time.time() - start_time  # 计算已过去的时间
            if elapsed_time > timeout:
                raise TimeoutError(f"点击宝箱时: 未在 {timeout}s 内点击宝箱。")

            # 30次宝箱完成
            if(over_time >= 5):
                self.logger.debug("30次宝箱完成")
                self.cache.set(IS_DALIY_CASE_FINISHED, 1)
                return

            # 获取宝箱列表
            treasure_list = self.reader.find_treasure_case()
            # print(treasure_list)
            if len(treasure_list) >= 1:
                # 点击第一个宝箱
                btn = treasure_list[0]
                pyautogui.click(btn[0], btn[1] + 20)
                
                # 判断是否点击成功并处理弹窗
                self.logger.debug("等待弹出宝箱内容...")
                self.reader.wait_treasure_pop_up()
                self.logger.debug("宝箱内容已弹出。等待2s")
                time.sleep(2) # 因为有缓动动画，所以等2s
                self.reader.click_rewards()
                # self.cs.clearAds(3)

                if(len(treasure_list) == 1):
                    over_time += 1
            
            # 如果领取完全部奖励，结束
            if len(treasure_list) == 0:
                break
            
            time.sleep(.3)

    
    # 工作
    def work(self):
        # 找到位置
        if(not self.reader.is_show_back2town_btn()):
            self.virtual_map.move2protal()
        
        # self.reader.close_30s_ads()
        # time.sleep(20)
        while True:
            try:
                is_finished = self.cache.get(IS_DALIY_CASE_FINISHED)
                if(is_finished and int(is_finished) == 1):
                    self.logger.debug("已完成每日30个箱子,无需再打")
                    break

                self.move_2_two_centipede()
                self.reader.wait_tranported()
                time.sleep(.3)

            except GameStatusError as e:
                self.logger.info(f"{e}\n准备到附近传送点。")
                self.cs.clickGiveUpRebornBtn()
                time.sleep(8)
                self.logger.info("已到达复活传送点，准备回城。")
                self.cs.back2Town()
                self.logger.info("已经回到城镇。")
                time.sleep(10)
