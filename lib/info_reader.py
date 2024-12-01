import time
import pyautogui
import Quartz
import pytesseract
import cv2
import numpy as np
from lib.challenge_select import ChallengeSelect
from lib.handler import correct_text_handler
from lib.logger import init_logger


# 读取屏幕信息
class InfoReader:

    def __init__(self, config):
        self.config = config
        self.app_name = config["APP"]["Name"]
        self.img_win_name = "ImageAnalysis"   
        self.logger = init_logger(config)
        self.cs = ChallengeSelect(config)


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


    # 获得窗口的信息
    def get_win_info(self):
        window = self.get_specific_window_info()
        if(window == None): raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
        window_bounds = window.get('kCGWindowBounds', {})
        winX, winY = window_bounds.get('X', 0), window_bounds.get('Y', 0)
        winWidth, winHeight = window_bounds.get('Width', 0), window_bounds.get('Height', 0)
        return winX, winY, winWidth, winHeight


    # 打印字代颜色
    def print_color(self, text, r, g, b):
        print(f"\033[48;2;{r};{g};{b}m{text}\033[0m")


    # 输出图片每个色块
    def print_img(self, mat_image):
        for row in range(mat_image.shape[0]):  # 遍历行
            for col in range(mat_image.shape[1]):  # 遍历列
                b, g, r = mat_image[row, col]  # 获取像素的 BGR 值
                self.print_color(f"{r},{g},{b}", r, g, b)

    # 通过rgb的方式输出图片的色块
    def print_img_by_rgb(self, mat_image):
        for row in range(mat_image.shape[0]):  # 遍历行
            for col in range(mat_image.shape[1]):  # 遍历列
                r, g, b = mat_image[row, col]  # 获取像素的 BGR 值
                self.print_color(f"{r},{g},{b}", r, g, b)


    # 查看木头和蓝矿是否满了
    def is_full_from_img(self, meatPosList):
        # 读取指定位置
        screenshot = pyautogui.screenshot(region=(meatPosList))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)

        # 定义目标颜色并转换为 BGR 格式
        target_rgb = (253, 219, 84)   # RGB 格式
        target_bgr = target_rgb[::-1]      # 转换为 BGR 格式

        # 定义颜色的容差上下界，并转换为 uint8 类型
        lower_bound = np.array(target_bgr) - 20
        upper_bound = np.array(target_bgr) + 20

        # 创建掩码，找到接近目标颜色的区域
        mask = cv2.inRange(mat_image, lower_bound, upper_bound)

        # 检查掩码中是否包含目标颜色
        return cv2.countNonZero(mask) > 0



    # 读截图
    # 直接判断是不是黄色，黄色，就是打满了的情况
    def read_screen(self):
        window = self.get_specific_window_info()
        if(window == None):
            raise RuntimeError('Err', f"Window not found")
    
        meatPosList = (221, 113, 45, 13)
        isMeatFull = self.is_full_from_img(meatPosList)

        blueMinePosList = (301, 113, 45, 13)
        isBlueMineFull = self.is_full_from_img(blueMinePosList)

        return isMeatFull, isBlueMineFull


    # 判断工会任务是否完成, false的情况下是完成了，true的情况下是没完成
    def is_task_complete(self, screenshot_handler):
        self.cs.openTaskList()
        time.sleep(.6)

        btnPos = (320, 365, 90, 37)
        # 读取指定位置
        screenshot = pyautogui.screenshot(region=(btnPos))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)
        
        result = self.read_task_list()
        screenshot_handler(result)

        # 定义目标颜色并转换为 BGR 格式
        target_rgb = (225, 204, 77)   # RGB 格式
        target_bgr = target_rgb[::-1]      # 转换为 BGR 格式

        # 定义颜色的容差上下界，并转换为 uint8 类型
        lower_bound = np.array(target_bgr) - 20
        upper_bound = np.array(target_bgr) + 20

        # 创建掩码，找到接近目标颜色的区域
        mask = cv2.inRange(mat_image, lower_bound, upper_bound)

        # 检查掩码中是否包含目标颜色
        return cv2.countNonZero(mask) == 0



    # 读取屏幕中的任务列表
    def read_task_list(self):
        winX, winY, winWidth, winHeight = self.get_win_info()
        # 读取指定位置
        screenshot = pyautogui.screenshot(region=(
            int(winX + 50), 
            int(winY + 325), 
            int(winWidth - 100), 
            int(winHeight - 650)
        ))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)
        task_img_heigt = int((winHeight - 650 - 15) / 3)
        task_img_width = int(winWidth - 100 - 100)
        gutter = 30
        # start_y:end_y, start_x:end_x
        task_1_img = mat_image[0:task_img_heigt - 5 - gutter - 3, 130:task_img_width]
        task_2_img = mat_image[task_img_heigt + 5 + 3:task_img_heigt * 2 - gutter, 130:task_img_width]
        task_3_img = mat_image[task_img_heigt * 2 + 18:task_img_heigt * 3 + 3 - gutter, 130:task_img_width]

        return {
            self.recognize_chinese_text(task_1_img): self.is_task_complete_by_color_percent(task_1_img),
            self.recognize_chinese_text(task_2_img): self.is_task_complete_by_color_percent(task_2_img),
            self.recognize_chinese_text(task_3_img): self.is_task_complete_by_color_percent(task_3_img),
        }


    # 通过颜色占比来判断是否完成任务
    def is_task_complete_by_color_percent(self, bgr_img):
        complete_color = (218,224,230)
        rate = self.get_color_ratio(bgr_img, complete_color)
        return rate > 0.3


    # 读取中文
    def recognize_chinese_text(self, bgr_image):
        pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
        # 读取图片
        image = self.preprocess_img(bgr_image)
        # 转换为灰度图像
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 进行二值化，提升OCR识别效果
        binary_image = cv2.adaptiveThreshold(
            gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 2
        )
        blended_image = cv2.addWeighted(gray_image, 0.7, binary_image, 0.3, 0)

        # 识别中文文字，使用简体中文语言包 'chi_sim'
        text = pytesseract.image_to_string(blended_image, lang='chi_sim',  config='--psm 6')  # 使用简体中文语言包
        return correct_text_handler(text)
    

    # 提高图像
    def preprocess_img(self, bgr_image):
        # Laplacian 算子
        laplacian = cv2.Laplacian(bgr_image, cv2.CV_64F)
        # 将拉普拉斯算子的结果转换为 uint8
        laplacian = cv2.convertScaleAbs(laplacian)
        # 应用加权合成     
        sharp = cv2.addWeighted(bgr_image, 1.7, laplacian, -0.3, 0)
        return sharp


    # 保存task的图片
    # ! 目前用不到
    def save_task_sample_img(self, bgr_img, name):
        path = f"static/task_img_sample/{name}.png"
        cv2.imwrite(path, bgr_img)                


    # 获取颜色占比
    def get_color_ratio(self, bgr_img, target_rgb_color):
        tolerance = 10
        target_bgr_color = target_rgb_color[::-1]        
        # 目标颜色上下限
        lower_bound = np.array([max(0, c - tolerance) for c in target_bgr_color], dtype=np.uint8)
        upper_bound = np.array([min(255, c + tolerance) for c in target_bgr_color], dtype=np.uint8)
        # 创建颜色掩膜
        mask = cv2.inRange(bgr_img, lower_bound, upper_bound)
        # 计算目标颜色的像素数
        target_pixels = cv2.countNonZero(mask)
        # 检查图像是否为二维
        if len(bgr_img.shape) != 3:
            raise ValueError("输入图像必须为三通道 BGR 格式。")        
        # 计算图像总像素数
        total_pixels = bgr_img.shape[0] * bgr_img.shape[1]
        # 计算占比
        color_ratio = target_pixels / total_pixels
        return color_ratio


    # 关闭按钮点击
    def close_task_menu(self, is_click_complete = False):
        if(is_click_complete): 
            self.cs.completeUnionTask()
            self.logger.info(f"点击已完成工会副本按钮.")
        self.cs.closeWin()
        time.sleep(.3)


    # 是否有显示回城图标
    def is_show_back2town_btn(self):
        btnPos = (410, 785, 38, 27)
        # 读取指定位置
        screenshot = pyautogui.screenshot(region=(btnPos))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)

        # 定义目标颜色并转换为 BGR 格式
        target_rgb = (89,106,116)   # RGB 格式
        target_bgr = target_rgb[::-1]      # 转换为 BGR 格式

        # 定义颜色的容差上下界，并转换为 uint8 类型
        lower_bound = np.array(target_bgr) - 20
        upper_bound = np.array(target_bgr) + 20

        # 创建掩码，找到接近目标颜色的区域
        mask = cv2.inRange(mat_image, lower_bound, upper_bound)

        # 检查掩码中是否包含目标颜色
        return cv2.countNonZero(mask) > 0



    # 判读是不是死了
    def is_dead(self):
        btnPos = (100, 720, 100, 40)
        # 读取指定位置
        screenshot = pyautogui.screenshot(region=(btnPos))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)

        target_rgb = (225,204,77)   # RGB 格式
        target_bgr = target_rgb[::-1]      # 转换为 BGR 格式

        lower_bound = np.array(target_bgr)
        upper_bound = np.array(target_bgr)

        mask = cv2.inRange(mat_image, lower_bound, upper_bound)
        is_contain_reborn_btn = cv2.countNonZero(mask) > 0


        btnPos = (280, 720, 100, 40)
        # 读取指定位置
        screenshot = pyautogui.screenshot(region=(btnPos))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)

        target_rgb = (219,88,79)   # RGB 格式
        target_bgr = target_rgb[::-1]      # 转换为 BGR 格式

        lower_bound = np.array(target_bgr)
        upper_bound = np.array(target_bgr)

        mask = cv2.inRange(mat_image, lower_bound, upper_bound)
        is_contain_give_up_btn = cv2.countNonZero(mask) > 0

        return is_contain_reborn_btn and is_contain_give_up_btn


    # 等待传送完成
    def wait_tranported(self):
        start_time = time.time()  # 记录开始时间
        timeout = 60  # 超时时间，单位为秒

        while True:
            elapsed_time = time.time() - start_time  # 计算已过去的时间
            if elapsed_time > timeout:
                raise TimeoutError("加载超时: 未在一分钟内传送完成。")

            window = self.get_specific_window_info()
            if(window == None): 
                raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
            
            window_bounds = window.get('kCGWindowBounds', {})
            winX, winY = window_bounds.get('X', 0), window_bounds.get('Y', 0)
            winWidth, winHeight = window_bounds.get('Width', 0), window_bounds.get('Height', 0)
            # 获取目标定位
            flagPos = (
                int((winWidth // 2) - 100 + winX), 
                int((winHeight // 2) - 100 + winY), 
                200, 
                200,
            )
            screenshot = pyautogui.screenshot(region=(flagPos[0], flagPos[1], flagPos[2], flagPos[3]))
            mat_image = np.array(screenshot)
            mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)
            target_rgb = (102, 193, 82)   # RGB 格式

            # cv2.imshow("123", mat_image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            target_bgr = target_rgb[::-1]      # 转换为 BGR 格式
            tolerance = 0  # 容差
            lower_bound = np.array([max(0, c - tolerance) for c in target_bgr])
            upper_bound = np.array([min(255, c + tolerance) for c in target_bgr])
            mask = cv2.inRange(mat_image, lower_bound, upper_bound)
            if(cv2.countNonZero(mask) > 0):
                return



    # 是否游戏加载成功
    # TODO: 判断，登录失败，请重试
    def wait_game_loaded(self, is_contains_ads = False):
        self.logger.debug("等待游戏加载...")
        start_time = time.time()  # 记录开始时间
        timeout = 60  # 超时时间，单位为秒

        while True:
            elapsed_time = time.time() - start_time  # 计算已过去的时间
            if elapsed_time > timeout:
                raise TimeoutError("加载超时: 游戏未在1分钟内加载完成。")

            window = self.get_specific_window_info()
            if(window == None): 
                raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
            
            window_bounds = window.get('kCGWindowBounds', {})
            winX, winY = window_bounds.get('X', 0), window_bounds.get('Y', 0)
            # 获取目标定位
            flagPos = (int(287 + winX), int(53 + winY), 20, 20)
            screenshot = pyautogui.screenshot(region=(flagPos))
            mat_image = np.array(screenshot)
            mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)

            target_rgb = (246,199,77)   # RGB 格式
            if(is_contains_ads): 
                target_rgb = (88,81,21)

            target_bgr = target_rgb[::-1]      # 转换为 BGR 格式

            lower_bound = np.array(target_bgr)
            upper_bound = np.array(target_bgr)

            mask = cv2.inRange(mat_image, lower_bound, upper_bound)
            if(cv2.countNonZero(mask) > 0):
                self.logger.debug("加载完毕！")
                return
        
    
    # 纵向排列三张图片
    def v_stack_show(self, *imgs):  
        # 确保所有图片的宽度一致，否则调整为相同宽度
        widths = [img.shape[1] for img in imgs]
        max_width = max(widths)
        
        resized_imgs = [
            cv2.resize(img, (max_width, int(img.shape[0] * max_width / img.shape[1])))
            if img.shape[1] != max_width else img
            for img in imgs
        ]
        
        # 纵向堆叠图片
        stacked_img = np.vstack(resized_imgs)
        
        # 显示结果
        cv2.imshow("Vertical Stack", stacked_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
