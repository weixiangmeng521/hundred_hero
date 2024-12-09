
# 教练员NPC
import time

import pyautogui
from employee import farmer
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader
from lib.logger import init_logger
from lib.move_controller import MoveControll
from lib.virtual_map import init_virtual_map
from lib.visual_track import VisualTrack


class CoachNPC:

    def __init__(self, config):
        self.config = config
        self.vt = VisualTrack(config)
        self.logger = init_logger(config)
        self.mc = MoveControll(config)
        self.cs = ChallengeSelect(config)
        self.reader = InfoReader(config)
        self.virtual_map = init_virtual_map(config)

    # 无限升级训练营
    def work(self):
        # 找到位置
        if(not self.reader.is_show_back2town_btn()):
            self.virtual_map.move2training_npc()


        # 流水线速度
        waitSec = 3.3
        _, isMineFull = self.reader.read_screen()

        if(isMineFull == True):
            self.find_NPC()        

        if(isMineFull == False):
            self.logger.info("刷一刷蓝矿")
            farmer.for_mine()

        time.sleep(waitSec)
        self.work()


    # 提升能力
    def upgrade_ability(self):
        _, _, tx, ty = self.vt.find_position((106, 204, 66), 10, 10)
        # 无视资源区域
        if(ty < 100): return
        
        pyautogui.click(tx - 25, ty + 40)
        time.sleep(.3)
        pyautogui.click(tx - 25, ty)
        time.sleep(1)


    # 移动到NPC
    def find_NPC(self):
        x, y, tx, ty = self.vt.find_position((205, 196, 214), 0, 0)
        # 如果没有找到目标就重新定位。
        if((x == tx and y == ty)):
            time.sleep(1)
            self.find_NPC()
            self.logger.info("没有找到训练营，重新定位...")

        if(not (x == tx and y == ty)):
            tolerate_distance = self.vt.get_point_distance(x, y, tx, ty)
            # 如果小于10像素，就算是移动到指定目的地了
            if(tolerate_distance >= 10):
                self.mc.move(x, y, tx, ty)

        # 点击绿泡泡
        self.cs.clickGreenPop()
        time.sleep(.3)
        self.upgrade_ability()
        self.reader.close_task_menu()
        time.sleep(.3)

        # 返回
        self.mc.move(tx, ty, x, y)
        time.sleep(.3)
