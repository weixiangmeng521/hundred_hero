import time

import cv2
import pyautogui
from defined import IS_DALIY_ARENA_FINISHED
from exception.game_status import GameStatusError
from lib.cache import get_cache_manager_instance
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader
from lib.logger import init_logger
from lib.move_controller import MoveControll
from lib.virtual_map import init_virtual_map

# 技术不好爱打架
class Fighter:


    def __init__(self, config):
        self.config = config
        self.virtual_map = init_virtual_map(config)    
        self.reader = InfoReader(config)
        self.logger = init_logger(config)
        self.cache = get_cache_manager_instance(config)
        self.mc = MoveControll(config)
        self.cs = ChallengeSelect(config)
        self.tryAfterFlag = False


    # 如果不能点击，就直接报错
    def click_avalible_btn(self):
        # awalys click first one
        target_color = (221,200,75)
        mat_img = self.reader.read_arena_first_btn()
        while(self.reader.is_target_area(mat_img, target_color)):
            btn_pos = self.reader.get_arena_first_btn_pos()
            pyautogui.click(btn_pos[0], btn_pos[1])
            time.sleep(.3)
            if(not self.reader.is_enable_enter_arena()):
                self.tryAfterFlag = True
                return False
            
            return True
        return False
    

    # 选择菜单
    def auto_fight(self):
        self.cs.clickGreenPop()
        self.logger.debug("进入[竞技场]选择菜单界面")
        time.sleep(.3)

        # 点击能点击的按钮
        while(self.click_avalible_btn()):
            # 进入游戏
            self.reader.wait_selected_level_entered()

            # 战斗
            self.mc.move_right(.2)
            self.reader.wait_fight_over()
            self.logger.debug("已脱离战斗")
            # 战斗结束
            self.reader.clear_rewards(3)

            # 返回
            self.reader.wait_selected_level_leave()
            time.sleep(.3)

        # 关闭win
        self.cs.closeWin()

        # 打完了竞技场，无需再打
        if(not self.tryAfterFlag):
            self.logger.debug("每日竞技场完成, 无需再打")
            self.cache.set(IS_DALIY_ARENA_FINISHED, 1, 7)

        # 再一小时后重试
        if(self.tryAfterFlag):
            self.logger.debug("还无法进入竞技场, 1h后自动重试...")
            self.cache.set_next_hour(IS_DALIY_ARENA_FINISHED)

    
    # 工作
    def work(self):
        is_finished = self.cache.get(IS_DALIY_ARENA_FINISHED)
        # 如果没有值，就设置默认值
        if(not is_finished):
            self.cache.set(IS_DALIY_ARENA_FINISHED, 0, 7)
        
        # 如果完成了任务就直接结束。
        if(is_finished and int(is_finished) == 1):
            self.logger.info("每日竞技场已完成，无需再打")
            return
        
        # 找到位置
        if(not self.reader.is_show_back2town_btn()):
            self.logger.info("准备移动到[竞技场]...")
            self.virtual_map.move2arena()
        
        # 自动战斗
        self.auto_fight()
        