import datetime
import os
import traceback
import cv2
import numpy as np
import pyautogui
from farm import farmCoin
from gacha import Gacha
from instance.guild_quest import GuildQuest
from lib import ChallengeSelect, MoveControll, VisualTrack
from instance import GameStatusError, black_rock, forest, snow_zone, hell_of_fire
import time
from lib.logger import init_logger
from reader import InfoReader


cPos = [262 , 696]
app_name = "百炼英雄"

# 选择关卡
cs = ChallengeSelect()
mc = MoveControll()
reader = InfoReader()
vt = VisualTrack(app_name)
GuildTask = GuildQuest()
gc = Gacha(app_name)
logger = init_logger(app_name)

# 是否允许截图
IS_ALLOW_SCREEN_SHOT = True
# 需不需要唤醒
WAKE_UP_FLAG = True
# 是否有加载广告
IS_LOADING_ADS = True
# 刷工会副本
FARM_UNION_TASK_FLAG = False
# 无限训练营
UPGRADE_ABILITY_FOREVER = False
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



# 刷经验
def work4Expeirence1():
    cs.selectExpeirenceInstance()
    time.sleep(6)

    time.sleep(3)
    instance = black_rock.CenterHall()
    instance.crossRoom1()
    
    cs.back2Town()
    time.sleep(6)


# 第二套刷经验
def work4Expeirence2():
    cs.selectHellOfHell()
    time.sleep(6)

    instance = hell_of_fire.HellOfFire()
    try:
        instance.crossRoom1()
    except GameStatusError as e:
        logger.info(f"{e}\n准备到附近传送点。")
        cs.clickGiveUpRebornBtn()
        time.sleep(8)
        logger.info("已到达复活传送点，准备回城。")
        cs.back2Town()
        logger.info("已经回到城镇。")
        time.sleep(10)
        # 循环
        work4Expeirence2()


# 刷木头
def work4Wood():
    cs.selectWoodInstance()
    instance = forest.RottenSwamp()
    time.sleep(6)

    try:
        while True:
            instance.crossRoom1()
            instance.crossRoom2()
    except GameStatusError as e:
        logger.error(e)

    cs.back2Town()
    time.sleep(6)


# 刷水晶
def work4Diamond():
    cs.selectDiamondInstance()
    time.sleep(6)

    try:
        instance = snow_zone.SnowZone()
        instance.crossRoom1Loop()
    except GameStatusError as e:
        logger.error(e)

    cs.back2Town()
    time.sleep(6)






# 刷工会副本
def work_4_union():
    while True:
        # 检测是否完成工会副本
        if(reader.is_task_complete() == True):
            reader.close_task_menu(True)
            time.sleep(1.2)
            cs.clearAds(1)
            logger.info("工会任务已完成，无需再打")
            if(reader.is_show_back2town_btn()): 
                cs.back2Town()
                GuildTask.refresh()
                time.sleep(10)
            return
        
        reader.close_task_menu()
        # 工会副本任务没有完成，准备打工会副本
        logger.info(f"工会任务没有完成，打工会任务。")
        
        # 刷副本
        time.sleep(1.2)
        
        GuildTask.farmingMagicRing()

        # GuildTask.farmingSnowfield()

        # GuildTask.farmingPollutionOutpost()

        # GuildTask.farmingColdWindCamp()

        



# 无限升级训练营
def improve_ability():
    # 流水线速度
    waitSec = 3.3    
    _, isMineFull = reader.read_screen()

    if(isMineFull == True):
        find_training_NPC()        

    if(isMineFull == False):
        logger.info("刷一刷蓝矿")
        work4Diamond()

    time.sleep(waitSec)
    improve_ability()





# 执行函数
def main():
    # 流水线速度
    waitSec = 3.3

    isWoodFull, isMineFull = reader.read_screen()
    logger.info(f"木头:{isWoodFull}, 蓝矿:{isMineFull}")

    if(isWoodFull == False):
        logger.info("刷一刷木头副本")
        work4Wood()

    elif(isMineFull == False):
        logger.info("刷一刷蓝矿")
        work4Diamond()

    else:
        logger.info("刷一刷经验")
        work4Expeirence2()

    logger.info(f"本轮打金结束。{waitSec}s 后自动进入下一轮。")
    time.sleep(waitSec)
    main()


# 矫正位置
def check_position():
    # 聚拢
    mc.move_left_down(.6)
    x, y, tx, ty = vt.find_position((0xc7, 0xd4, 0xb1), 5, 5)
    mc.move(x, y, tx, ty)


# 提升能力
def upgrade_ability():
    _, _, tx, ty = vt.find_position((106, 204, 66), 10, 10)
    # 无视资源区域
    if(ty < 100): return
    
    pyautogui.click(tx - 25, ty + 40)
    time.sleep(.3)
    pyautogui.click(tx - 25, ty)
    time.sleep(1)



