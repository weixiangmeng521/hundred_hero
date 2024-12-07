import queue
import traceback
import cv2
import numpy as np
import pyautogui
from employee.bounty_hunter import BountyHunter
from employee.cards_master import CardsMaster
from employee.coach_NPC import CoachNPC
from employee.task_excutor import TaskExcutor
from employee.treasure_hunter import TreasureHunt
from exception.game_status import GameStatusError
from employee.farmer import Farmer
from instance.union_task import UnionTask
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader
from lib.logger import init_logger
from lib.message_service import MessageService
from lib.move_controller import MoveControll
from lib.app_trace import AppTrace
from lib.threads_manager import ThreadsManager
from lib.virtual_map import VirtualMap, init_virtual_map
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
# web服务
webServer = WebServer(config)
# 虚拟map
virtualMap = init_virtual_map(config)
# 配置twilio
pusher = MessageService(config)
# 定义队列用于线程间通信
event_queue = queue.Queue()
# 初始化多线程管理器
threadsManager = ThreadsManager(config, event_queue)


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
# 无限打钱
ENABLE_AUTO_COIN = config.getboolean('TASK', 'EnableAutoCoin')
# 无限刷资源
ENABLE_AUTO_WOOD_AND_MINE = config.getboolean('TASK', 'EnableAutoWoodAndMine')
# 无限刷资源
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
        # 打工会
        if(ENABLE_AUTO_UNION_TASK): taskExcutor.work()
        # 训练营
        if(ENABLE_AUTO_ABILITY_IMPROVE): coachNPC.work()
        # 抽卡
        if(ENABLE_AUTO_GACHA): cardsMaster.work()
        # 刷30个箱子
        if(ENABLE_AUTO_DAILY_CASE): treasureHunter.work()
        # 打钱
        if(ENABLE_AUTO_COIN): bountyHunter.work()
        # 刷资源
        if(ENABLE_AUTO_WOOD_AND_MINE): farmer.work()
        # 虚拟map
        if(ENABLE_VIRTUAL_MAP): virtualMap.work(event_queue)

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
        threadsManager.add_task("WorkThread", work_thread)
        # 是否需要添加web server
        if config.getboolean('WEB_SERVER', 'Enable'):
            threadsManager.add_task("WebServer", webServer.run)

        threadsManager.run()

    if(not ENABLE_DEAMON):
        work_thread(event_queue)


if __name__ == "__main__":
    main()


    # vc.test_for_find_object_in_image()

    # print(pyautogui.position())