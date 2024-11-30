

import time
from instance.forest import RottenSwamp
from instance.front_flatland import FrontFlatland
from instance.poor_zone import PoorZone
from instance.snow_zone import SnowZone
from lib import ChallengeSelect
from reader import InfoReader


cs = ChallengeSelect()
reader = InfoReader()

# 打第一个巨人boss
def killBossGiant():
    # 打第一个boss
    cs.selectFrontFlatland()
    instance = FrontFlatland()
    reader.wait_tranported()
    instance.killBoss()
    cs.back2Town()
    reader.wait_tranported()
    return 10


# 打小树精
def killTreeSpirit():
    cs.selectPoorCamp()
    instance = PoorZone()
    reader.wait_tranported()
    move_back = instance.killTreeBoss()
    move_back()
    reader.wait_tranported()
    return 10


# 打牛魔王
def killBullBoss():
    cs.selectTwoPeak()
    instance = PoorZone()
    reader.wait_tranported()
    move_back = instance.killBullBoos()
    move_back()
    reader.wait_tranported()
    return 20


# 打蜘蛛boss
def killSpiderBoss():
    cs.selectWoodInstance()
    instance = RottenSwamp()
    reader.wait_tranported()
    instance.killSpiderBoss()
    cs.back2Town()
    reader.wait_tranported()
    return 10


# 打大树boss
def killBigTreeBoss():
    cs.selectColdWindCamp()
    instance = RottenSwamp()
    reader.wait_tranported()
    move_back = instance.killTreeSprite()
    move_back()
    reader.wait_tranported()
    return 10

# 打雪人boss
def killSnowmanBoss():
    cs.selectSnowInstance()
    instance = SnowZone()
    reader.wait_tranported()
    move_back = instance.killSnowManBoss()
    move_back()
    reader.wait_tranported()
    return 10


# 打金
def farmCoin():
    gold = 0
    gold += killBossGiant()
    gold += killTreeSpirit()
    gold += killBullBoss()
    # gold += killSpiderBoss()
    gold += killBigTreeBoss()
    # gold += killSnowmanBoss()
    return gold



