import math

import pyautogui
from instance.guild_quest import GuildQuest
from lib import ChallengeSelect, MoveControll, VisualTrack
from instance import GameStatusEror, black_rock, forest, snow_zone, hell_of_fire
import time
from reader import InfoReader


cPos = [262 , 696]
app_name = "百炼英雄"

# 选择关卡
cs = ChallengeSelect()
mc = MoveControll()
reader = InfoReader()
vt = VisualTrack()
GuildTask = GuildQuest()

# 需不需要唤醒
WAKE_UP_FLAG = True
# 需不需要刷工会副本
FARM_UNION_TASK_FLAG = False
# 无限训练营
UPGRADE_ABILITY_FOREVER = True


# wake up
def wake_up_window():
    # 把窗口拖动到桌面顶端
    cs.move2LeftTop(reader.is_game_loaded)



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
    except GameStatusEror as e:
        print(f"{e}\n准备到附近传送点。")
        cs.clickGiveUpRebornBtn()
        time.sleep(8)
        print("已到达复活传送点，准备回城。")
        cs.back2Town()
        print("已经回到城镇。")
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
    except GameStatusEror as e:
        print(e)

    cs.back2Town()
    time.sleep(6)


# 刷水晶
def work4Diamond():
    cs.selectDiamondInstance()
    time.sleep(6)

    try:
        instance = snow_zone.SnowZone()
        instance.crossRoom1Loop()
    except GameStatusEror as e:
        print(e)

    cs.back2Town()
    time.sleep(6)






# 刷工会副本
def work4Union():
    while True:
        # 检测是否完成工会副本
        if(reader.is_task_complete() == True):
            reader.close_task_menu(True)
            time.sleep(1.2)
            cs.clearAds(1)
            print("工会任务已完成，无需再打")
            if(reader.is_show_back2town_btn()): 
                cs.back2Town()
                GuildTask.refresh()
                time.sleep(10)
            return
        
        reader.close_task_menu()
        # 工会副本任务没有完成，准备打工会副本
        print(f"工会任务没有完成，打工会任务。")
        
        # 刷副本
        time.sleep(1.2)
        GuildTask.farmingColdWindCamp()
        




# TODO 刷金币
def earnMoney():

    print("完成中")


# 无限升级训练营
def improveAbility():
    # 流水线速度
    waitSec = 3.3    
    _, isMineFull = reader.read_screen()

    if(isMineFull == True):
        find_training_NPC()        

    if(isMineFull == False):
        print("刷一刷蓝矿")
        work4Diamond()

    time.sleep(waitSec)
    improveAbility()





# 执行函数
def main():
    # 流水线速度
    waitSec = 3.3

    isWoodFull, isMineFull = reader.read_screen()
    print(f"木头:{isWoodFull}, 蓝矿:{isMineFull}")

    if(isWoodFull == False):
        print("刷一刷木头副本")
        work4Wood()

    elif(isMineFull == False):
        print("刷一刷蓝矿")
        work4Diamond()

    else:
        print("刷一刷经验")
        work4Expeirence2()

    print(f"本轮打金结束。{waitSec}s 后自动进入下一轮。")
    time.sleep(waitSec)
    main()


# 矫正位置
def check_position():
    # 聚拢
    mc.move_left_down(.6)
    x, y, tx, ty = vt.find_position((0xc7, 0xd4, 0xb1), 5, 5)
    print(x, y, tx, ty)
    mc.move(x, y, tx, ty)


# 提升能力
def upgrade_ability():
    x, y, tx, ty = vt.find_position((106, 204, 66), 10, 10)
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
        print("没有找到训练营，重新定位...")

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
    print(point)
    mc.pointer_move_to(point[0], point[1] + 20)


# 唤醒
if(WAKE_UP_FLAG): wake_up_window()
# 打工会
if(FARM_UNION_TASK_FLAG): work4Union()
# 训练营
if(UPGRADE_ABILITY_FOREVER): improveAbility()




# main()
