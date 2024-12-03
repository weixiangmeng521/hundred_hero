

import time
from instance.forest import RottenSwamp
from instance.front_flatland import FrontFlatland
from instance.poor_zone import PoorZone
from instance.snow_zone import SnowZone
from lib.app_trace import AppTrace
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader
from lib.logger import init_logger
from lib.move_controller import MoveControll
from lib.visual_track import VisualTrack


# BOSS杀手，专业打boss
class BountyHunter:

    def __init__(self, config):
        self.config = config
        self.cs = ChallengeSelect(config)
        self.reader = InfoReader(config)
        self.trace = AppTrace(config)
        self.logger = init_logger(config)
        self.vt = VisualTrack(config)
        self.mc = MoveControll(config)


    # 打第一个巨人boss
    def killBossGiant(self):
        # 打第一个boss
        self.cs.selectFrontFlatland()
        instance = FrontFlatland(self.config)
        self.reader.wait_tranported()
        instance.killBoss()
        self.cs.back2Town()
        self.reader.wait_tranported()
        return 10

    
    # 击杀岩石巨人
    def killBossStoneMen(self):
        self.cs.selectWoodInstance()
        instance = RottenSwamp(self.config)
        self.reader.wait_tranported()
        instance.killStoneMen()
        self.cs.back2Town()
        self.reader.wait_tranported()
        return 10
    

    # 打小树精
    def killTreeSpirit(self):
        self.cs.selectPoorCamp()
        instance = PoorZone(self.config)
        self.reader.wait_tranported()
        move_back = instance.killTreeBoss()
        move_back()
        self.reader.wait_tranported()
        return 10


    # 打牛魔王
    def killBullBoss(self):
        self.cs.selectTwoPeak()
        instance = PoorZone(self.config)
        self.reader.wait_tranported()
        move_back = instance.killBullBossOldVersion()
        move_back()
        self.reader.wait_tranported()
        return 20
    

    # 打牛魔王
    def killBullBossQuickly(self):
        self.cs.selectPollutionOutpost()
        instance = PoorZone(self.config)
        self.reader.wait_tranported()
        instance.killBullBossQuickly()
        self.cs.back2Town()
        self.reader.wait_tranported()
        return 20


    # 打蜘蛛boss
    def killSpiderBoss(self):
        self.cs.select()
        instance = RottenSwamp(self.config)
        self.reader.wait_tranported()
        instance.killSpiderBoss()
        self.cs.back2Town()
        self.reader.wait_tranported()
        return 10


    # 打大树boss
    def killBigTreeBoss(self):
        self.cs.selectColdWindCamp()
        instance = RottenSwamp(self.config)
        self.reader.wait_tranported()
        move_back = instance.killTreeSprite()
        move_back()
        self.reader.wait_tranported()
        return 10

    # 打雪人boss
    def killSnowmanBoss(self):
        self.cs.selectSnowInstance()
        instance = SnowZone(self.config)
        self.reader.wait_tranported()
        move_back = instance.killSnowManBoss()
        move_back()
        self.reader.wait_tranported()
        return 10


    # 单个打金任务
    def task(self):
        gold = 0
        # gold += self.killBossGiant()
        gold += self.killTreeSpirit()
        gold += self.killBullBossQuickly()
        # gold += self.killSpiderBoss()
        gold += self.killBigTreeBoss()
        # gold += self.killSnowmanBoss()
        return gold


    # 移动到传送台
    def move_2_port(self):
        x, y, tx, ty = self.vt.find_position((121, 236, 239), 0, 0)
        self.mc.move(x, y, tx, ty)
        time.sleep(.3)


    # 循环打金
    def work(self):
        # 也许有那么一点点位置偏移，就会偏航
        # self.move_2_port()

        total = 0
        while True:
            # 开始计时
            start_time = time.time()
            # 秒杀boss
            earned = self.task()
            total += earned
            self.logger.info(f"💰总打金:{ total }")
            
            # 进入5-1刷新
            self.cs.selectIcecrownThrone()
            self.reader.wait_tranported()
            
            # 结束计时
            end_time = time.time()
            self.trace.record_time_formate(end_time - start_time, earned)

