# 寻宝
import time

import cv2
import numpy as np
import pyautogui
from defined import IS_DALIY_CASE_FINISHED
from employee.human import Human
from exception.game_status import GameStatusError
from instance.two_centipede import TwoCentipede
from lib.cache import get_cache_manager_instance
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader
from lib.logger import init_logger
from lib.select_hero import SelectHero
from lib.virtual_map import init_virtual_map

# 每日30个箱子
class TreasureHunt(Human):
    
    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.logger = init_logger(config)
        self.cs = ChallengeSelect(config)
        self.reader = InfoReader(config)
        self.cache = get_cache_manager_instance(config)
        self.virtual_map = init_virtual_map(config)
        self.selectHero = SelectHero(config)        
        # 最大等待击杀怪物时间
        self.wait_max_time = 60
        # 是不是宝箱数量大于30个
        self.is_treasure_num_greater_than_30 = config.getboolean("TASK", "IsTreasureNumGreaterThan30")
        
    
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
        

    # 检查30个宝箱是不是已经被点击
    def check_daliy_treasure_task_is_done(self):
        is_finished = self.cache.get(IS_DALIY_CASE_FINISHED)
        if(is_finished and int(is_finished) == 1):
            self.logger.debug("已完成每日30个箱子,无需再打")
            return

        self.logger.debug("读取任务列表, 判断每日30个宝箱是否领取完...")
        # 打开list
        self.cs.openTaskList()
        time.sleep(.6)
        # 读取list
        task_map = self.reader.read_task_list()
        for key, value in task_map.items():
            # 尽可能点击完成按钮
            isClicked = False
            while(self.reader.click_complete_task_btn()):
                isClicked = True
                time.sleep(.3)
            
            # 如发生点击了任务完成按钮，就重新读取当前状态
            if(isClicked):
                self.logger.debug("发生点击完成按钮事件...")
                self.reader.close_task_menu()
                time.sleep(.3)
                self.check_daliy_treasure_task_is_done()
                return
            
            # 判断是否已经完成任务
            if(key.find("开启") != -1 and bool(value)):
                self.logger.debug("每日30次宝箱已经完成。")
                self.cache.set(IS_DALIY_CASE_FINISHED, 1)
                self.reader.close_task_menu()
                return
            
            if(key.find("开启") != -1 and not bool(value)):
                self.logger.debug("没有打完30个宝箱,准备完成任务...")
                self.reader.close_task_menu()
                return

        self.reader.close_task_menu()


    # 点击宝箱
    # 点击，因为旁边有小怪，也可能失效，点击不上
    # 判断今日是否已经领取完30个奖励 => 通过每日任务判断 [2024.12.23]
    def till_get_treasure(self):
        start_time = time.time()  # 记录开始时间
        timeout = 60 * 2  # 超时时间，单位为秒
        
        # 如果出现5次，点击，宝箱没有消失，就说明，30次到期了
        max_clicked_times = 5
        over_time = 0

        while True:
            elapsed_time = time.time() - start_time  # 计算已过去的时间
            if elapsed_time > timeout:
                raise TimeoutError(f"点击宝箱时: 未在 {timeout}s 内点击宝箱。")

            # 30次宝箱完成
            if(over_time >= max_clicked_times):
                # 直接返回，回城后判断是否完成了任务
                if(not self.is_treasure_num_greater_than_30):
                    self.cache.set(IS_DALIY_CASE_FINISHED, 1)
                return

            # 获取宝箱列表
            treasure_list = self.reader.find_treasure_case()
            # print(treasure_list)
            if len(treasure_list) >= 1:
                # 点击第一个宝箱
                btn = treasure_list[0]
                pyautogui.click(btn[0], btn[1] + 20)
                time.sleep(.1)
                pyautogui.click(btn[0], btn[1] + 20)
                
                # 判断是否点击成功并处理弹窗
                self.logger.debug("等待弹出宝箱内容...")
                self.reader.wait_treasure_pop_up()
                self.logger.debug("宝箱内容已弹出。等待2s")
                time.sleep(2) # 因为有缓动动画，所以等2s
                
                self.reader.click_rewards()
                time.sleep(.1)
                self.reader.click_rewards()
                # self.cs.clearAds(3)

                if(len(treasure_list) == 1):
                    over_time += 1
            
            # 如果领取完全部奖励，结束
            if len(treasure_list) == 0:
                break
            
            time.sleep(.3)

    
    # 工作
    # TODO: 有读取miss的可能性
    def work(self):
        self.logger.info("准备每日30宝箱...")

        # 找到位置
        if(not self.reader.is_show_back2town_btn()):
            self.logger.debug("准备移动到传送阵.")
            self.virtual_map.move2protal()

        while True:
            try:                
                # 查看是否任务已经完成
                if(not self.is_treasure_num_greater_than_30):
                    self.check_daliy_treasure_task_is_done()
                
                is_finished = self.cache.get(IS_DALIY_CASE_FINISHED)
                if(is_finished and int(is_finished) == 1):
                    return

                # 设置默认值
                if(not is_finished):
                    self.cache.set(IS_DALIY_CASE_FINISHED, 0)
                
                # 全员上阵
                is_full = self.reader.is_team_member_full()
                if(not is_full):
                    self.logger.info("全部英雄上阵。")
                    self.selectHero.dispatch_all_hero()

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
