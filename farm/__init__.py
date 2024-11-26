

import time
from instance.forest import RottenSwamp
from instance.front_flatland import FrontFlatland
from instance.poor_zone import PoorZone
from instance.snow_zone import SnowZone
from lib import ChallengeSelect


cs = ChallengeSelect()


# 打第一个巨人boss
def killBossGiant():
    # 打第一个boss
    cs.selectFrontFlatland()
    instance = FrontFlatland()
    time.sleep(8)
    instance.killBoss()
    cs.back2Town()
    time.sleep(8) 


# 打树精
def killTreeSpirit():
    cs.selectPoorCamp()
    instance = PoorZone()
    time.sleep(8)
    instance.killTreeBoss()
    cs.back2Town()
    time.sleep(8) 


# 打牛魔王
def killBullBoss():
    cs.selectTwoPeak()
    instance = PoorZone()
    time.sleep(8)
    instance.killBullBoos()
    cs.back2Town()
    time.sleep(8) 


# 打蜘蛛boss
def killSpiderBoss():
    cs.selectWoodInstance()
    instance = RottenSwamp()
    time.sleep(8)
    instance.killSpiderBoss()
    cs.back2Town()
    time.sleep(8) 


# 打大树boss
def killBigTreeBoss():
    cs.selectColdWindCamp()
    instance = RottenSwamp()
    time.sleep(8)
    instance.killTreeSprite()
    cs.back2Town()
    time.sleep(8) 

# 打雪人boss
def killSnowmanBoss():
    cs.selectSnowInstance()
    instance = SnowZone()
    time.sleep(8)
    instance.killSnowManBoss()
    cs.back2Town()
    time.sleep(8) 


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
    killSnowmanBoss()
    gold += 10
    return gold



