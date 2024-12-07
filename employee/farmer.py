import time
from exception.game_status import GameStatusError
from instance.black_rock import CenterHall
from instance.forest import RottenSwamp
from instance.union_task import UnionTask
from instance.hell_of_fire import HellOfFire
from instance.snow_zone import SnowZone
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader
from lib.logger import init_logger
from lib.virtual_map import init_virtual_map



# 作为苦逼的农民
class Farmer:

    def __init__(self, config):
        self.config = config
        self.cs = ChallengeSelect(config)
        self.logger = init_logger(config)
        self.reader = InfoReader(config)
        self.unionTask = UnionTask(config)
        self.virtual_map = init_virtual_map(config)


    # 刷经验
    def for_experience(self):
        self.cs.selectExpeirenceInstance()
        time.sleep(9)

        instance = CenterHall(self.config)
        instance.crossRoom1()
        
        self.cs.back2Town()
        time.sleep(6)


    # 第二套刷经验
    def for_experience2(self):
        self.cs.selectHellOfHell()
        time.sleep(6)

        instance = HellOfFire(self.config)
        try:
            instance.crossRoom1()
        except GameStatusError as e:
            self.logger.info(f"{e}\n准备到附近传送点。")
            self.cs.clickGiveUpRebornBtn()
            time.sleep(8)
            self.logger.info("已到达复活传送点，准备回城。")
            self.cs.back2Town()
            self.logger.info("已经回到城镇。")
            time.sleep(10)
            # 循环
            self.for_experience2()


    # 刷木头
    def for_wood(self):
        self.cs.selectWoodInstance()
        instance = RottenSwamp(self.config)
        time.sleep(6)

        try:
            while True:
                instance.crossRoom1()
                instance.crossRoom2()
        except GameStatusError as e:
            self.logger.error(e)

        self.cs.back2Town()
        time.sleep(6)


    # 刷水晶
    def for_mine(self):
        self.cs.selectDiamondInstance()
        time.sleep(6)

        try:
            instance = SnowZone(self.config)
            instance.crossRoom1Loop()
        except GameStatusError as e:
            self.logger.error(e)

        self.cs.back2Town()
        time.sleep(6)


    # 自动打工，根据资源需求来打工
    def work(self):
        # 找到位置
        if(not self.reader.is_show_back2town_btn()):
            self.virtual_map.move2protal()

        # 流水线速度
        waitSec = 3.3

        isWoodFull, isMineFull = self.reader.read_screen()
        self.logger.info(f"木头:{isWoodFull}, 蓝矿:{isMineFull}")

        if(isWoodFull == False):
            self.logger.info("刷一刷木头副本")
            self.for_wood()

        elif(isMineFull == False):
            self.logger.info("刷一刷蓝矿")
            self.for_mine()

        else:
            self.logger.info("刷一刷经验")
            self.for_experience2()

        self.logger.info(f"本轮打金结束。{waitSec}s 后自动进入下一轮。")
        time.sleep(waitSec)
        self.work()


 

    # # 刷工会副本
    # def for_union_task(self):
    #     while True:
    #         # 检测是否完成工会副本
    #         if(self.reader.is_task_complete() == True):
    #             self.reader.close_task_menu(True)
    #             time.sleep(1.2)
    #             self.cs.clearAds(1)
    #             self.logger.info("工会任务已完成，无需再打")
    #             if(self.reader.is_show_back2town_btn()): 
    #                 self.cs.back2Town()
    #                 self.unionTask.refresh()
    #                 time.sleep(10)
    #             return
            
    #         self.reader.close_task_menu()
    #         # 工会副本任务没有完成，准备打工会副本
    #         self.logger.info(f"工会任务没有完成，打工会任务。")
            
    #         # 刷副本
    #         time.sleep(1.2)
            
    #         self.unionTask.farmingMagicRing()

    #         # GuildTask.farmingSnowfield()

    #         # GuildTask.farmingPollutionOutpost()

    #         # GuildTask.farmingColdWindCamp()

    