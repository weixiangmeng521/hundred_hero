import queue
import time
import traceback

import pyautogui
from defined import IS_DALIY_ARENA_FINISHED
from employee.bounty_hunter import BountyHunter
from employee.cards_master import CardsMaster
from employee.coach_NPC import CoachNPC
from employee.fighter import Fighter
from employee.task_excutor import TaskExcutor
from employee.tower_warrior import TowerWarrior
from employee.treasure_hunter import TreasureHunt
from exception.game_status import GameStatusError
from employee.farmer import Farmer
from instance.union_task import UnionTask
from lib.cache import get_cache_manager_instance
from lib.challenge_select import ChallengeSelect
from lib.controll_wechat import init_controll_wechat
from lib.info_reader import InfoReader
from lib.logger import init_logger
from lib.logger_analysis import get_logger_analysis_instance
from lib.message_service import MessageService
from lib.move_controller import MoveControll
from lib.app_trace import AppTrace
from lib.select_hero import SelectHero
from lib.threads_manager import ThreadsManager
from lib.virtual_map import init_virtual_map
from lib.visual_track import VisualTrack
import configparser

from server.web_server import WebServer


# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 选择关卡
cs = ChallengeSelect(config)
vc = VisualTrack(config)
mc = MoveControll(config)
wechat = init_controll_wechat(config)
reader = InfoReader(config)
unionTask = UnionTask(config)
cardsMaster = CardsMaster(config)
logger = init_logger(config)
bountyHunter = BountyHunter(config)
farmer = Farmer(config)
taskExcutor = TaskExcutor(config)
trace = AppTrace(config)
coachNPC = CoachNPC(config)
treasureHunter = TreasureHunt(config)
fighter = Fighter(config)
warrior = TowerWarrior(config)
selectHero = SelectHero(config)


# web服务
webServer = WebServer(config)
# 虚拟map
virtualMap = init_virtual_map(config)
# 配置twilio
pusher = MessageService(config)
# 定义队列用于线程间通信
event_queue = queue.Queue()
# 初始化多线程管理器
threads_manager = ThreadsManager(config, event_queue)


# 是否守护线程
ENABLE_DEAMON = config.getboolean('THREADS', 'EnableDeamon')
# 需不需要唤醒
IS_WAKE_UP_APP = config.getboolean('TASK', 'IsWakeUpApp')
# 是否有加载广告
IS_LOADING_ADS = config.getboolean('TASK', 'IsLoadingAds')
# 刷工会副本
ENABLE_AUTO_UNION_TASK = config.getboolean('TASK', 'EnableAutoUnionTask')
# 无限训练营
ENABLE_AUTO_ABILITY_IMPROVE = config.getboolean('TASK', 'EnableAutoAbilityImporve')
# 无限抽卡
ENABLE_AUTO_GACHA = config.getboolean('TASK', 'EnableAutoGaCha')
# 刷每日箱子
ENABLE_AUTO_DAILY_CASE = config.getboolean('TASK', 'EnableAutoDaliyCase')
# 刷每日元素塔
ENABLE_AUTO_DAILY_ELEMENT_TOWER = config.getboolean('TASK', 'EnableAutoDaliyElementTower')
# 无限格斗
ENABLE_AUTO_FRIGHT = config.getboolean("TASK", "EnableAutoFight")
# 无限打钱
ENABLE_AUTO_COIN = config.getboolean('TASK', 'EnableAutoCoin')
# 无限刷资源
ENABLE_AUTO_WOOD_AND_MINE = config.getboolean('TASK', 'EnableAutoWoodAndMine')
# 虚拟地图
ENABLE_VIRTUAL_MAP = config.getboolean('TASK', 'EnableVirtualMap')

# wake up
def wake_up_window():
    # 把窗口拖动到桌面顶端
    cs.move2LeftTop(reader.wait_game_loaded, IS_LOADING_ADS)


# 工作线程
def work_thread(event_queue):
    try:
        # 唤醒
        if(IS_WAKE_UP_APP): wake_up_window()
        # 虚拟map, 测试用
        if(ENABLE_VIRTUAL_MAP): 
            virtualMap.work(event_queue)
            return

        # 打工会
        if(ENABLE_AUTO_UNION_TASK): taskExcutor.work()
        # 打架
        if(ENABLE_AUTO_FRIGHT): fighter.work()        
        # 刷每日元素塔
        if(ENABLE_AUTO_DAILY_ELEMENT_TOWER): warrior.work()               
        # 抽卡
        if(ENABLE_AUTO_GACHA): cardsMaster.work()
        # 刷30个箱子
        if(ENABLE_AUTO_DAILY_CASE): treasureHunter.work()
        
        # TODO: 下面的划分为重任务，也叫体力任务。体力任务执行的时候加上检测
        # 训练营
        if(ENABLE_AUTO_ABILITY_IMPROVE): coachNPC.work()        
        # 打钱
        if(ENABLE_AUTO_COIN): bountyHunter.work()
        # 刷资源
        if(ENABLE_AUTO_WOOD_AND_MINE): farmer.work()


    except (RuntimeError, GameStatusError, TimeoutError) as e:
        stack_info = traceback.format_exc()
        logger.error(f"{e}, {stack_info}")
        trace.report_error(e)

    except Exception as e:
        stack_info = traceback.format_exc()
        logger.error(f"{e}, {stack_info}")
        trace.play_sound("Ping.aiff")


# 入口函数
def main():
    if(ENABLE_DEAMON):
        threads_manager.add_task("WorkThread", work_thread)
        # 是否需要添加web server
        if config.getboolean('WEB_SERVER', 'Enable'):
            threads_manager.add_task("WebServer", webServer.run)

        threads_manager.run()

    if(not ENABLE_DEAMON):
        work_thread(event_queue)

# TODO: 获取当前钱的数量,并放入缓存里
if __name__ == "__main__":
    main()

    # wechat.wake_up()
    # selectHero.dispatch_target_hero()

    # webServer.run(queue)

    # vc.test_for_find_object_in_image()
    # print(pyautogui.position())