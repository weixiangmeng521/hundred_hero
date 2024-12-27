from collections import defaultdict
import hashlib
import math
import re
import time
import uuid
import mss
import pyautogui
import Quartz
import pytesseract
import cv2
import numpy as np
from defined import IS_DALIY_CASE_FINISHED
from exception.game_status import GameStatusError
from lib.cache import get_cache_manager_instance
from lib.challenge_select import ChallengeSelect
from lib.handler import correct_text_handler
from lib.logger import init_logger
import matplotlib.pyplot as plt

# 读取屏幕信息
class InfoReader:

    def __init__(self, config):
        self.config = config
        self.app_name = config["APP"]["Name"]
        self.img_win_name = "ImageAnalysis"   
        self.logger = init_logger(config)
        self.cs = ChallengeSelect(config)
        self.cache = get_cache_manager_instance(config)
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


    # 获取钱的数量
    def get_coin_num(self, is_debug = False) -> int:
        winX, winY, winWidth, winHeight = self.get_win_info()
        with mss.mss() as sct:
            # Point(x=311, y=82)
            region = {
                "top": int(winY + 57), 
                "left": int(winX + 309),
                "width": int(45), 
                "height": int(15)
            }
            # 截取屏幕
            screenshot = sct.grab(region)
            mat_image = np.array(screenshot)
            num = 0
            try:
                num = self.recognize_number_text(mat_image)
            except ValueError as e:
                # 如果识别失败，就保存图片
                if(is_debug):
                    self.save_task_sample_img(mat_image)
                raise ValueError(e)
            return num


    # 是不是显示了元素塔塔的宝箱宝箱
    def is_show_tower_treasure(self):
        window = self.get_specific_window_info()
        if(window == None): raise RuntimeError('Err', f"{self.app_name}`s window is not found.")        
        
        winX, winY, winWidth, winHeight = self.get_win_info()
        screenshot = pyautogui.screenshot(region=(
            int(winX + 340), 
            int(winY + 214 - 77), 
            int(25), 
            int(10)
        ))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)
        target_color = (109, 228, 96)
        return self.is_target_area(mat_image, target_color)


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
    def is_task_complete(self, task_name):
        if(len(task_name) == 0):
            raise ValueError("Err: task_name cannot not be empty.")
        
        # 获取三个位置，如果是变绿了，就点击。
        isClicked = False
        while(self.click_complete_task_btn()):
            time.sleep(.3)
            self.clear_rewards()
            time.sleep(.3)
            isClicked = True
            
        if isClicked:
            return True

        # 如果有点击
        # TODO: 这里可能识别错误
        # 因为有缓动动画，所以要延迟2秒
        time.sleep(2)            
        # 获取task的list，判断是不是已经提交了
        task_list = self.read_task_list()
        for key, value in task_list.items():
            if(key == task_name and bool(value)):
                return True
        return False
    

    # 获取三个任务的领取按钮的位置，如果符合要求就点击
    def click_complete_task_btn(self):
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
        task_img_width = int(winWidth - 110)
        gutter = 12
        # start_y:end_y, start_x:end_x
        task_1_img = mat_image[12:task_img_heigt - 8 - gutter, 275:task_img_width]
        task_2_img = mat_image[task_img_heigt + 20:task_img_heigt * 2 - gutter, 275:task_img_width]
        task_3_img = mat_image[task_img_heigt + 95:task_img_heigt * 3 - 5 - gutter, 275:task_img_width]

        btn1 = (int((task_img_width // 2) + 185) , int((task_img_heigt - 8 - gutter) // 2 + 352))
        btn2 = (int((task_img_width // 2) + 185) , int((task_img_heigt * 2 - gutter) // 2  + task_img_heigt + 320))
        btn3 = (int((task_img_width // 2) + 185) , int((task_img_heigt * 3 - 5 - gutter) // 2  + task_img_heigt + 360))

        # 点击完成按钮
        green_color = (97, 198, 98)
        # 只点击第一个
        if(self.is_target_area(task_1_img, green_color, 0)):
            pyautogui.click(btn1[0], btn1[1])
            return True
        
        # if(self.is_target_area(task_2_img, green_color, 0)):
        #     pyautogui.click(btn2[0], btn2[1])
        #     return True

        # if(self.is_target_area(task_3_img, green_color, 0)):
        #     pyautogui.click(btn3[0], btn3[1])
        #     return True
        return False


    # 关闭奖励弹窗
    def clear_rewards(self, times = 1):
        self.logger.info("关闭奖励显示。")
        window = self.get_specific_window_info()
        if(window == None): raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
        winX, winY, winWidth, winHeight = self.get_win_info()
        for _ in range(int(times)):
            pyautogui.click(winX + winWidth - 10, winY + winHeight - 10)
            time.sleep(.3)


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


    # 统计颜色出现的次数
    def count_colors(self, bgr_image, top_color_num=10):
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
        print(f"前 {top_color_num} 种最常见的颜色:")
        for color, count in sorted_colors[:top_color_num]:
            r, g, b = color
            print(f"颜色\033[48;2;{r};{g};{b}m{color}\033[0m, 出现 {count} 次")

        return color_counts



    # 输出图片每个色块
    def print_img(self, mat_image):
        for row in range(mat_image.shape[0]):  # 遍历行
            for col in range(mat_image.shape[1]):  # 遍历列
                b, g, r = mat_image[row, col]  # 获取像素的 BGR 值
                self.print_color(f"{r},{g},{b}", r, g, b)


    # 读取屏幕中的任务列表
    def read_task_list(self):
        winX, winY, winWidth, winHeight = self.get_win_info()
        # # 读取指定位置
        with mss.mss() as sct:
            region = {
                "top": int(winY + 325), 
                "left": int(winX + 50),
                "width": int(winWidth - 100), 
                "height": int(winHeight - 650)
            }
            # 截取屏幕
            screenshot = sct.grab(region)
            
            mat_image = np.array(screenshot)
            mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)
            task_img_heigt = int((winHeight - 650 - 15) / 3)
            task_img_width = int(winWidth + 80)
            gutter = 30
            # start_y:end_y, start_x:end_x
            task_1_img = mat_image[20:task_img_heigt - 5 - gutter - 3 + 23, 255:task_img_width]
            task_2_img = mat_image[task_img_heigt * 2 + 38:task_img_heigt * 3 + 26 - gutter, 255:task_img_width]
            task_3_img = mat_image[task_img_heigt * 3 + 122:task_img_heigt * 3 + 179 - gutter, 255:task_img_width]

            # self.v_stack_show(
            #     self.preprocess_img(task_1_img),
            #     self.preprocess_img(task_2_img),
            #     self.preprocess_img(task_3_img),
            # )

            return {
                self.recognize_chinese_text(task_1_img): self.is_task_complete_by_color_percent(task_1_img),
                self.recognize_chinese_text(task_2_img): self.is_task_complete_by_color_percent(task_2_img),
                self.recognize_chinese_text(task_3_img): self.is_task_complete_by_color_percent(task_3_img),
            }


    # 保存今日工会任务的img
    def save_union_task_img(self):
        winX, winY, winWidth, winHeight = self.get_win_info()
        # 创建 mss 实例
        with mss.mss() as sct:
            region = {
                "top": int(winY + 325), 
                "left": int(winX + 50),
                "width": int(winWidth - 100), 
                "height": int(winHeight - 650)
            }
            # 截取屏幕
            screenshot = sct.grab(region)
            
            mat_image = np.array(screenshot)
            mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)
            task_img_heigt = int((winHeight - 650 - 15) / 3)
            task_img_width = int(winWidth + 80)
            gutter = 30
            # start_y:end_y, start_x:end_x
            task_1_img = mat_image[20:task_img_heigt - 5 - gutter - 3 + 23, 255:task_img_width]
            task_2_img = mat_image[task_img_heigt * 2 + 38:task_img_heigt * 3 + 26 - gutter, 255:task_img_width]
            task_3_img = mat_image[task_img_heigt * 3 + 122:task_img_heigt * 3 + 179 - gutter, 255:task_img_width]
            task_map = {
                self.recognize_chinese_text(task_1_img): task_1_img,
                self.recognize_chinese_text(task_2_img): task_2_img,
                self.recognize_chinese_text(task_3_img): task_3_img,
            }
            for key, img in task_map.items():
                # 找到需要完成的任务
                if(key.find("击杀") != -1):
                    self.save_task_sample_img(img)



    # 通过颜色占比来判断是否完成任务
    def is_task_complete_by_color_percent(self, bgr_img):
        complete_color = (229,223,217)
        rate = self.get_color_ratio(bgr_img, complete_color)
        # self.print_img(bgr_img)
        return rate <= 0.5


    # 读取中文
    def recognize_chinese_text(self, bgr_image):
        pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
        # 读取图片
        image = self.preprocess_img(bgr_image)

        # 识别中文文字，使用简体中文语言包 'chi_sim'
        text = pytesseract.image_to_string(image, lang='chi_sim',  config='--psm 6')  # 使用简体中文语言包
        return correct_text_handler(text)
    

    # 读取数字
    def recognize_number_text(self, bgr_image):
        pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
        # 读取图片
        image = self.preprocess_num_text_img(bgr_image)
        # self.save_task_sample_img(image)
        text = pytesseract.image_to_string(image, config='--psm 6')
        cleaned_text = re.sub(r"\s+", "", text)
        num = 0
        try:
            num = int(cleaned_text)
        except ValueError:
            self.logger.debug(f"recognize_number_text识别失败: {cleaned_text}")
            raise ValueError(f"recognize_number_text识别失败: {cleaned_text}")               
        return num


    # 处理代数字的图片
    def preprocess_num_text_img(self, bgr_img):
        scale_factor = 2.0  # 宽和高均放大两倍        
        # 转换为HSV颜色空间
        hsv_image = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
        # 扩大一倍
        resized_hsv_img = cv2.resize(hsv_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        resized_bgr_img = cv2.resize(bgr_img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

        # 定义白色的HSV颜色范围（例如：0-180度的色调，0-255的饱和度，200-255的明度）
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 20, 255])

        # 使用cv2.inRange()创建白色区域的掩模
        mask = cv2.inRange(resized_hsv_img, lower_white, upper_white)
        
        # 将白色区域设为白色，其他区域设为黑色
        final_image = cv2.bitwise_and(resized_bgr_img, resized_bgr_img, mask=mask)
        # 变成三维
        final_image = final_image[:, :, :-1]
        # 翻转
        inverted_image = cv2.bitwise_not(final_image)
        return inverted_image


    # 提高图像
    def preprocess_img(self, bgr_image):
        scale_factor = 2.0  # 宽和高均放大两倍
        # Laplacian 算子
        laplacian = cv2.Laplacian(bgr_image, cv2.CV_64F)
        # 将拉普拉斯算子的结果转换为 uint8
        laplacian = cv2.convertScaleAbs(laplacian)
        # 应用加权合成     
        sharp = cv2.addWeighted(bgr_image, 1.7, laplacian, -0.3, 0)
        # 扩大一倍
        # resized_img = cv2.resize(sharp, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        # 转换为灰度图像
        gray_image = cv2.cvtColor(sharp, cv2.COLOR_BGR2GRAY)
        # 进行二值化，提升OCR识别效果
        binary_image = cv2.adaptiveThreshold(
            gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 3
        )
        # # 轻微膨胀一次
        # kernel = np.ones((2, 2), np.uint8)  # 高度为1，宽度为15的矩阵
        # dilated = cv2.dilate(binary_image, kernel, iterations=1)

        blended_image = cv2.addWeighted(gray_image, 0.6, binary_image, 0.4, 0)
        return blended_image


    # 保存到sample的图片
    def save_task_sample_img(self, *imgs):
        for img in imgs:
            name = self.calculate_md5_from_image(img)
            path = f"static/sample/{name}.png"            
            cv2.imwrite(path, img)

            print(name)



    # 根据 OpenCV 的图像 NumPy 数组生成 MD5。
    # :param image_array: NumPy 数组，表示图像数据
    # :return: 图像数据的 MD5 字符串
    def calculate_md5_from_image(self, image_array):
        if not isinstance(image_array, np.ndarray):
            raise ValueError("输入数据不是有效的 NumPy 数组")

        # 将图像数据转换为字节流
        image_bytes = image_array.tobytes()

        # 计算 MD5 值
        md5_hash = hashlib.md5(image_bytes).hexdigest()
        return md5_hash


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
        target_rgb = (112,205,242)
        target_rgb1 = (74,166,212)
        target_rgb2 = (217,186,76)
        return self.is_target_area(mat_image, target_rgb, 0) and self.is_target_area(mat_image, target_rgb1, 0) and self.is_target_area(mat_image, target_rgb2, 0)


    # 读取竞技场第一个按钮
    def read_arena_first_btn(self):
        winX, winY, winWidth, winHeight = self.get_win_info()
        btnPos = (int(winX + 316), int(winY + 498), 85, 38)
        # 读取指定位置
        screenshot = pyautogui.screenshot(region=(btnPos))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)
        return mat_image


    # 读取安第一个竞技场按钮的坐标
    def get_arena_first_btn_pos(self):
        winX, winY, winWidth, winHeight = self.get_win_info()
        return (int(winX + 316 + 85 // 2),  int(winY + 498 + 38 // 2))


    # 是否能进入竞技场
    def is_enable_enter_arena(self):
        winX, winY, winWidth, winHeight = self.get_win_info()
        popupArea = (
            int(winX + 130),
            int(winY + winHeight // 2 - 5),
            180,
            10,
        )
        screenshot = pyautogui.screenshot(region=(popupArea))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)     
        targetColor = (147, 152, 156)
        return not self.is_target_area(mat_image, targetColor, 0)


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


    # 检测图片
    def detect_template(self, main_image, template_image_path, threshold=0.8):
        # 加载主图和模板图
        template = cv2.imread(template_image_path)
        
        if main_image is None or template is None:
            raise ValueError("无法加载主图或模板图，请检查路径是否正确。")
        
        # 转为灰度图
        main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        
        # 模板匹配
        result = cv2.matchTemplate(main_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        
        # 获取匹配结果中的最大值和位置
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        print(round(max_val, 2))
        # 判断是否匹配
        return round(max_val, 2) >= threshold


    # 知道boss死亡
    def till_boss_die(self, wait_max_time = 60 * 1):
        # 计划设置10分钟系统超时
        start_time = time.time()  # 记录开始时间
        timeout = wait_max_time # 超时时间，单位为秒

        while True:
            window = self.get_specific_window_info()
            if(window == None): 
                raise RuntimeError('Err', f"{self.app_name}`s window is not found.")

            elapsed_time = time.time() - start_time  # 计算已过去的时间
            if elapsed_time > timeout:
                raise TimeoutError(f"找宝箱超时: 未在{timeout}s内找到宝箱。")                

            # 死亡监控
            if(self.is_dead()):
                raise GameStatusError("泼街了，准备复活。")

            winX, winY, winWidth, winHeight = self.get_win_info()
            # 获取目标定位
            flagPos = (
                int(winX),
                int(winY + 110), 
                int(winWidth - winX),  # 宽度
                int(winHeight - winY - 110)  # 高度
            )
            screenshot = pyautogui.screenshot(region=flagPos)
            mat_image = np.array(screenshot)
            mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)
            
            # self.save_task_sample_img(mat_image)
            bloodColor = (213,70,66)
            isShowBlood = self.is_target_area(mat_image, bloodColor)
            # self.find_red_values(mat_image)
            if(not isShowBlood):
                self.logger.info("击杀boss成功.")
                return

            self.logger.info("等待击杀boss成功...")


    # 检测图片中出现的红色，并输出这些红色的像素值。
    def find_red_values(self, image_bgr):
        if image_bgr is None:
            raise ValueError("无法加载图片，请检查路径是否正确。")

        # 转换为 HSV 颜色空间
        hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

        # 定义红色的 HSV 范围（红色有两个区域）
        lower_red1 = np.array([0, 100, 100])     # 第一区间
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])   # 第二区间
        upper_red2 = np.array([179, 255, 255])

        # 创建掩膜
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2)

        # 使用掩膜提取红色区域的像素
        red_pixels = image_bgr[red_mask > 0]  # 提取红色区域的 BGR 值

        # 去重以获取唯一的红色值
        unique_red_values = np.unique(red_pixels, axis=0)
        
        # 输出检测结果
        if unique_red_values.size == 0:
            print("图片中未检测到红色。")
            return

        for color in unique_red_values:
            b, g, r = color  # BGR 格式
            self.print_color(f"{r},{g},{b}", r, g, b)


    # 直到出现箱子
    def till_find_treasure(self, treasure_num = 1, wait_max_time = 60 * 3):
        # 计划设置10分钟系统超时
        start_time = time.time()  # 记录开始时间
        timeout = wait_max_time # 超时时间，单位为秒
        # 如果有爆宝箱，却达不到treasure_num的标准，就降低标准
        tolerate_timeout = 30

        while True:
            window = self.get_specific_window_info()
            if(window == None): 
                raise RuntimeError('Err', f"{self.app_name}`s window is not found.")

            elapsed_time = time.time() - start_time  # 计算已过去的时间
            if elapsed_time > timeout:
                self.cache.set(IS_DALIY_CASE_FINISHED, 1)
                raise TimeoutError(f"找宝箱超时: 未在{timeout}s内找到宝箱。")                

            # 死亡监控
            if(self.is_dead()):
                raise GameStatusError("泼街了，准备复活。")


            winX, winY, winWidth, winHeight = self.get_win_info()
            # 获取目标定位
            flagPos = (
                int(winX),
                int(winY), 
                int(winWidth - winX),  # 宽度
                int(winHeight - winY)  # 高度
            )
            screenshot = pyautogui.screenshot(region=flagPos)
            mat_image = np.array(screenshot)
            mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)

            clickable_list = self.find_treasure_case()
            # print(clickable_list)
            if(len(clickable_list) >= treasure_num):
                break
            
            # 降低标准
            if(elapsed_time > tolerate_timeout and len(clickable_list) == 1):
                self.logger.debug("降级击杀BOSS多宝箱的标准。")
                break


            time.sleep(1)
            self.logger.info("等待击杀完boss,出现宝箱.")


    # 找到寻宝箱
    def find_treasure_case(self):
        green = (0x66,0xc1,0x52)
        clickable_list = self.get_targets_list(green, 0, 0)
        return clickable_list


    # 有广告和无广告的版本
    def click_rewards(self):
        window = self.get_specific_window_info()
        if(window == None): 
            raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
          
        winX, winY, winWidth, winHeight = self.get_win_info()
        # 获取目标定位
        flagPos = (
            int(winX + winWidth // 2 - 60),
            int(winY + 560),
            int(120),  # 宽度
            int(45)  # 高度
        )
        screenshot = pyautogui.screenshot(region=flagPos)
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)

        # 黄色广告的btn
        ads_btn = (221,200,75)

        start_time = time.time()  # 记录开始时间
        timeout = 30 # 超时时间，单位为秒
        while True:
            elapsed_time = time.time() - start_time  # 计算已过去的时间
            if elapsed_time > timeout:
                raise TimeoutError(f"点击领取按钮失败: 未在{timeout}s内点击领取宝箱成功。")
            # print(winX, winY)
            # 如果有广告就不看广告
            is_contain_ads = self.is_target_area(mat_image, ads_btn, 0)
            self.logger.debug(f"宝箱按钮为: [{'广告' if is_contain_ads else '普通' }]按钮")
            if(is_contain_ads):
                # Point(x=244, y=674)
                pyautogui.click(int(winX + winWidth // 2), int(winY + 560) + 90)
                self.logger.debug("点击跳过广告。")
                time.sleep(.3)
                self.clear_rewards()
                break

            if(not is_contain_ads):
                pyautogui.click(int(winX + winWidth // 2), int(winY + 560) + 12)
                self.logger.debug("领取奖励。")
                time.sleep(.3)
                self.clear_rewards()
                break

            # 这个延迟很有必要
            time.sleep(1.2)




        # # TODO: 广告无法关闭，根据金币的图片是否显示，判断是否点击成功。点击失败，就重复
        # if(is_contain_ads):
        #     self.logger.debug("包含广告，进入广告")
        #     # 进入广告
        #     self.logger.debug("等待广告加载...")
        #     self.wait_ads_loaded()
        #     self.logger.debug("已经加载广告完成")
        #     time.sleep(.3)

        #     # 静音
        #     self.mute_30s_ads()
        #     # 关闭
        #     self.close_30s_ads()
        #     self.logger.debug("等待广告结束")
        #     self.wait_ads_closed()
        #     self.logger.debug("广告已经结束")
        #     time.sleep(.3)
            
    
    # 关闭30s的广告
    def close_30s_ads(self):
        window = self.get_specific_window_info()
        if(window == None): 
            raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
          
        winX, winY, winWidth, winHeight = self.get_win_info()
        pyautogui.moveTo(int(winX + winWidth - 45), int(winY + 75),duration=.5)
        pyautogui.click(clicks=3)
        self.logger.debug("点击关闭按钮点击")
        

    # 静音广告
    def mute_30s_ads(self):
        window = self.get_specific_window_info()
        if(window == None): 
            raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
          
        winX, winY, winWidth, winHeight = self.get_win_info()   
        pyautogui.moveTo(int(winX + winWidth - 80), int(winY + 75), duration=.5)
        pyautogui.click(clicks=3)
        self.logger.debug("点击广告静音按钮")


    # 遍历目标颜色，检查比例是否超过阈值
    def is_target_color_present(self, mat_image, target_colors, threshold=0.7):
        for color in target_colors:
            result = self.get_color_ratio(mat_image, color)
            # print(f"Color {color}: {result}")
            # if result > threshold:
            if math.isclose(result, threshold, rel_tol=1e-9):
                return True
        return False

    
    # 是否显示了宝箱内容
    def is_treasure_pop_up(self):
        window = self.get_specific_window_info()
        if(window == None): 
            raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
          
        winX, winY, winWidth, winHeight = self.get_win_info()
        # 获取目标定位
        flagPos = (
            int(winX + 110),
            int(winY + 290),
            int(250),  # 宽度
            int(30)  # 高度
        )
        screenshot = pyautogui.screenshot(region=flagPos)
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)

        target_color = (54,122,107)
        target_color2 = (60,134,117)
        target_color3 = (59,132,116)

        target_colors = [target_color, target_color2, target_color3]
        return self.is_target_color_present(mat_image, target_colors)
        

    # 等待出现pop up
    def wait_treasure_pop_up(self, timeout = 30):
        start_time = time.time()  # 记录开始时间
        
        # 等待出现弹窗
        while self.is_treasure_pop_up():
            elapsed_time = time.time() - start_time  # 计算已过去的时间
            if elapsed_time > timeout:
                raise TimeoutError(f"等待超时: {timeout}s内寻找的宝箱弹窗。")
            time.sleep(.5)


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
                int((winWidth // 2) - 150 + winX), 
                int((winHeight // 2) - 150 + winY), 
                300, 
                300,
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
                time.sleep(.05)
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
        

    # 等待广告
    def __wait_ads_do(self, loaded_or_closed):
        self.logger.debug("等待广告加载...")
        start_time = time.time()  # 记录开始时间
        timeout = 60 * 2  # 超时时间，单位为秒\

        while True:
            elapsed_time = time.time() - start_time  # 计算已过去的时间
            if elapsed_time > timeout:
                raise TimeoutError("加载超时: 广告加载超时。")
            
            window = self.get_specific_window_info()
            if(window == None): 
                raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
            
            winX, winY, winWidth, winHeight = self.get_win_info()
            # 获取目标定位
            flagPos = (int(287 + winX), int(53 + winY), 20, 20)
            screenshot = pyautogui.screenshot(region=(flagPos))
            mat_image = np.array(screenshot)
            mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)
            # 金币的颜色
            target_rgb = (246,199,77)   # RGB 格式
            if(self.is_target_area(mat_image, target_rgb, 0) == loaded_or_closed):
                if(loaded_or_closed):  
                    self.logger.debug("广告已经关闭！") 
                if(not loaded_or_closed): 
                    self.logger.debug("广告加载完毕！")
                break


    # 等待广告加载完成
    def wait_ads_loaded(self):
        self.__wait_ads_do(False)


    # 等待广告看完
    def wait_ads_closed(self):
        self.__wait_ads_do(True)


    # 等待离开斗兽场
    def wait_selected_level_leave(self, level_name = "斗兽场"):
        self.logger.debug(f"等待离开[{level_name}]...")
        start_time = time.time()  # 记录开始时间
        timeout = 60 * 2  # 超时时间，单位为秒\

        while True:
            elapsed_time = time.time() - start_time  # 计算已过去的时间
            if elapsed_time > timeout:
                raise TimeoutError(f"等待超时: 等待离开[{level_name}]超时。")
            
            window = self.get_specific_window_info()
            if(window == None): 
                raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
            
            winX, winY, winWidth, winHeight = self.get_win_info()
            # 获取目标定位
            flagPos = (int(287 + winX), int(53 + winY), 20, 20)
            screenshot = pyautogui.screenshot(region=(flagPos))
            mat_image = np.array(screenshot)
            mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)
            # 金币的颜色
            target_rgb = (246,199,77)   # RGB 格式
            if(self.is_target_area(mat_image, target_rgb, 0)):
                break
            self.logger.debug(f"离开[{level_name}]: 等待中...")
            time.sleep(.6)


    # 等待进入斗兽场
    def wait_selected_level_entered(self, level_name = "斗兽场"):
        self.logger.debug(f"等待进入[{level_name}]...")
        start_time = time.time()  # 记录开始时间
        timeout = 60  # 超时时间，单位为秒\

        while True:
            elapsed_time = time.time() - start_time  # 计算已过去的时间
            if elapsed_time > timeout:
                raise TimeoutError(f"等待超时: {timeout}s等待进入[{level_name}]超时。")
            
            window = self.get_specific_window_info()
            if(window == None): 
                raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
            
            winX, winY, winWidth, winHeight = self.get_win_info()
            # 获取目标定位
            flagPos = (int((winWidth // 2) - 30 + winX), int(100 + winY), 45, 50)
            screenshot = pyautogui.screenshot(region=(flagPos))
            mat_image = np.array(screenshot)
            mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)
            # VS标志的颜色
            target_rgb1 = (80, 140, 215)   # 正常模式
            target_rgb2 = (72, 137, 233)   # 正常模式
            target_rgb3 = (24, 48, 82)     # 出现pk结果时，会变暗
            target_rgb4 = (30, 54, 83)     # 出现pk结果时，会变暗
            if(self.is_target_area(mat_image, target_rgb1, 0) or self.is_target_area(mat_image, target_rgb2, 0)):
                return
            
            if(self.is_target_area(mat_image, target_rgb3, 0) or self.is_target_area(mat_image, target_rgb4, 0)):
                return

            self.logger.debug(f"进入[{level_name}]: 等待中...")
            time.sleep(.6)



    # 等待战斗结束
    def wait_fight_over(self, level_name = "斗兽场"):
        self.logger.debug(f"等待[{level_name}]战斗结束...")
        start_time = time.time()  # 记录开始时间
        timeout = 60  # 超时时间，单位为秒\

        while True:
            elapsed_time = time.time() - start_time  # 计算已过去的时间
            if elapsed_time > timeout:
                raise TimeoutError(f"等待超时: {timeout}s等待战斗结束超时。")
            
            window = self.get_specific_window_info()
            if(window == None): 
                raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
            
            winX, winY, winWidth, winHeight = self.get_win_info()
            # 获取目标定位
            flagPos = (int((winWidth // 2) - 30 + winX), int(100 + winY), 45, 50)
            screenshot = pyautogui.screenshot(region=(flagPos))
            mat_image = np.array(screenshot)
            mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)
            # VS标志的颜色
            target_rgb3 = (24, 48, 82)     # 出现pk结果时，会变暗
            target_rgb4 = (30, 54, 83)     # 出现pk结果时，会变暗
            if(self.is_target_area(mat_image, target_rgb3, 0) or self.is_target_area(mat_image, target_rgb4, 0)):
                return
            
            # self.count_colors(mat_image)

            self.logger.debug(f"[{level_name}]打架中...")
            time.sleep(.6)


    # 是否能挑战塔
    def is_challenge_tower_available(self):
        window = self.get_specific_window_info()
        if(window == None): 
            raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
        
        winX, winY, winWidth, winHeight = self.get_win_info()
        # 获取目标定位
        flagPos = (int((winWidth // 2) - 3 + winX), int(winY + 702), 20, 11)
        screenshot = pyautogui.screenshot(region=(flagPos))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)
        target_rgb = (233, 94, 84)
        return not self.is_target_area(mat_image, target_rgb, 0)


    # 读取安第一个竞技场按钮的坐标
    def get_tower_challenge_btn_pos(self):
        winX, winY, winWidth, winHeight = self.get_win_info()
        return (int((winWidth // 2) - 55 + winX + 55), int(winY + 695 + 22.5))


    # 是不是带全了人
    def is_team_member_full(self):
        window = self.get_specific_window_info()
        if(window == None): 
            raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
        
        winX, winY, winWidth, winHeight = self.get_win_info()
        # 获取目标定位
        flagPos = (int(20 + winX), int(winY + 790), 13, 11)
        screenshot = pyautogui.screenshot(region=(flagPos))
        mat_image = np.array(screenshot)
        mat_image = cv2.cvtColor(mat_image, cv2.COLOR_RGB2BGR)
        target_rgb1 = (222, 89, 80)
        target_rgb2 = (226, 91, 81)
        return not self.is_target_area(mat_image, target_rgb1, 0) and not self.is_target_area(mat_image, target_rgb2, 0)


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
        
        # 获取窗口参数
        try:
            winX, winY, winWidth, winHeight = self.get_win_info()
        except RuntimeError as e:
            winX, winY, winWidth, winHeight = (0, 0, 0, 0)


        # 显示结果
        cv2.imshow("VerticalStack", stacked_img)
        cv2.moveWindow("VerticalStack", int(winX + winWidth), - 100)  
        cv2.waitKey(0)
        cv2.destroyAllWindows()


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
        kernel = np.ones((10, 10), np.uint8)
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


    # 获取游戏的中心点
    def get_center_point(self):
        winX, winY, winWidth, winHeight = self.get_win_info()
        return (int(winX + winWidth // 2), int(winY + winHeight // 2))


    # 获得两点之间的距离
    def get_point_distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)