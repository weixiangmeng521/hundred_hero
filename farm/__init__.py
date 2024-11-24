

import time
from instance.forest import RottenSwamp
from instance.front_flatland import FrontFlatland
from instance.poor_zone import PoorZone
from lib import ChallengeSelect


cs = ChallengeSelect()


# 打第一个巨人boss
def killBossGiant():
    # 打第一个boss
    cs.selectFrontFlatland()
    instance = FrontFlatland()
    time.sleep(9)
    instance.killBoss()
    cs.back2Town()
    time.sleep(9) 


# 打树精
def killTreeSpirit():
    cs.selectPoorCamp()
    instance = PoorZone()
    time.sleep(9)
    instance.killTreeBoss()
    cs.back2Town()
    time.sleep(9) 


# 打牛魔王
def killBullBoss():
    cs.selectTwoPeak()
    instance = PoorZone()
    time.sleep(9)
    instance.killBullBoos()
    cs.back2Town()
    time.sleep(9) 


# 打蜘蛛boss
def killSpiderBoss():
    cs.selectWoodInstance()
    instance = RottenSwamp()
    time.sleep(9)
    instance.killSpiderBoss()
    cs.back2Town()
    time.sleep(9) 


# 打大树boss
def killBigTreeBoss():
    cs.selectColdWindCamp()
    instance = RottenSwamp()
    time.sleep(9)
    instance.killTreeSprite()
    cs.back2Town()
    time.sleep(9) 


# 打金
def farmCoin():
    killBossGiant()
    killTreeSpirit()
    killBullBoss()
    killSpiderBoss()
    killBigTreeBoss()
    
    # 循环打
    farmCoin()




