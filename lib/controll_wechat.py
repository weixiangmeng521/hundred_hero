
# 控制微信
from collections import defaultdict
import os
import shutil
import subprocess
import time
import Quartz
import cv2
import mss
import numpy as np
import pyautogui
from lib.logger import init_logger

instance = None
# 单例模式
def init_controll_wechat(config):
    global instance 
    if(instance):
        return instance
    instance = ControllWechat(config)
    return instance


# 控制微信的类
class ControllWechat:
    # 初始化
    def __init__(self, config):
        self.config = config
        self.app_name = config["APP"]["WechatName"]
        self.login_win_name = "登录"
        self.qr_folder = "QR_code"
        self.game_name = config["APP"]["Name"]
        self.logger = init_logger(config)
        # 0 => 未登录
        # 1 => 已登陆
        # -1 => 未知
        self.state = -1

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


    # 获取微信状态
    def get_state(self):
        return self.state


    # 获取所有活动窗口
    def get_active_window_title(self):
        script = '''
        tell application "System Events"
            set frontApp to name of first application process whose frontmost is true
            tell process frontApp
                set windowTitle to name of front window
            end tell
        end tell
        return windowTitle
        '''
        window_title = ""
        try:
            window_title = subprocess.check_output(
                ["osascript", "-e", script], text=True
            ).strip()
        except subprocess.CalledProcessError:
            self.logger.debug("无法获取活动窗口标题")
        return window_title


    # 判断当前的微信状态
    def get_wechat_state(self):
        active_window = self.get_active_window_title()
        # 获取失败的情况
        if(active_window == ""):
            self.logger.debug("获取的活动窗口为空")
            return
        # 如果是登录界面，就截图
        if(active_window == self.login_win_name):
            # window = self.get_specific_window_info("WeChat")
            window = self.get_specific_window_info(self.login_win_name)
            if(window == None): 
                raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
            
            # 判断是不是直接进入微信
            if self.is_directly_login(self.login_win_name):
                xBtn, yBtn = self.get_login_btn_pos(self.login_win_name)
                pyautogui.click(xBtn, yBtn)
                # 等待是否登录OK
                self.wait_enter()
                return 1

            # 是不是显示，你已退出微信
            if self.is_logout(self.login_win_name):
                xBtn, yBtn = self.get_confim_btn_pos()
                pyautogui.click(xBtn, yBtn)

            # 等待扫码
            self.wait_scan_QRcode()
            return 1
        return 1


    # 保证电脑不熄屏
    click_place = "right_bottom"
    def keep_alive(self):
        if(self.click_place == "right_bottom"):
            winX, winY, winWidth, winHeight = self.get_win_info(self.login_win_name)
            pyautogui.click(int(winX + winWidth - 10), int(winY + winHeight - 10))
            self.click_place = "left_bottom"
            return

        if(self.click_place == "left_bottom"):
            winX, winY, winWidth, winHeight = self.get_win_info(self.login_win_name)
            pyautogui.click(int(winX + 10), int(winY + winHeight - 10))
            self.click_place = "right_bottom"
            return 


    # 是不是显示，你已退出微信
    def is_logout(self, win_name):
        winX, winY, winWidth, winHeight = self.get_win_info(win_name)
        screenshot = pyautogui.screenshot(region=(
            int(winX + 65), 
            int(winY + 257), 
            int(170), 
            int(30)
        ))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)
        target_color = (220, 225, 233)
        return self.is_target_area(mat_image, target_color)


    # 获得确认按钮的位置
    def get_confim_btn_pos(self):
        winX, winY, winWidth, winHeight = self.get_win_info(self.login_win_name)
        return (
            int(winX + 65 + 170 // 2), 
            int(winY + 257 + 30 // 2), 
        )


    # 等待扫码
    def wait_scan_QRcode(self):
        while True:
            try: 
                win = self.get_specific_window_info(self.app_name)
                if(win): 
                    self.logger.debug("登录成功!")      
                    self.state = 1              
                    return
            except:
                self.logger.debug("等待进入主界面...")
                time.sleep(10)
                continue
            
            self.keep_alive()
            self.logger.debug("等待进入主界面...")
            self.screenshot_wechat(self.login_win_name)
            time.sleep(10)


    # 等待进入
    def wait_enter(self, wait_time = .6):         
        while True:
            try: 
                win = self.get_specific_window_info(self.app_name)
                if(win): 
                    self.logger.debug("登录成功!")
                    return
            except:
                self.logger.debug("等待进入主界面...")
                time.sleep(wait_time)
                continue
            # 正常执行
            self.logger.debug("等待进入主界面...")
            time.sleep(wait_time)


    # 是不是指定地方
    def is_target_area(self, bgr_img, target_rgb, threshold = 10):
        # 定义目标颜色并转换为 BGR 格式
        target_bgr = target_rgb[::-1]      # 转换为 BGR 格式

        # 定义颜色的容差上下界，并转换为 uint8 类型
        lower_bound = np.array(target_bgr) - threshold
        upper_bound = np.array(target_bgr) + threshold

        # 创建掩码，找到接近目标颜色的区域
        mask = cv2.inRange(bgr_img, lower_bound, upper_bound)

        # 检查掩码中是否包含目标颜色
        return cv2.countNonZero(mask) > 0


    # 清空文件夹
    def clear_qr_folder(self, folder_path):
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        os.makedirs(folder_path)
    

    # 保存图片
    def save_screenshot(self, mat_image, folder_path):
        name = "QRcode"
        file_path = os.path.join(folder_path, f"{name}.png")
        cv2.imwrite(file_path, mat_image)
        self.logger.debug(f"截图已保存到: {file_path}")


    # 截图微信
    def screenshot_wechat(self, win_name):
        winX, winY, winWidth, winHeight = self.get_win_info(win_name)

        with mss.mss() as sct:
            # Point(x=311, y=82)
            region = {
                "top": int(winY + 151),
                "left": int(winX + 65),
                "width": int(150),
                "height": int(150),
            }
            # 截取屏幕
            screenshot = sct.grab(region)
            mat_image = np.array(screenshot)

        qr_folder = self.qr_folder
        self.clear_qr_folder(qr_folder)
        self.save_screenshot(mat_image, qr_folder)


    # 是不是直接登录
    def is_directly_login(self, win_name):
        winX, winY, winWidth, winHeight = self.get_win_info(win_name)
        screenshot = pyautogui.screenshot(region=(
            int(winX + 65), 
            int(winY + 280), 
            int(170), 
            int(30)
        ))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)
        target_color = (87, 189, 106)
        return self.is_target_area(mat_image, target_color)


    # 获取登录按钮的中心点
    def get_login_btn_pos(self, win_name):
        winX, winY, winWidth, winHeight = self.get_win_info(self.login_win_name)
        return (
            int(winX + 65 + 170 // 2), 
            int(winY + 280 + 30 // 2), 
        )


    # 统计颜色出现的次数
    def count_colors(self, bgr_image):
        if bgr_image is None:
            print("图片加载失败！请检查路径。")
            return None

        # 将图片转换为 RGB 模式
        image_rgb = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

        # 统计颜色出现的次数
        color_counts = defaultdict(int)

        # 遍历每个像素点
        for row in image_rgb:
            for pixel in row:
                color_tuple = tuple(map(int, pixel))  # 转换为整数元组 (R, G, B)
                color_counts[color_tuple] += 1

        # 打印结果（示例前 10 种颜色）
        sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
        print("前 10 种最常见的颜色:")
        for color, count in sorted_colors[:10]:
            print(f"颜色 {color}: 出现 {count} 次")

        return color_counts


    # 显示图片
    def show_img(self, mat_image):
        cv2.imshow("test", mat_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    # 获得窗口的信息
    def get_win_info(self, win_name):
        window = self.get_specific_window_info(win_name)
        if(window == None): raise RuntimeError('Err', f"{win_name}`s window is not found.")
        window_bounds = window.get('kCGWindowBounds', {})
        winX, winY = window_bounds.get('X', 0), window_bounds.get('Y', 0)
        winWidth, winHeight = window_bounds.get('Width', 0), window_bounds.get('Height', 0)
        return winX, winY, winWidth, winHeight
    
    
    # 唤醒app
    def wake_up(self):
        self.state = 0
        script = f"""
        tell application "WeChat"
            activate
        end tell
        """
        os.system(f"osascript -e '{script}'")
        self.state = self.get_wechat_state()


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
        time.sleep(.3)










    