# 找到训练营
def find_training_NPC():
    x, y, tx, ty = vt.find_position((205, 196, 214), 0, 0)
    # 如果没有找到目标就重新定位。
    if((x == tx and y == ty)):
        time.sleep(1)
        find_training_NPC()
        logger.info("没有找到训练营，重新定位...")

    if(not (x == tx and y == ty)):
        tolerate_distance = vt.get_point_distance(x, y, tx, ty)
        # 如果小于10像素，就算是移动到指定目的地了
        if(tolerate_distance >= 10):
            mc.move(x, y, tx, ty)

    # 点击绿泡泡
    cs.clickGreenPop()
    time.sleep(.3)
    upgrade_ability()
    reader.close_task_menu()
    time.sleep(.3)

    # 返回
    mc.move(tx, ty, x, y)
    time.sleep(.3)




# 获取当前画面绿色冒泡的列表
def get_pop_list():
    _list = vt.get_targets_list((0x66,0xc1,0x52), 20, 20)
    point = vt.get_shortest_point(_list)
    logger.info(point)
    mc.pointer_move_to(point[0], point[1] + 20)


# 时间格式输出
def record_time_formate(execution_time, earned):
        # 转换为分钟和秒
    minutes = int(execution_time // 60)
    seconds = execution_time % 60
    rate =  earned / execution_time
    hour_earned = rate * 60 * 60
    logger.debug(f"打金耗时: {minutes}m {seconds:.2f}s, 1h刷金预计: {hour_earned:.2f}")



# 打金
def farming_coin():
    total = 0
    while True:
        # 开始计时
        start_time = time.time()
        # 刷副本
        earned = farmCoin()
        total += earned
        logger.info(f"💰总打金:{ total }")
        # 关闭游戏
        cs.closeGame()
        # 结束计时
        end_time = time.time()
        record_time_formate(end_time - start_time, earned)
        # 启动游戏
        wake_up_window()


# 自动抽卡
def auto_card():
    is_entered_interface = gc.is_entered()

    # 判断是否已经进入抽卡界面
    if(not is_entered_interface):
        x, y, tx, ty = vt.find_position((210, 174, 109), 0, 0)
        # 如果没有找到目标就重新定位。
        if((x == tx and y == ty)):
            time.sleep(1)
            logger.debug("没有找到抽卡中心，重新定位...")
            auto_card()

        if(not (x == tx and y == ty)):
            tolerate_distance = vt.get_point_distance(x, y, tx, ty)
            # 如果小于10像素，就算是移动到指定目的地了
            if(tolerate_distance >= 10):
                mc.move(x, y, tx, ty)
        # 定位到，点击绿色泡泡
        cs.clickGreenPop()
        time.sleep(.3)

    while True:
        # 如果不能点击了，就结束
        try:
            gc.auto_recruit_btn()
        except GameStatusError as e:
            logger.debug(e.get_error_info())
            break

    # 关闭抽卡，返回
    reader.close_task_menu()
    time.sleep(.1)
    
    # 判断是否已经进入抽卡界面
    if(not is_entered_interface):
        mc.move(tx, ty, x, y)

    # 寻找蓝色传送台
    if(is_entered_interface):
        x, y, tx, ty = vt.find_position((0xc7, 0xd4, 0xb1), 5, 5)
        mc.move(x, y, tx, ty)

# 截屏，查看bug信息
def screen_shot():
    if(IS_ALLOW_SCREEN_SHOT == False): 
        return

    log_dir = "screenshot"  # 子文件夹名称
    if not os.path.exists(log_dir):  # 如果文件夹不存在，则创建
        os.makedirs(log_dir)

    screenshot = pyautogui.screenshot()
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path = f"screenshot/{timestamp}.png"
    cv2.imwrite(path, img)
    logger.debug(f"已经保存截图到:{path}")


# 错误处理
def error_handle():
    play_sound("Glass.aiff")
    screen_shot()
    cs.closeGameWithoutException()
    time.sleep(.3)
    __init__()


# 播放声音
def play_sound(file_name):
    os.system(f"afplay /System/Library/Sounds/{file_name}")


# 初始函数
def __init__():
    # 唤醒
    if(WAKE_UP_FLAG): wake_up_window()
    # 打工会
    if(FARM_UNION_TASK_FLAG): work_4_union()
    # 训练营
    if(UPGRADE_ABILITY_FOREVER): improve_ability()
    # 抽卡
    if(IS_AUTO_GACHA): auto_card()
    # 打钱
    if(IS_AUTO_FARM): farming_coin()
    # 刷资源
    if(IS_AUTO_WOOD_AND_MINE): main()



try:
    __init__()

except (RuntimeError, GameStatusError, TimeoutError) as e:
    stack_info = traceback.format_exc()
    logger.error(f"{e}, {stack_info}")
    error_handle()

except KeyboardInterrupt:
    print("正常结束")

except Exception as e:
    stack_info = traceback.format_exc()
    logger.error(f"{e}, {stack_info}")
    play_sound("Ping.aiff")




