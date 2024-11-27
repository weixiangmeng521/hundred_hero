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


# 地狱火副本
hellInstanceTabPos = [337, 750]
fireOfHellLayerTabPos = [121, 330]
fireOfHellInstancePos = [300, 530]

# 任务列表
taskListBtnPos = [445, 385]
unionTaskTabPos = [390 , 840]
completeUnionTaskTabPos = [370 , 385]

# 关闭窗口的btn
closeBtnPos = [85, 840]

# 放弃复活
giveUpRebornBtn = [315, 740]

app_name = "百炼英雄"



# 选择关卡
class ChallengeSelect():
    waitTime = .3

    # 获取窗口信息
    def get_specific_window_info(self):
        # 获取所有在屏幕上的窗口信息
        options = Quartz.kCGWindowListOptionOnScreenOnly
        window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)
        
        # 查找指定窗口
        for window in window_list:
            window_name = window.get('kCGWindowName', '')
            if app_name in window_name:
                return window  # 返回指定窗口的信息
        return None
    

    # 点击最近的绿色冒泡
    def clickGreenPop(self):
        vt = VisualTrack()
        _list = vt.get_targets_list((0x66,0xc1,0x52), 20, 20)
        point = vt.get_shortest_point(_list)
        if(len(point) == 0):
            return
        pyautogui.click(point[0], point[1] + 20)

    # 刷经验
    def selectExpeirenceInstance(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")
        self.clickGreenPop()
        # print(f"副本选择被点击")
        time.sleep(self.waitTime)
        pyautogui.click(blackRockBtnPos[0], blackRockBtnPos[1])
        # print(f"黑石堡垒被点击")
        time.sleep(self.waitTime)
        pyautogui.click(centerHallBtnPos[0], centerHallBtnPos[1])
        # print(f"中央走廊被点击")


    # 刷木头
    def selectWoodInstance(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")
        self.clickGreenPop()
        # print(f"副本选择被点击")
        time.sleep(self.waitTime)
        pyautogui.click(forestMapBtnPos[0], forestMapBtnPos[1])
        # print(f"污染之森点击")
        time.sleep(self.waitTime)
        pyautogui.click(decayedSwampBtnPos[0], decayedSwampBtnPos[1])
        # print(f"污染之森点击")


    # 污染之林的污染前哨
    def selectPollutionOutpost(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")
        self.clickGreenPop()
        time.sleep(self.waitTime)
        pyautogui.click(forestMapBtnPos[0], forestMapBtnPos[1])        
        time.sleep(self.waitTime)
        pyautogui.click(pollutionOutpostBtnPos[0], pollutionOutpostBtnPos[1])
        
    
    # [打金]刷前哨平原的副本
    def selectFrontFlatland(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")
        self.clickGreenPop()
        time.sleep(self.waitTime)
        pyautogui.click(flatlandBtnPos[0], flatlandBtnPos[1])        
        time.sleep(self.waitTime)
        pyautogui.click(chorchHillBtnPos[0], chorchHillBtnPos[1])


    # [打金]贫瘠营地
    def selectPoorCamp(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")
        self.clickGreenPop()
        time.sleep(self.waitTime)
        pyautogui.click(poorZoneBtnPos[0], poorZoneBtnPos[1])        
        time.sleep(self.waitTime)
        pyautogui.click(poorCampPosBtnPos[0], poorCampPosBtnPos[1])


    # [打金]双峰峡谷
    def selectTwoPeak(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")
        self.clickGreenPop()
        time.sleep(self.waitTime)
        pyautogui.click(poorZoneBtnPos[0], poorZoneBtnPos[1])        
        time.sleep(self.waitTime)
        pyautogui.click(twoPeakPosBtnPos[0], twoPeakPosBtnPos[1])

    


    # 刷寒风营地的副本
    def selectColdWindCamp(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")
        self.clickGreenPop()
        time.sleep(self.waitTime)
        pyautogui.click(forestMapBtnPos[0], forestMapBtnPos[1])        
        time.sleep(self.waitTime)
        pyautogui.click(coldWindCampBtnPos[0], coldWindCampBtnPos[1])


    # 刷水晶
    def selectDiamondInstance(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")
        self.clickGreenPop()
        # print(f"副本选择被点击")
        time.sleep(self.waitTime)
        pyautogui.click(snwoMapBtnPos[0], snwoMapBtnPos[1])
        # print(f"严寒地带点击")
        time.sleep(self.waitTime)
        pyautogui.click(snowBtnPos[0], snowBtnPos[1])
        # print(f"北风营地点击")


    # 选择雪原副本
    def selectSnowInstance(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")
        self.clickGreenPop()
        # print(f"副本选择被点击")
        time.sleep(self.waitTime)
        pyautogui.click(snwoMapBtnPos[0], snwoMapBtnPos[1])
        # print(f"严寒地带点击")
        time.sleep(self.waitTime)
        pyautogui.click(snowRingBtnPos[0], snowRingBtnPos[1])
        # print(f"北风营地点击")

    
    # 查看任务栏的任务
    def openTaskList(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")
        pyautogui.click(taskListBtnPos[0], taskListBtnPos[1])
        time.sleep(self.waitTime)
        pyautogui.click(unionTaskTabPos[0], unionTaskTabPos[1])


    # 选择炎火之狱副本
    def selectHellOfHell(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")
        self.clickGreenPop()
        time.sleep(self.waitTime)
        pyautogui.click(hellInstanceTabPos[0], hellInstanceTabPos[1])
        time.sleep(self.waitTime)
        pyautogui.click(fireOfHellLayerTabPos[0], fireOfHellLayerTabPos[1])
        time.sleep(self.waitTime)
        pyautogui.click(fireOfHellInstancePos[0], fireOfHellInstancePos[1])


    # 选择炎火之狱副本
    def selectHellOfHell(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")
        self.clickGreenPop()
        time.sleep(self.waitTime)
        pyautogui.click(hellInstanceTabPos[0], hellInstanceTabPos[1])
        time.sleep(self.waitTime)
        pyautogui.click(fireOfHellLayerTabPos[0], fireOfHellLayerTabPos[1])
        time.sleep(self.waitTime)
        pyautogui.click(fireOfHellInstancePos[0], fireOfHellInstancePos[1])


    # 放弃
    def clickGiveUpRebornBtn(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")
        pyautogui.click(giveUpRebornBtn[0], giveUpRebornBtn[1])


    # 完成Task
    def completeUnionTask(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")
        pyautogui.click(completeUnionTaskTabPos[0], completeUnionTaskTabPos[1])


    # 关闭窗口
    def closeWin(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")
        pyautogui.click(closeBtnPos[0], closeBtnPos[1])


    # 打道回府
    def back2Town(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")
        pyautogui.click(back2TownPos[0], back2TownPos[1])
        time.sleep(self.waitTime)
        pyautogui.click(yesBtnPos[0], yesBtnPos[1])
        print(f"打道回府！")


    # 把窗口移动到（0，0）
    def move2LeftTop(self, waitFn, isContainAds):
        win = self.get_specific_window_info()
        wechat = ControllWechat()

        wechat.wake_up()
        wechat.wake_up_game()
        time.sleep(.3)
        # 没启动游戏
        if(win == None): 
            if(waitFn): waitFn(isContainAds)

        win = self.get_specific_window_info()
        bounds = win.get('kCGWindowBounds', {})  # 窗口边界
        x = int(bounds.get('X', 0))  # X 坐标
        y = int(bounds.get('Y', 0))  # Y 坐标

        print(f"postion:({x},{y})")
        pyautogui.moveTo(x + 10, y + 10, .1)
        pyautogui.dragTo(10, 30, duration=.1, button='left')
        time.sleep(.3)

        if(isContainAds):
            self.clearAds(5)


    # 清除广告
    def clearAds(self, times):
        print("关闭广告。")
        window = self.get_specific_window_info()
        if(window == None): raise Exception('Err', f"{app_name}`s window is not found.")
        window_bounds = window.get('kCGWindowBounds', {})
        winWidth, winHeight = window_bounds.get('Width', 0), window_bounds.get('Height', 0)
        for _ in range(int(times)):
            pyautogui.click(winWidth - 10, winHeight + 10)
            time.sleep(.3)


    # 关闭游戏
    def closeGame(self):
        window = self.get_specific_window_info()
        if(window == None): raise Exception('Err', f"{app_name}`s window is not found.")
        window_bounds = window.get('kCGWindowBounds', {})
        winWidth, _ = window_bounds.get('Width', 0), window_bounds.get('Height', 0)
        pyautogui.click(winWidth - 30, 40)
        print("关闭游戏")
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
            if app_name in window_name:
                window = _window  # 返回指定窗口的信息
        if(window == None): return
        window_bounds = window.get('kCGWindowBounds', {})
        winWidth, _ = window_bounds.get('Width', 0), window_bounds.get('Height', 0)
        pyautogui.click(winWidth - 30, 40)
        print("关闭游戏")
        time.sleep(.1)
    




# 控制类
class MoveControll():
    mouse = Controller()

    def __init__(self):
        curX, curY = pyautogui.position()
        self.curPos = [curX, curY]
        self.xPos = cPos[0]
        self.yPos = cPos[1]
        # self.get_window_info()


    # 获取窗口信息
    def get_specific_window_info(self):
        # 获取所有在屏幕上的窗口信息
        options = Quartz.kCGWindowListOptionOnScreenOnly
        window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)

        # 查找指定窗口
        for window in window_list:
            window_name = window.get('kCGWindowName', '')
            if app_name in window_name:
                return window  # 返回指定窗口的信息
        return None


    # 计算两点距离
    def get_point_distance(self, x1, y1, x2, y2):
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance


    def recover(self):
        pyautogui.moveTo(self.curPos[0], self.curPos[1])
        print(f"x = {self.curPos[0]}, y = {self.curPos[1]}")


    def move_before_check(self):
        if(self.get_specific_window_info() == None): raise Exception('Err', f"{app_name}`s window is not found.")


    def get_window_info(self):
        self.move_before_check()
        pyautogui.move(self.xPos, self.yPos)
        # pyautogui.click(self.xPos, self.yPos)


    def move_up(self, sec):
        self.move_before_check()
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos), int(self.yPos) - 50, sec, button='left')


    def move_top(self, sec):
        self.move_before_check()
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos), int(self.yPos) - 50, sec, button='left')


    def move_top_fast(self, sec):
        self.move_before_check()
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos), int(self.yPos) - 150, sec, button='left')


    def move_down(self, sec):
        self.move_before_check()
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos), int(self.yPos) + 50, sec, button='left')


    def move_down_fast(self, sec):
        self.move_before_check()
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos), int(self.yPos) + 150, sec, button='left')


    def move_left(self, sec):
        self.move_before_check()
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos) - 50, int(self.yPos), sec, button='left')

    def move_right(self, sec):
        self.move_before_check()        
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos) + 50, int(self.yPos), sec, button='left')


    def move_left_down(self, sec):
        self.move_before_check()        
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos) - 78, int(self.yPos + 50), sec, button='left')


    def move_left_top(self, sec):
        self.move_before_check()        
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos) - 78, int(self.yPos - 50), sec, button='left')


    def move_right_top(self, sec):
        self.move_before_check()        
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos) + 78, int(self.yPos - 50), sec, button='left')

    def move_right_down(self, sec):
        self.move_before_check()        
        pyautogui.moveTo(self.xPos, self.yPos)
        pyautogui.dragTo(int(self.xPos) + 78, int(self.yPos + 50), sec, button='left')


    def move(self, x, y, tX, tY):
        self.move_before_check()       
        distance = self.get_point_distance(x, y, tX, tY) 
        # 计算移动时间
        speed = 50 / 0.27      
        # 移动所需要的时间

        dx = cPos[0] - x
        dy = cPos[1] - y
        dX = tX + dx
        dY = tY + dy

        sec = distance / speed
        pyautogui.moveTo(cPos[0], cPos[1])
        pyautogui.dragTo(int(dX), int(dY), sec, button='left')



    def pointer_move_to(self, x, y):
        self.move_before_check()
        pyautogui.moveTo(int(x), int(y))




