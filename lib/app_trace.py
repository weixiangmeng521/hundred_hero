import datetime
import os
import time

import cv2
import numpy as np
import pyautogui

from lib.challenge_select import ChallengeSelect
from lib.logger import init_logger
from lib.message_service import MessageService

# 捕获error消息
class AppTrace:

    def __init__(self, config):
        self.config = config
        self.app_name = config["APP"]["Name"]
        self.logger = init_logger(config)
        self.pusher = MessageService(config)
        self.cs = ChallengeSelect(config)


    # 截屏，查看bug信息
    def screen_shot(self):
        if(self.config.getboolean('APP', 'EnableScreenShot') == False): 
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
        self.logger.debug(f"已经保存截图到:{path}")


    # 播放声音
    def play_sound(self, file_name):
        # 静音
        if(self.config.getboolean('APP', 'EnableSound') == False):
            return
        os.system(f"afplay /System/Library/Sounds/{file_name}")


    # 时间格式输出
    def record_time_formate(self, execution_time, earned):
        # 转换为分钟和秒
        minutes = int(execution_time // 60)
        seconds = execution_time % 60
        rate =  earned / execution_time
        hour_earned = rate * 60 * 60
        self.logger.debug(f"打金耗时: {minutes}m {seconds:.2f}s, 1h刷金预计: {hour_earned:.2f}")

    # 报告错误
    def report_error(self, info):
        self.play_sound("Glass.aiff")
        self.pusher.push(f"[{self.app_name}]运行异常, 请查看错误日志. err: {info}")
        self.screen_shot()
        self.cs.closeGameWithoutException()
        time.sleep(.3)        