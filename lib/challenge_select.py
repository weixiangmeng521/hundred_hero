import os
import pygetwindow
from pynput.mouse import Controller
import pyautogui
import time
import Quartz
import sys
import cv2
from PIL import Image
import numpy as np
import math
from lib.controll_wechat import ControllWechat
from lib.logger import init_logger
from lib.virtual_map import init_virtual_map
from lib.visual_track import VisualTrack


cPos = [222 , 696]
back2TownPos = [425, 786]
yesBtnPos = [302, 540]
challengePopPos = [282, 400]

# 平原系
flatlandBtnPos = [142, 280]
chorchHillBtnPos = [302, 365]


# 荒芜之地
poorZoneBtnPos = [142, 330]
poorCampPosBtnPos = [302, 285]
twoPeakPosBtnPos = [302, 365]


# 黑石系
blackRockBtnPos = [142, 630]
centerHallBtnPos = [302, 440]

# 严寒地带系
snwoMapBtnPos = [121, 440]
snowBtnPos = [302, 360]
snowRingBtnPos = [302, 290]

# 污染之森系列
forestMapBtnPos = [121, 380]
decayedSwampBtnPos = [302, 360]
pollutionOutpostBtnPos = [302, 300]
coldWindCampBtnPos = [302, 450]

# 冰冠堡垒
IconcrownMapBtnPos = [121, 500]
IconcrownThroneBtnPos = [302, 285]


# 地狱火副本
hellInstanceTabPos = [337, 750]
# 炎狱之层
fireOfHellLayerTabPos = [121, 330]
fireOfHellInstancePos = [300, 530]
# 炽晶之地
fireMineLandTabPos = [121, 260]
twoCentipedePos = [302, 360]

# 任务列表
taskListBtnPos = [445, 385]
unionTaskTabPos = [390 , 840]
completeUnionTaskTabPos = [370 , 385]

# 关闭窗口的btn
closeBtnPos = [85, 840]

# 放弃复活
giveUpRebornBtn = [315, 740]


# 元素塔的pos
elementTowerTabPos = [399, 847]



