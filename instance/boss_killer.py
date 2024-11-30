

import time
from instance.forest import RottenSwamp
from instance.front_flatland import FrontFlatland
from instance.poor_zone import PoorZone
from instance.snow_zone import SnowZone
from lib.challenge_select import ChallengeSelect
from reader import InfoReader

# BOSS杀手，专业打boss
class BossKiller:

    def __init__(self, config):
        self.config = config
        self.cs = ChallengeSelect(config)
        self.reader = InfoReader(config)


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
        move_back = instance.killBullBoos()
        move_back()
        self.reader.wait_tranported()
        return 20


    # 打蜘蛛boss
    def killSpiderBoss(self):
        self.cs.selectWoodInstance()
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


    # 打金
    def work(self):
        gold = 0
        gold += self.killBossGiant()
        gold += self.killTreeSpirit()
        gold += self.killBullBoss()
        # gold += self.killSpiderBoss()
        gold += self.killBigTreeBoss()
        # gold += self.killSnowmanBoss()
        return gold



