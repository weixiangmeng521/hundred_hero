import time
from defined import IS_UNION_TASK_FINISHED
from instance.union_task import UnionTask
from lib.cache import get_cache_manager_instance
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader
from lib.logger import init_logger


# 执行者，任务达人
class TaskExcutor:


    def __init__(self, config):
        self.config = config
        self.cs = ChallengeSelect(config)
        self.unionTask = UnionTask(config)
        self.reader = InfoReader(config)
        self.logger = init_logger(config)
        self.cache = get_cache_manager_instance(config)
        # 今日目标任务
        self.target_task_fn = None
        # 今日的任务名称
        self.target_task_name = ""
        # 手动分类
        self.task_mapping = {
            "击杀BOSS岩石巨像": self.unionTask.farmingStoneMenEfficiently,
            "击杀100名兽人弓手": self.unionTask.farmingColdWindCamp,
            "击杀100只冰霜傀儡": self.unionTask.farmingSnowfield,
        }

        # self.unionTask.farmingMagicRing()
        # self.unionTask.farmingSnowfield()
        # self.unionTask.farmingPollutionOutpost()
        # self.unionTask.farmingColdWindCamp()



    # 截取图片，取样
    def check_union_task_list(self):
        # 打开list
        self.cs.openTaskList()
        time.sleep(.6)
        # 读取list
        task_map = self.reader.read_task_list()
        self.logger.debug(f"任务列表:[{ task_map }]")
        for key, value in task_map.items():
            # 找到需要完成的任务
            if(key.find("击杀") != -1):
                fn = self.task_mapping.get(key)
                self.target_task_fn = fn
                self.target_task_name = key
                self.logger.info(f"今天需要完成的工会任务:[{ key }]")
                if(fn == None):
                    raise RuntimeError(f"[{ key }]的功能还没有完善.")
    

    # 刷工会副本
    def for_union_task(self):
        while True:
            self.check_union_task_list()
            # 检测是否完成工会副本
            if(self.reader.is_task_complete(self.target_task_name)):
                self.reader.close_task_menu(True)
                # 设置缓存
                self.cache.set(IS_UNION_TASK_FINISHED, 1)                
                time.sleep(1.2)
                self.cs.clearAds(1)
                self.logger.info("工会任务已完成，无需再打")
                # 是否显示回城按钮
                if(self.reader.is_show_back2town_btn()): 
                    self.cs.back2Town()
                    self.unionTask.refresh()
                    self.target_task_fn = None
                    time.sleep(10)
                return
            
            self.reader.close_task_menu()
            # 工会副本任务没有完成，准备打工会副本
            self.logger.info(f"工会任务没有完成，打工会任务。")
            
            # 刷副本
            time.sleep(1)

            # 执行目标对象
            if(self.target_task_fn):
                self.target_task_fn()
            time.sleep(1)
            


    # 执行任务
    def work(self):
        is_finished = self.cache.get(IS_UNION_TASK_FINISHED)
        # 如果完成了任务就直接结束。
        if(is_finished and int(is_finished) == 1):
            self.logger.info("工会任务已完成，无需再打")
            return

        self.for_union_task()