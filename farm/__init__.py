

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


# 打树精
def killTreeSpirit():
    cs.selectPoorCamp()
    instance = PoorZone()
    reader.wait_tranported()
    instance.killTreeBoss()
    cs.back2Town()
    reader.wait_tranported()


# 打牛魔王
def killBullBoss():
    cs.selectTwoPeak()
    instance = PoorZone()
    reader.wait_tranported()
    instance.killBullBoos()
    cs.back2Town()
    reader.wait_tranported()


# 打蜘蛛boss
def killSpiderBoss():
    cs.selectWoodInstance()
    instance = RottenSwamp()
    reader.wait_tranported()
    instance.killSpiderBoss()
    cs.back2Town()
    reader.wait_tranported()


# 打大树boss
def killBigTreeBoss():
    cs.selectColdWindCamp()
    instance = RottenSwamp()
    reader.wait_tranported()
    instance.killTreeSprite()
    # cs.back2Town()
    # reader.wait_tranported()

# 打雪人boss
def killSnowmanBoss():
    cs.selectSnowInstance()
    instance = SnowZone()
    reader.wait_tranported()
    instance.killSnowManBoss()
    time.sleep(1)


# 打金
def farmCoin():
    gold = 0
    killBossGiant()
    gold += 10
    killTreeSpirit()
    gold += 10
    killBullBoss()
    gold += 20
    killSpiderBoss()
    gold += 10
    killBigTreeBoss()
    gold += 10
    # killSnowmanBoss()
    # gold += 10
    return gold



