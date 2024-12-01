import time

import cv2
import numpy as np
from instance.union_task import UnionTask
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
        # 今日目标任务
        self.target_task_fn = None
        # 手动分类
        self.task_mapping = {
            "击杀BOSS岩石巨像": self.unionTask.farmingRottingSwamp,


        }
        # self.unionTask.farmingMagicRing()
        # self.unionTask.farmingSnowfield()
        # self.unionTask.farmingPollutionOutpost()
        # self.unionTask.farmingColdWindCamp()
        # self.unionTask.farmingColdWindCamp()


    # 截取图片，取样
    def check_union_task_list(self, task_map):
        for key, value in task_map.items():
            # 找到需要完成的任务
            if(key.find("击杀") != -1 and bool(value)):
                fn = self.task_mapping.get(key)
                self.target_task_fn = fn
                self.logger.debug(f"今天需要完成的工会任务:[{ key }]")
    

    # 刷工会副本
    def for_union_task(self):
        while True:
            # 检测是否完成工会副本
            if(self.reader.is_task_complete(self.check_union_task_list) == True):
                self.reader.close_task_menu(True)
                time.sleep(1.2)
                self.cs.clearAds(1)
                self.logger.info("工会任务已完成，无需再打")
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
            time.sleep(1.2)

            # 执行目标对象
            if(self.target_task_fn):
                self.target_task_fn()
            


    # 执行任务
    def work(self):
        self.for_union_task()