
# 控制微信
import logging
import os
import time
import Quartz
import pyautogui
from lib.logger import init_logger



class ControllWechat():
    
    def __init__(self):
        self.app_name = "微信"
        self.game_name = "百炼英雄"
        self.logger = init_logger(self.game_name)

    # 获取窗口信息
    def get_specific_window_info(self, win_name):
        # 获取所有在屏幕上的窗口信息
        options = Quartz.kCGWindowListOptionOnScreenOnly
        window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)

        # 查找指定窗口
        for window in window_list:
            window_name = window.get('kCGWindowName', '')
            if win_name in window_name:
                return window  # 返回指定窗口的信息
        return None


    
    # 唤醒app
    def wake_up(self):
        window = self.get_specific_window_info(self.app_name)
        if(window == None): raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
        script = f"""
        tell application "WeChat"
            activate
        end tell
        """
        os.system(f"osascript -e '{script}'")


    # 启动游戏
    def wake_up_game(self):
        window = self.get_specific_window_info(self.app_name)
        if(window == None): raise RuntimeError('Err', f"{self.app_name}`s window is not found.")   

        game_window = self.get_specific_window_info(self.game_name)
        if(game_window): return

        window_bounds = window.get('kCGWindowBounds', {})
        winX, winY = window_bounds.get('X', 0), window_bounds.get('Y', 0)
        winHeight = window_bounds.get('Height', 0)
        pyautogui.click(winX + 25, winY + winHeight - 150)
        time.sleep(.3)
        pyautogui.click(winX + 25 + 85, winY + winHeight - 150 - 70)










    


