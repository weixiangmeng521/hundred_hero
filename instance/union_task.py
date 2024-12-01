
# 刷工会副本
import time
from exception.game_status import GameStatusError
from instance import forest, snow_zone
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader
from lib.logger import init_logger


# 工会任务
class UnionTask:

    def __init__(self, config):
        self.config = config
        self.app_name = config["APP"]["Name"]
        self.cs = ChallengeSelect(config)
        self.reader = InfoReader(config)
        self.logger = init_logger(config)
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
        instance = snow_zone.SnowZone(self.config)
        instance.crossGuildRoom()

     
    # 刷雪原的北风营地
    def farmingSnowfield(self):
        # 如果在城镇，就选择副本并且进入副本
        if(self.reader.is_show_back2town_btn() == False):
            # 选择并进入副本
            self.cs.selectDiamondInstance()
            time.sleep(10)

        # 刷副本
        instance = snow_zone.SnowZone(self.config)

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

        instance = forest.RottenSwamp(self.config)

        # 走到圈内
        if(self.loop_lock == False):
            instance.crossRoom3Begin()
            self.loop_lock = True
        
        # 循环走圈
        instance.crossRoom3Loop()


    # 刷腐烂沼泽
    def farmingRottingSwamp(self):
        self.cs.selectWoodInstance()
        # 等待
        self.reader.wait_tranported()
        instance = forest.RottenSwamp(self.config)

        try:
            while True:
                # instance.crossRoom1()
                instance.crossRoom2(should_check = False)
        except GameStatusError as e:
            self.logger.error(e)

        self.cs.back2Town()
        # 等待
        self.reader.wait_tranported()

    
    # 刷寒风营地
    def farmingColdWindCamp(self):
        # 如果在城镇，就选择副本并且进入副本
        if(self.reader.is_show_back2town_btn() == False):
            # 选择并进入副本
            self.cs.selectColdWindCamp()
            time.sleep(10)
            
        # 刷副本
        instance = forest.RottenSwamp(self.config)
        instance.crossColdWindCamp()