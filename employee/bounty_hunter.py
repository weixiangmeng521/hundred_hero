

import time
from instance.black_rock import CenterHall
from instance.forest import RottenSwamp
from instance.front_flatland import FrontFlatland
from instance.poor_zone import PoorZone
from instance.snow_zone import SnowZone
from lib.app_trace import AppTrace
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader
from lib.logger import init_logger
from lib.move_controller import MoveControll
from lib.virtual_map import init_virtual_map
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
        self.virtual_map = init_virtual_map(config)


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
    def killBullBossOptimized(self):
        self.cs.selectPollutionOutpost()
        instance = PoorZone(self.config)
        self.reader.wait_tranported()
        instance.killBullBossOptimized()
        self.cs.back2Town()
        self.reader.wait_tranported()
        return 20
    

    # 打牛魔王，单人快速版本
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


    # 打双头蛇怪
    def killTwoHeadSnake(self):
        self.cs.selectDiamondInstance()
        instance = SnowZone(self.config)
        self.reader.wait_tranported()
        instance.killTwoHeadSnakeBoss()
        self.cs.back2Town()
        self.reader.wait_tranported()
        return 10

    
    # 击杀猛犸巨象
    def killMammoth(self):
        self.cs.selectSnowInstance()
        instance = SnowZone(self.config)
        self.reader.wait_tranported()
        instance.killMammoth()
        self.cs.back2Town()
        self.reader.wait_tranported()        
        return 10

    
    # 打黑石四大天王
    def killBackRock4Boss(self):
        self.cs.selectBlackRockHallway()
        instance = CenterHall(self.config)
        self.reader.wait_tranported()
        instance.kill4Boss()
        self.cs.back2Town()
        self.reader.wait_tranported()    
        return 40


    # 单个打金任务
    def task(self):
        gold = 0
        # gold += self.killBossGiant()
        gold += self.killTreeSpirit()
        gold += self.killBullBossOptimized()
        # gold += self.killSpiderBoss()
        gold += self.killBigTreeBoss()
        # gold += self.killSnowmanBoss()
        return gold

    # 快速单个打金任务
    def fast_task(self):
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


    # 普通模式
    def genral_mode(self):
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


    # 一次性杀四个boss
    def general_mode_for_kill_4_boss(self):
        total = 0
        while True:
            # 开始计时
            start_time = time.time()

            # 秒杀boss
            earned = self.killBackRock4Boss()
            total += earned
            self.logger.info(f"💰总打金:{ total }")
            
            # 进入5-1刷新
            self.cs.back2Town()
            self.reader.wait_tranported()
            
            # 结束计时
            end_time = time.time()
            self.trace.record_time_formate(end_time - start_time, earned)        



    # 进入快速模式
    def fast_mode(self):
        total = 0
        while True:
            # 开始计时
            start_time = time.time()
            # 秒杀boss
            earned = self.fast_task()
            total += earned
            self.logger.info(f"💰总打金:{ total }")
            
            # 进入5-1刷新
            self.cs.selectIcecrownThrone()
            self.reader.wait_tranported()
            
            # 结束计时
            end_time = time.time()
            self.trace.record_time_formate(end_time - start_time, earned)


    # 循环打金
    # 自动匹配模式，快速模式，和默认模式
    def work(self):
        # 找到位置
        self.virtual_map.move2protal()
        
        is_full = self.reader.is_team_member_full()
        if(is_full):
            self.logger.debug("匹配[普通刷金]模式")
            self.general_mode_for_kill_4_boss()

        if(not is_full):
            self.logger.debug("匹配[极速刷金]模式")
            self.fast_mode()
        