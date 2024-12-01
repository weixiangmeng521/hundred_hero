import traceback
import numpy as np
from employee.bounty_hunter import BountyHunter
from employee.cards_master import CardsMaster
from employee.coach_NPC import CoachNPC
from employee.task_excutor import TaskExcutor
from exception.game_status import GameStatusError
from employee.farmer import Farmer
from instance.union_task import UnionTask
import time
from lib.challenge_select import ChallengeSelect
from lib.info_reader import InfoReader
from lib.logger import init_logger
from lib.message import MessageService
from lib.move_controller import MoveControll
from lib.app_trace import AppTrace
from lib.threads_manager import ThreadsManager
from lib.visual_track import VisualTrack
import configparser


# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 选择关卡
cs = ChallengeSelect(config)
mc = MoveControll(config)
reader = InfoReader(config)
vt = VisualTrack(config)
unionTask = UnionTask(config)
cardsMaster = CardsMaster(config)
logger = init_logger(config)
bountyHunter = BountyHunter(config)
farmer = Farmer(config)
taskExcutor = TaskExcutor(config)
trace = AppTrace(config)
coachNPC = CoachNPC(config)
threadsManager = ThreadsManager(config)


# 配置twilio
pusher = MessageService(config)

app_name = config["APP"]["Name"]
# 需不需要唤醒
IS_WAKE_UP_APP = True
# 是否有加载广告
IS_LOADING_ADS = True
# 刷工会副本
FARM_UNION_TASK = False
# 无限训练营
IS_ABILITY_AIM = False
# 无限抽卡
IS_AUTO_GACHA = False
# 无限打钱
IS_AUTO_FARM = True
# 无限刷资源
IS_AUTO_WOOD_AND_MINE = False



# wake up
def wake_up_window():
    # 把窗口拖动到桌面顶端
    cs.move2LeftTop(reader.wait_game_loaded, IS_LOADING_ADS)


# 工作线程
def work_thread(name):
    try:
        # 唤醒
        if(IS_WAKE_UP_APP): wake_up_window()
        # 打工会
        if(FARM_UNION_TASK): taskExcutor.work()
        # 训练营
        if(IS_ABILITY_AIM): coachNPC.work()
        # 抽卡
        if(IS_AUTO_GACHA): cardsMaster.work()
        # 打钱
        if(IS_AUTO_FARM): bountyHunter.work()
        # 刷资源
        if(IS_AUTO_WOOD_AND_MINE): farmer.work()

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
    threadsManager.add_task("WorkThread", work_thread)
    threadsManager.run()


if __name__ == "__main__":
    main()