# 选择关卡
class ChallengeSelect:
    def __init__(self, config):
        self.config = config
        self.app_name = config["APP"]["Name"]
        self.logger = init_logger(config)
        self.wechat = ControllWechat(self.config)
        self.virtual_map = init_virtual_map(config)
        self.waitTime = .1


    # 获取窗口信息
    def get_specific_window_info(self):
        # 获取所有在屏幕上的窗口信息
        options = Quartz.kCGWindowListOptionOnScreenOnly
        window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)
        
        # 查找指定窗口
        for window in window_list:
            window_name = window.get('kCGWindowName', '')
            if self.app_name in window_name:
                return window  # 返回指定窗口的信息
        return None
    
    
    # 获取窗口信息
    def get_win_info(self):
        window = self.get_specific_window_info()
        if(window == None): raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
        window_bounds = window.get('kCGWindowBounds', {})
        winX, winY = window_bounds.get('X', 0), window_bounds.get('Y', 0)
        winWidth, winHeight = window_bounds.get('Width', 0), window_bounds.get('Height', 0)
        return winX, winY, winWidth, winHeight
    

    # 点击最近的绿色冒泡
    def clickGreenPop(self):
        # 超时时间，单位为秒
        timeout = 30

        # 寻找绿泡泡
        start_time = time.time()  # 记录开始时间
        while True:
            # 寻找绿泡泡
            vt = VisualTrack(self.config)
            green = (0x66,0xc1,0x52)
            _list = vt.get_targets_list(green, 20, 20)
            point = vt.get_shortest_point(_list)
            # 找到的绿泡泡
            if(len(point) == 0):
                elapsed_time = time.time() - start_time  # 计算已过去的时间
                # 超时结算
                if elapsed_time > timeout:
                    raise TimeoutError(f"{timeout}s内未找到绿色泡泡, 位置可能偏移...")
                
                # 多次尝试
                time.sleep(.3)
                self.logger.debug(f"{30}s内,尝试寻找绿泡泡。")
                continue
            # 结束循环
            break
        

        # 点击绿泡泡
        start_time = time.time()  # 记录开始时间
        while True:
            self.logger.info("点击绿色对话泡")
            pyautogui.click(point[0], point[1] + 20)

            # 检查是否点击成功
            x, y, tx, ty = vt.find_position(green, 0, 0)
            # 点击失败的情况
            if(x != tx and y != ty):
                elapsed_time = time.time() - start_time  # 计算已过去的时间
                # 超时结算
                if elapsed_time > timeout:
                    print(f"find_position: {x}, {y}, {tx}, {ty}")
                    raise TimeoutError(f"{timeout}s内点击无效, 位置可能偏移...")
                
                # 多次尝试
                time.sleep(.3)
                self.logger.debug(f"{30}s内,尝试成功点击绿泡泡。")
                continue
            # 结束循环
            break

    # 检查窗口状态
    def check_window_handler(self):
        if(self.get_specific_window_info() == None): 
            raise RuntimeError('Err', f"{self.app_name}`s window is not found.")


    # 刷经验
    def selectExpeirenceInstance(self):
        self.check_window_handler()
        self.clickGreenPop()
        # self.logger.info(f"副本选择被点击")
        time.sleep(self.waitTime)
        pyautogui.click(blackRockBtnPos[0], blackRockBtnPos[1])
        # self.logger.info(f"黑石堡垒被点击")
        time.sleep(self.waitTime)
        pyautogui.click(centerHallBtnPos[0], centerHallBtnPos[1])
        self.logger.info(f"进入[中央走廊]")


    # 刷木头
    def selectWoodInstance(self):
        self.check_window_handler()
        self.clickGreenPop()
        # self.logger.info(f"副本选择被点击")
        time.sleep(self.waitTime)
        pyautogui.click(forestMapBtnPos[0], forestMapBtnPos[1])
        # self.logger.info(f"污染之森点击")
        time.sleep(self.waitTime)
        pyautogui.click(decayedSwampBtnPos[0], decayedSwampBtnPos[1])
        # self.logger.info(f"污染之森点击")
        self.logger.info("进入[污染之森]")


    # 污染之林的污染前哨
    def selectPollutionOutpost(self):
        self.check_window_handler()
        self.clickGreenPop()
        time.sleep(self.waitTime)
        pyautogui.click(forestMapBtnPos[0], forestMapBtnPos[1])        
        time.sleep(self.waitTime)
        pyautogui.click(pollutionOutpostBtnPos[0], pollutionOutpostBtnPos[1])
        self.logger.info("进入[污染前哨]")
    
    # [打金]刷前哨平原的副本
    def selectFrontFlatland(self):
        self.check_window_handler()
        self.clickGreenPop()
        time.sleep(self.waitTime)
        pyautogui.click(flatlandBtnPos[0], flatlandBtnPos[1])        
        time.sleep(self.waitTime)
        pyautogui.click(chorchHillBtnPos[0], chorchHillBtnPos[1])
        self.logger.info("进入[前哨平原]")


    # [打金]贫瘠营地
    def selectPoorCamp(self):
        self.check_window_handler()
        self.clickGreenPop()
        time.sleep(self.waitTime)
        pyautogui.click(poorZoneBtnPos[0], poorZoneBtnPos[1])        
        time.sleep(self.waitTime)
        pyautogui.click(poorCampPosBtnPos[0], poorCampPosBtnPos[1])
        self.logger.info("进入[贫瘠营地]")


    # [打金]双峰峡谷
    def selectTwoPeak(self):
        self.check_window_handler()
        self.clickGreenPop()
        time.sleep(self.waitTime)
        pyautogui.click(poorZoneBtnPos[0], poorZoneBtnPos[1])        
        time.sleep(self.waitTime)
        pyautogui.click(twoPeakPosBtnPos[0], twoPeakPosBtnPos[1])
        self.logger.info("进入[双峰峡谷]")


    # 刷寒风营地的副本
    def selectColdWindCamp(self):
        self.check_window_handler()
        self.clickGreenPop()
        time.sleep(self.waitTime)
        pyautogui.click(forestMapBtnPos[0], forestMapBtnPos[1])        
        time.sleep(self.waitTime)
        pyautogui.click(coldWindCampBtnPos[0], coldWindCampBtnPos[1])
        self.logger.info("进入[寒风营地]")


    # 刷水晶
    def selectDiamondInstance(self):
        self.check_window_handler()
        self.clickGreenPop()
        # self.logger.info(f"副本选择被点击")
        time.sleep(self.waitTime)
        pyautogui.click(snwoMapBtnPos[0], snwoMapBtnPos[1])
        # self.logger.info(f"严寒地带点击")
        time.sleep(self.waitTime)
        pyautogui.click(snowBtnPos[0], snowBtnPos[1])
        # self.logger.info(f"北风营地点击")
        self.logger.info("进入[北风营地]")


    # 选择魔力之环
    def selectSnowInstance(self):
        self.check_window_handler()
        self.clickGreenPop()
        # self.logger.info(f"副本选择被点击")
        time.sleep(self.waitTime)
        pyautogui.click(snwoMapBtnPos[0], snwoMapBtnPos[1])
        # self.logger.info(f"严寒地带点击")
        time.sleep(self.waitTime)
        pyautogui.click(snowRingBtnPos[0], snowRingBtnPos[1])
        # self.logger.info(f"北风营地点击")
        self.logger.info("进入[魔力之环]")


    # 冰冠堡垒的王座大厅
    def selectIcecrownThrone(self):
        self.check_window_handler()
        self.clickGreenPop()
        time.sleep(self.waitTime)
        pyautogui.click(IconcrownMapBtnPos[0], IconcrownMapBtnPos[1])
        time.sleep(self.waitTime)
        pyautogui.click(IconcrownThroneBtnPos[0], IconcrownThroneBtnPos[1])
        self.logger.info("进入[王座大厅]")


    # 选择双虫
    def selectTwoCentipede(self):
        self.check_window_handler()
        self.clickGreenPop()
        time.sleep(self.waitTime)
        pyautogui.click(hellInstanceTabPos[0], hellInstanceTabPos[1])        
        time.sleep(self.waitTime)
        pyautogui.click(fireMineLandTabPos[0], fireMineLandTabPos[1])
        time.sleep(self.waitTime)
        pyautogui.click(twoCentipedePos[0], twoCentipedePos[1])
        self.logger.info("进入[蜈蚣岗]")

    
    # 查看任务栏的任务
    def openTaskList(self):
        self.check_window_handler()
        pyautogui.click(taskListBtnPos[0], taskListBtnPos[1])
        time.sleep(self.waitTime)
        pyautogui.click(unionTaskTabPos[0], unionTaskTabPos[1])
        self.logger.info("进入[工会任务列表]")


    # 选择炎火之狱副本
    def selectHellOfHell(self):
        self.check_window_handler()
        self.clickGreenPop()
        time.sleep(self.waitTime)
        pyautogui.click(hellInstanceTabPos[0], hellInstanceTabPos[1])
        time.sleep(self.waitTime)
        pyautogui.click(fireOfHellLayerTabPos[0], fireOfHellLayerTabPos[1])
        time.sleep(self.waitTime)
        pyautogui.click(fireOfHellInstancePos[0], fireOfHellInstancePos[1])
        self.logger.info("进入[炎火之狱]")


    # 选择元素塔
    def selectElementTower(self):
        pyautogui.click(elementTowerTabPos[0], elementTowerTabPos[1])
        self.logger.info("选择[元素塔的TAB]")


    # 放弃
    def clickGiveUpRebornBtn(self):
        self.check_window_handler()
        pyautogui.click(giveUpRebornBtn[0], giveUpRebornBtn[1])


    # 完成Task
    def completeUnionTask(self):
        self.check_window_handler()
        pyautogui.click(completeUnionTaskTabPos[0], completeUnionTaskTabPos[1])


    # 关闭窗口
    def closeWin(self):
        self.check_window_handler()
        pyautogui.click(closeBtnPos[0], closeBtnPos[1])
        self.logger.info("关闭对话窗")


    # 挑战下一关旁边的确认按钮
    def click_arena_comfirm_btn(self):
        # macos的自带25px的边
        # macos自带图片查看器的边框为（80 - 25）px
        # 微信小程序百炼英雄的白条win的宽为（125 - 80）px
        # 图片查看模式下，下一关按钮的定位为 Point(x=316, y=746)
        # 由此可知: 他的坐标为 winX + 316, winY - (80 - 25) - 25 + 746
        self.check_window_handler()
        winX, winY, winWidth, winHeight = self.get_win_info()
        pyautogui.click(int(winX + 153), (winY - (80 - 25) - 25 + 746))


    # 打道回府
    def back2Town(self):
        self.check_window_handler()
        pyautogui.click(back2TownPos[0], back2TownPos[1])
        time.sleep(self.waitTime)
        pyautogui.click(yesBtnPos[0], yesBtnPos[1])
        self.logger.info(f"打道回府！")
        self.virtual_map.reposition()


    # 把窗口移动到（0，0）
    def move2LeftTop(self, waitFn, isContainAds):
        win = self.get_specific_window_info()

        self.wechat.wake_up()
        self.wechat.wake_up_game()
        time.sleep(.3)
        # 没启动游戏
        if(win == None): 
            if(waitFn): waitFn(isContainAds)

        win = self.get_specific_window_info()
        bounds = win.get('kCGWindowBounds', {})  # 窗口边界
        x = int(bounds.get('X', 0))  # X 坐标
        y = int(bounds.get('Y', 0))  # Y 坐标

        pyautogui.moveTo(x + 10, y + 10, .1)
        pyautogui.dragTo(10, 30, duration=.1, button='left')
        time.sleep(.3)

        if(isContainAds):
            self.clearAds(5)


    # 清除广告
    def clearAds(self, times):
        self.logger.info("关闭广告。")
        window = self.get_specific_window_info()
        if(window == None): raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
        window_bounds = window.get('kCGWindowBounds', {})
        winWidth, winHeight = window_bounds.get('Width', 0), window_bounds.get('Height', 0)
        winX, winY = window_bounds.get('X', 0), window_bounds.get('Y', 0)
        for _ in range(int(times)):
            pyautogui.click(winX + winWidth - 10, winY + winHeight - 10)
            time.sleep(.3)


    # 关闭游戏
    def closeGame(self):
        window = self.get_specific_window_info()
        if(window == None): raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
        window_bounds = window.get('kCGWindowBounds', {})
        winX, winY = window_bounds.get('X', 0), window_bounds.get('Y', 0)
        winWidth, _ = window_bounds.get('Width', 0), window_bounds.get('Height', 0)
        pyautogui.click(winX + winWidth - 30, winY + 20)
        self.logger.info("关闭游戏")
        time.sleep(.1)
        

    # 关闭游戏无视报错的那种
    def closeGameWithoutException(self):
        window = None
        # 获取所有在屏幕上的窗口信息
        options = Quartz.kCGWindowListOptionOnScreenOnly
        window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)
        # 查找指定窗口
        for _window in window_list:
            window_name = _window.get('kCGWindowName', '')
            if self.app_name in window_name:
                window = _window  # 返回指定窗口的信息
        if(window == None): return
        window_bounds = window.get('kCGWindowBounds', {})
        winX, winY = window_bounds.get('X', 0), window_bounds.get('Y', 0)
        winWidth, _ = window_bounds.get('Width', 0), window_bounds.get('Height', 0)
        pyautogui.click(winX + winWidth - 30, winY + 20)
        self.logger.info("关闭游戏")
        time.sleep(.1)
    