# 视觉跟踪
class VisualTrack:
    
    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = .5
        self.color = (255, 0, 0)  # 绿色
        self.thickness = 1
    

    # 获取窗口信息
    def get_specific_window_info(self):
        # 获取所有在屏幕上的窗口信息
        options = Quartz.kCGWindowListOptionOnScreenOnly
        window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)
        # 查找指定窗口
        for window in window_list:
            window_name = window.get('kCGWindowName', '')
            if app_name in window_name:
                return window  # 返回指定窗口的信息
        return None
        
    
    # 获得窗口的信息
    def get_win_info(self):
        window = self.get_specific_window_info()
        if(window == None): raise Exception('Err', f"{self.app_name}`s window is not found.")
        window_bounds = window.get('kCGWindowBounds', {})
        winX, winY = window_bounds.get('X', 0), window_bounds.get('Y', 0)
        winWidth, winHeight = window_bounds.get('Width', 0), window_bounds.get('Height', 0)
        return winX, winY, winWidth, winHeight


    # display analysis
    # target_color = (121, 236, 239)
    # lower_bound: number
    # upper_bound: number
    def find_position(self, target_color, lower_bound, upper_bound):
        # Get window region
        winX, winY, winWidth, winHeight = self.get_win_info()
        screenshot = pyautogui.screenshot(region=(int(winX), int(winY), int(winWidth), int(winHeight)))
        mat_image = np.array(screenshot)

        # Remove advertisements
        cv2.rectangle(mat_image, (340, 110), (460, 170), (0, 0, 0), -1)

        # Convert to HSV color space
        hsv_image = cv2.cvtColor(mat_image, cv2.COLOR_BGR2HSV)

        # Convert target BGR color to HSV
        target_hsv = cv2.cvtColor(np.uint8([[target_color]]), cv2.COLOR_BGR2HSV)[0][0]

        # Define HSV bounds using tolerance
        lower_bound = np.array([
            max(0, target_hsv[0] - lower_bound),  # Hue lower bound
            max(0, target_hsv[1] - lower_bound),  # Saturation lower bound
            max(0, target_hsv[2] - lower_bound)   # Value lower bound
        ], dtype=np.uint8)

        upper_bound = np.array([
            min(179, target_hsv[0] + upper_bound),  # Hue upper bound
            min(255, target_hsv[1] + upper_bound),  # Saturation upper bound
            min(255, target_hsv[2] + upper_bound)   # Value upper bound
        ], dtype=np.uint8)

        # Mask the image to isolate the target color
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
        result = cv2.bitwise_and(mat_image, mat_image, mask=mask)

        # Convert to grayscale for binary thresholding
        gray_img = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)

        # Dilate the binary image to merge nearby features
        kernel = np.ones((9, 9), np.uint8)
        dilated_image = cv2.dilate(binary_image, kernel, iterations=1)

        # Find contours in the binary image
        contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate the center of the window
        height, width = binary_image.shape
        window_center = (width // 2, height // 2)

        # Default values for the target centroid
        target_x, target_y = window_center

        if contours:
            # Get the largest contour by area
            largest_contour = max(contours, key=cv2.contourArea)

            # Calculate moments of the largest contour
            moments = cv2.moments(largest_contour)
            if moments['m00'] != 0:  # Avoid division by zero
                target_x = int(moments['m10'] / moments['m00'])
                target_y = int(moments['m01'] / moments['m00'])

        return window_center[0], window_center[1], target_x, target_y


    # 计算两点距离
    def get_point_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


    # 获得目标对象的列表
    def get_targets_list(self, target_color, lower_bound, upper_bound):
        DEBUG = False

        winX, winY, winWidth, winHeight = self.get_win_info()
        # frame draw
        screenshot = pyautogui.screenshot(region=(int(winX), int(winY), int(winWidth), int(winHeight)))
        mat_image = np.array(screenshot)
        # 创建新的空白图像   
        mat_image = mat_image.copy()  

        # # 转化为rgb 
        rgb_img = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2RGB)

        # 清除广告干扰
        cv2.rectangle(mat_image, (340, 110), (460,170), (0, 0, 0), -1)

        # 转变格式
        hsv_image = cv2.cvtColor(mat_image, cv2.COLOR_BGR2HSV)

        target_hsv = cv2.cvtColor(np.uint8([[target_color]]), cv2.COLOR_BGR2HSV)[0][0]
        # Define the color range to extract the color (a tolerance can be added)
        lower_bound = np.array([target_hsv[0], target_hsv[1], target_hsv[2] - lower_bound])  # lower bound (with some tolerance)
        upper_bound = np.array([target_hsv[0], target_hsv[1], target_hsv[2] + upper_bound])  # upper bound

        # 取色
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
        result = cv2.bitwise_and(mat_image, mat_image, mask=mask)

        # 膨胀
        _, binary_image = cv2.threshold(result, 127, 255, cv2.THRESH_BINARY)
        kernel = np.ones((60, 60), np.uint8)
        dilated_result = cv2.dilate(binary_image, kernel, iterations=1)

        gray_img = cv2.cvtColor(dilated_result, cv2.COLOR_RGB2GRAY)
        _, binary_image = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)

        # 检测图像中的轮廓
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        res_list = list({})
        center = self.get_center_point()
        for cnt in contours:
            M = cv2.moments(cnt)
            # 计算质心（中心点）的坐标
            if M['m00'] != 0:  # 确保区域面积非零，防止除零错误
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
            else:
                # 如果区域面积为零，则默认中心为 (0, 0)
                cX, cY = 0, 0
            res_list.append(np.array([cX, cY]))
            if(DEBUG): 
                cv2.circle(rgb_img, (cX, cY), 5, (255, 0, 0), -1)
                cv2.line(rgb_img, (cX, cY), center, (255, 0, 0), 5)
                distance = self.get_point_distance(center[0], center[1], cX, cY)
                cv2.putText(rgb_img, f"(D:{int(distance)})", (cX + 20, cY), self.font, self.font_scale, self.color, self.thickness, cv2.LINE_AA)

        if(DEBUG): 
            cv2.circle(rgb_img, center, 5, (255, 0, 0), -1)
            bgr_image = cv2.cvtColor(rgb_img, cv2.COLOR_RGBA2BGR)
            cv2.imshow("test", bgr_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return res_list


    # 获取最短目标点
    def get_shortest_point(self, point_list):
        center = self.get_center_point()
        shortest = math.inf
        point = {}
        for el in point_list:
            distance = self.get_point_distance(center[0], center[1], el[0], el[1])
            if(int(distance) < shortest):
                shortest = distance
                point = el
        return point



    # 获取游戏的中心点
    def get_center_point(self):
        winX, winY, winWidth, winHeight = self.get_win_info()
        return (int(winX + winWidth // 2), int(winY + winHeight // 2))



    # mark in frame
    def mark_in_frame(self, target_color, lower_bound, upper_bound):
        winX, winY, winWidth, winHeight = self.get_win_info()
        # frame draw
        screenshot = pyautogui.screenshot(region=(int(winX), int(winY), int(winWidth), int(winHeight)))
        mat_image = np.array(screenshot)
        # 创建新的空白图像   
        mat_image = mat_image.copy()  

        # # 转化为rgb 
        rgb_img = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2RGB)

        x, y, cX, cY = self.find_position(target_color, lower_bound, upper_bound)

        # 设置红色的RGB值
        red_color = (255, 0, 0)
        # 横向线
        rgb_img[y, :] = red_color  # 修改中心行的所有像素为红色
        rgb_img[:, x] = red_color  # 修改中心列的所有像素为红色
        
        # 画目标点
        cv2.circle(rgb_img, (cX, cY), 5, (255, 0, 0), -1)

        # 建立目标连接
        cv2.line(rgb_img, (cX, cY), (x, y), (255, 0, 0), 1)


        print(f"图像大小 {winWidth} x {winHeight}; 中心点:({x},{y})")
        print(f"目标点:({cX},{cY})")
        # return (center[1], center[0], cX, cY)
        bgr_image = cv2.cvtColor(rgb_img, cv2.COLOR_RGBA2BGR)
        return bgr_image


    # play frame
    def play_frame(self, target_color, lower_bound, upper_bound):
        img_win_name = "ImageAnalysis"  

        window = self.get_specific_window_info()
        if(window == None): raise Exception('Err', f"{app_name}`s window is not found.")
        window_bounds = window.get('kCGWindowBounds', {})
        winX, winY = window_bounds.get('X', 0), window_bounds.get('Y', 0)
        winWidth, _ = window_bounds.get('Width', 0), window_bounds.get('Height', 0)

        while True:
            frame = self.mark_in_frame(target_color, lower_bound, upper_bound)
            cv2.imshow(img_win_name, frame)
            cv2.moveWindow(img_win_name, int(winX + winWidth), - 100)        
            
            print(winX, winY)

            # 设置刷新间隔，并检测按键退出
            key = cv2.waitKey(30)
            if key == ord('q') or key == 27:  # 27 是 ESC 的 ASCII 值
                cv2.destroyAllWindows()
                break




# # display analysis
# def find_position(winX, winY, winWidth, winHeight):    
#     # frame draw
#     screenshot = pyautogui.screenshot(region=(int(winX), int(winY), int(winWidth), int(winHeight)))
#     mat_image = np.array(screenshot)
#     # 创建新的空白图像   
#     mat_image = mat_image.copy()  


#     # 清除广告干扰
#     cv2.rectangle(mat_image, (340, 110), (460,170), (0, 0, 0), -1)

#     # 转变格式
#     hsv_image = cv2.cvtColor(mat_image, cv2.COLOR_BGR2HSV)

#     # 读取关键的颜色
#     # target_color = (102, 200, 207)

#     target_color = (121, 236, 239)

#     target_hsv = cv2.cvtColor(np.uint8([[target_color]]), cv2.COLOR_BGR2HSV)[0][0]
#     # Define the color range to extract the color (a tolerance can be added)
#     lower_bound = np.array([target_hsv[0], target_hsv[1], target_hsv[2] - 15])  # lower bound (with some tolerance)
#     upper_bound = np.array([target_hsv[0], target_hsv[1], target_hsv[2] + 15])  # upper bound

#     # 取色
#     mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
#     result = cv2.bitwise_and(mat_image, mat_image, mask=mask)

#     # 膨胀
#     _, binary_image = cv2.threshold(result, 127, 255, cv2.THRESH_BINARY)
#     kernel = np.ones((60, 60), np.uint8)
#     dilated_result = cv2.dilate(binary_image, kernel, iterations=1)

#     gray_img = cv2.cvtColor(dilated_result, cv2.COLOR_RGB2GRAY)
#     _, binary_image = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)

#     # 检测图像中的轮廓
#     contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


#     # 假设我们只关注第一个轮廓（即 contours[0]）
#     if(len(contours) >= 1):
#         cnt = contours[0]

#     # 计算轮廓的几何矩
#     try:
#         M = cv2.moments(cnt)
#         # 计算质心（中心点）的坐标
#         if M['m00'] != 0:  # 确保区域面积非零，防止除零错误
#             cX = int(M['m10'] / M['m00'])
#             cY = int(M['m01'] / M['m00'])
#         else:
#             # 如果区域面积为零，则默认中心为 (0, 0)
#             cX, cY = 0, 0
#     except Exception as e:
#         height, width, _ = dilated_result.shape
#         cX = width // 2
#         cY = height // 2
#     # 画十字架
#     height, width, _ = dilated_result.shape
#     center = (width // 2, height // 2)    

#     return (center[0], center[1], cX, cY) 


# # mark in frame
# def mark_in_frame(winX, winY, winWidth, winHeight):
#     # frame draw
#     screenshot = pyautogui.screenshot(region=(int(winX), int(winY), int(winWidth), int(winHeight)))
#     mat_image = np.array(screenshot)
#     # 创建新的空白图像   
#     mat_image = mat_image.copy()  

#     # # 转化为rgb 
#     rgb_img = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2RGB)

#     x, y, cX, cY = find_position(winX, winY, winWidth, winHeight)

#     # 设置红色的RGB值
#     red_color = (255, 0, 0)
#     # 横向线
#     rgb_img[y, :] = red_color  # 修改中心行的所有像素为红色
#     rgb_img[:, x] = red_color  # 修改中心列的所有像素为红色
    
#     # 画目标点
#     cv2.circle(rgb_img, (cX, cY), 5, (255, 0, 0), -1)

#     # 建立目标连接
#     cv2.line(rgb_img, (cX, cY), (x, y), (255, 0, 0), 1)


#     print(f"图像大小 {winWidth} x {winHeight}; 中心点:({x},{y})")
#     print(f"目标点:({cX},{cY})")

#     # return (center[1], center[0], cX, cY)

#     bgr_image = cv2.cvtColor(rgb_img, cv2.COLOR_RGBA2BGR)
#     return bgr_image




# # play frame
# def play_frame():
#     img_win_name = "ImageAnalysis"  

#     window = get_specific_window_info(app_name)
#     if(window == None): raise Exception('Err', f"{app_name}`s window is not found.")
#     window_bounds = window.get('kCGWindowBounds', {})
#     winX, winY = window_bounds.get('X', 0), window_bounds.get('Y', 0)
#     winWidth, winHeight = window_bounds.get('Width', 0), window_bounds.get('Height', 0)

#     while True:
#         frame = mark_in_frame(winX, winY, winWidth, winHeight)
#         cv2.imshow(img_win_name, frame)
#         cv2.moveWindow(img_win_name, int(winX + winWidth), - 100)        
        
#         print(winX, winY)

#         # 设置刷新间隔，并检测按键退出
#         key = cv2.waitKey(30)
#         if key == ord('q') or key == 27:  # 27 是 ESC 的 ASCII 值
#             cv2.destroyAllWindows()
#             break
