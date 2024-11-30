
# 刷工会副本
import time
from instance import forest, snow_zone
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader


# 工会任务
class UnionTask:

    def __init__(self, config):
        self.config = config
        self.app_name = config["APP"]["Name"]
        self.cs = ChallengeSelect(config)
        self.reader = InfoReader(config)
        # 是否进入了雪原循环圈
        self.loop_lock = False

    # 刷新
    def refresh(self):
        self.loop_lock = False

    
    # 刷雪原的魔力之环副本
    def farmingMagicRing(self):
        # 如果在城镇，就选择副本并且进入副本
        if(self.reader.is_show_back2town_btn() == False):
            # 选择副本
            self.cs.selectSnowInstance()
            time.sleep(10)

        # 刷副本
        instance = snow_zone.SnowZone()
        instance.crossGuildRoom()

     
    # 刷雪原的北风营地
    def farmingSnowfield(self):
        # 如果在城镇，就选择副本并且进入副本
        if(self.reader.is_show_back2town_btn() == False):
            # 选择并进入副本
            self.cs.selectDiamondInstance()
            time.sleep(10)

        # 刷副本
        instance = snow_zone.SnowZone()

        # 走到圈内
        if(self.loop_lock == False):
            instance.room1TaskBegin()
            self.loop_lock = True
        
        # 循环走圈
        instance.room1TaskLoop()


    # 刷污染前哨
    def farmingPollutionOutpost(self):
        # 如果在城镇，就选择副本并且进入副本
        if(self.reader.is_show_back2town_btn() == False):
            # 选择并进入副本
            self.cs.selectPollutionOutpost()
            time.sleep(10)

        instance = forest.RottenSwamp()

        # 走到圈内
        if(self.loop_lock == False):
            instance.crossRoom3Begin()
            self.loop_lock = True
        
        # 循环走圈
        instance.crossRoom3Loop()

    
    # 刷寒风营地
    def farmingColdWindCamp(self):
        # 如果在城镇，就选择副本并且进入副本
        if(self.reader.is_show_back2town_btn() == False):
            # 选择并进入副本
            self.cs.selectColdWindCamp()
            time.sleep(10)
            
        # 刷副本
        instance = forest.RottenSwamp()
        instance.crossColdWindCamp()