import difflib
import time
from defined import IS_UNION_TASK_FINISHED
from employee.human import Human
from instance.union_task import UnionTask
from lib.cache import get_cache_manager_instance
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader
from lib.logger import init_logger
from lib.select_hero import SelectHero
from lib.virtual_map import init_virtual_map


# 执行者，任务达人
class TaskExcutor(Human):

    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.cs = ChallengeSelect(config)
        self.unionTask = UnionTask(config)
        self.reader = InfoReader(config)
        self.logger = init_logger(config)
        self.cache = get_cache_manager_instance(config)
        self.virtual_map = init_virtual_map(config)
        self.selectHero = SelectHero(config)
        # 今日目标任务
        self.target_task_fn = None
        # 今日的任务名称
        self.target_task_name = ""
        # 手动分类
        self.task_mapping = {
            "击杀BOSS岩石巨像": self.unionTask.farmingStoneMenEfficiently,
            "击杀100名兽人弓手": self.unionTask.farmingColdWindCamp,
            "击杀100只冰霜傀儡": self.unionTask.farmingSnowfield,
            "击杀100名娜迦法师": self.unionTask.farmingSnowfield,
            "击杀100名树精斥候": self.unionTask.farmingNorthRottingSwamp,
            "击杀100只小雪人": self.unionTask.farmingMagicRing,
            "击杀100只大雪怪": self.unionTask.farmingBigIceMonster,
            "击杀100名树精守卫": self.unionTask.farmingColdWindCamp,
            "击杀BOSS冰雪巨人": self.unionTask.farmingIceGiant,
            "击杀BOSS三头怪蛇": self.unionTask.farmingTwoHeadSnake,
            "击杀BOSS猛犸巨像": self.unionTask.farmingMammoth,
            "击杀100只红眼蝙蝠": self.unionTask.farmingPollutionOutpost,
            "击杀100只剧毒黑蜂": self.unionTask.farmingPollutionOutpost,
            "击杀100只霜狼": self.unionTask.farmingMagicRing,
            "击杀100名海豹人法师": self.unionTask.farmingSnowfield,
            "采集木头270次": self.unionTask.farmingTree,
        }

        # self.unionTask.farmingMagicRing()
        # self.unionTask.farmingSnowfield()
        # self.unionTask.farmingPollutionOutpost()
        # self.unionTask.farmingColdWindCamp()
    
    
    # 获取与输入字符串最相似的键
    def find_best_match(self, input_str, task_mapping):
        best_match = difflib.get_close_matches(input_str, task_mapping.keys(), n=1, cutoff=0.5)
        if best_match:
            return best_match[0], task_mapping[best_match[0]]
        else:
            return None, None


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
            if(key.find("击杀") != -1 or key.find("采集") != -1):
                # 直接取值
                task = self.task_mapping.get(key)        
                if(task):
                    self.target_task_fn = task
                    self.target_task_name = key                    
                    self.logger.info(f"今天需要完成的工会任务:[{ key }]")
                    return

                # 模糊匹配
                best_key, task = self.find_best_match(key, self.task_mapping)
                if(best_key):
                    self.target_task_fn = task
                    self.target_task_name = key
                    self.logger.info(f"[模糊匹配]今天需要完成的工会任务:[{ best_key }]")
                    return

                # 匹配失败
                self.reader.save_union_task_img()
                raise RuntimeError(f"[{ key }]的功能还没有完善.")


    # 刷工会副本
    def for_union_task(self):
        # 查看是否是全员上阵
        is_full = self.reader.is_team_member_full()
        if(not is_full):
            self.logger.info("全部英雄上阵。")
            self.selectHero.dispatch_all_hero()
                    
        while True:
            self.check_union_task_list()
            # 检测是否完成工会副本
            if(self.reader.is_task_complete(self.target_task_name)):                
                self.reader.close_task_menu(True)
                # 设置缓存
                self.cache.set(IS_UNION_TASK_FINISHED, 1)
                self.logger.info("工会任务已完成，无需再打")
                # 是否显示回城按钮
                if(self.reader.is_show_back2town_btn()): 
                    self.cs.back2Town()
                    self.unionTask.refresh()
                    self.target_task_fn = None
                    self.reader.wait_tranported()
                return
            
            self.reader.close_task_menu()
            # 工会副本任务没有完成，准备打工会副本
            self.logger.info(f"工会任务没有完成，打工会任务。")
            
            # 刷副本
            time.sleep(.1)

            # 执行目标对象
            if(self.target_task_fn):
                self.target_task_fn()
            time.sleep(.1)
            


    # 执行任务
    # TODO: 检测效率
    def work(self):
        # 找到位置
        if(not self.reader.is_show_back2town_btn()):
            self.virtual_map.move2protal()
            
        # 判断是否是完成了任务
        is_finished = self.cache.get(IS_UNION_TASK_FINISHED)
        # 如果完成了任务就直接结束。
        if(is_finished and int(is_finished) == 1):
            self.logger.info("工会任务已完成，无需再打")
            return
        # 设置默认值
        if(not is_finished):
            self.cache.set(IS_UNION_TASK_FINISHED, 0)

        self.for_union_task()
