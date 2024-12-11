import time

import pyautogui
from defined import IS_DALIY_TOWER_FINISHED
from exception.game_status import GameStatusError
from lib.cache import get_cache_manager_instance
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader
from lib.logger import init_logger
from lib.move_controller import MoveControll
from lib.virtual_map import init_virtual_map

# 刷塔狂人
class TowerWarrior:

    def __init__(self, config):
        self.config = config
        self.logger = init_logger(config)
        self.cs = ChallengeSelect(config)
        self.reader = InfoReader(config)
        self.cache = get_cache_manager_instance(config)
        self.virtual_map = init_virtual_map(config)
        self.mc = MoveControll(config)


    # 进入挑战塔界面
    def challenge(self):
        self.cs.clickGreenPop()
        time.sleep(1)
        self.cs.selectElementTower()
        time.sleep(1)
        while(self.reader.is_challenge_tower_available()):
            # 普通点击
            btn_pos = self.reader.get_tower_challenge_btn_pos()

            # 判断是不是有宝箱，有宝箱就点击宝箱，再挑战下一轮
            if(self.reader.is_show_tower_treasure()):
                self.logger.debug("有宝箱需要领取")
                pyautogui.click(btn_pos[0], btn_pos[1])
                time.sleep(.3)
                self.reader.clear_rewards()
                time.sleep(6)

            pyautogui.click(btn_pos[0], btn_pos[1], clicks=3)
            time.sleep(.3)

            # 进入游戏
            self.reader.wait_selected_level_entered("元素之塔")
            time.sleep(1.6)
            # 战斗
            self.mc.move_right(.3)
            self.reader.wait_fight_over("元素之塔")
            self.logger.debug("已脱离战斗, 继续挑战")
            time.sleep(.3)

            # 点击确认按钮，安全退出到塔的界面
            self.cs.click_arena_comfirm_btn()
            time.sleep(.3)
            self.reader.wait_selected_level_leave("元素之塔")
            self.logger.debug("等待5s进入下一轮.")
            time.sleep(6)
        



        self.cache.set(IS_DALIY_TOWER_FINISHED, 1, 7)
        self.logger.debug("已经打完今日的元素之塔, 无需再打.")
        self.cs.closeWin()
        time.sleep(3)

    
    # 工作
    # TODO: 刷到10次的时候会出现领取奖励的情况，要判断
    def work(self):
        is_finished = self.cache.get(IS_DALIY_TOWER_FINISHED)
        if(is_finished and int(is_finished) == 1):
            self.logger.debug("已经完成今日刷塔挑战, 无需再打")
            return
        
        # 设置默认值
        if(not is_finished):
            self.cache.set(IS_DALIY_TOWER_FINISHED, 0, 7)

        # 找到位置
        if(not self.reader.is_show_back2town_btn()):
            self.virtual_map.move2tower()

        self.challenge()





