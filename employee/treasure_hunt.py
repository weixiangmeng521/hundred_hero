# 寻宝
import time
from instance.two_centipede import TwoCentipede
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader
from lib.logger import init_logger

# 每日30个箱子
class TreasureHunt:
    
    def __init__(self, config):
        self.config = config
        self.logger = init_logger(config)
        self.cs = ChallengeSelect(config)
        self.reader = InfoReader(config)

        
    # 移动到双虫
    def move_2_two_centipede(self):
        # self.cs.selectTwoCentipede()
        # self.reader.wait_tranported()
        # self.cs.clearAds(5)

        # instance = TwoCentipede(self.config)
        # instance.move_to_front_of_BOSS()
        


        # killboss, till find two of treasure
        self.reader.till_find_treasure()



        # self.cs.back2Town()




    
    # 工作
    def work(self):
        while True:
            self.move_2_two_centipede()
            self.reader.wait_tranported()
            time.sleep(1)
        