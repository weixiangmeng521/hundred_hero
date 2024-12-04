import pyautogui
import Quartz
import cv2
from PIL import Image
import numpy as np
import math
from lib.logger import init_logger



# 视觉跟踪
class VisualTrack:

    def __init__(self, config):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = .5
        self.color = (255, 0, 0)  # 绿色
        self.thickness = 1
        self.app_name = config["APP"]["Name"]
        self.logger = init_logger(config)
    

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

        return (window_center[0], window_center[1], target_x, target_y)


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


        self.logger.info(f"图像大小 {winWidth} x {winHeight}; 中心点:({x},{y})")
        self.logger.info(f"目标点:({cX},{cY})")
        # return (center[1], center[0], cX, cY)
        bgr_image = cv2.cvtColor(rgb_img, cv2.COLOR_RGBA2BGR)
        return bgr_image


    # play frame
    def play_frame(self, target_color, lower_bound, upper_bound):
        img_win_name = "ImageAnalysis"  

        window = self.get_specific_window_info()
        if(window == None): raise RuntimeError('Err', f"{self.app_name}`s window is not found.")
        winX, winY, winWidth, winHeight = self.get_win_info()

        while True:
            frame = self.mark_in_frame(target_color, lower_bound, upper_bound)
            cv2.imshow(img_win_name, frame)
            cv2.moveWindow(img_win_name, int(winX + winWidth), - 100)        
            
            self.logger.info(winX, winY)

            # 设置刷新间隔，并检测按键退出
            key = cv2.waitKey(30)
            if key == ord('q') or key == 27:  # 27 是 ESC 的 ASCII 值
                cv2.destroyAllWindows()
                break


    # 找对象
    def find_object_in_image(self, bgr_template, bgr_image):
        # 加载图像和模板
        template = cv2.cvtColor(bgr_template, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        
        # 获取模板尺寸
        h, w = template.shape

        # 匹配模板
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 如果匹配程度较高，绘制矩形
        threshold = 0.3  # 阈值，越高越严格
        if max_val >= threshold:
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            image_with_rectangle = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            cv2.rectangle(image_with_rectangle, top_left, bottom_right, (0, 255, 0), 2)
            # print(f"匹配成功！匹配度：{max_val}")
            return image_with_rectangle
        else:
            print("未找到匹配对象。")
            return image

        # # 显示结果
        # cv2.imshow("Detected Object", image_with_rectangle)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


    # 测试find_object_in_image
    def test_for_find_object_in_image(self):
        template = cv2.imread("./static/npc/RecruitmentHall.jpg")
        rgb_template = cv2.cvtColor(template, cv2.COLOR_RGBA2BGR)
        img_win_name = "test"

        while True:
            winX, winY, winWidth, winHeight = self.get_win_info()
            screenshot = pyautogui.screenshot(region=(int(winX), int(winY), int(winWidth), int(winHeight)))
            mat_image = np.array(screenshot)
            rgb_img = cv2.cvtColor(mat_image, cv2.COLOR_RGBA2BGR)
            frame = self.find_object_in_image(rgb_template, rgb_img)

            cv2.imshow(img_win_name, frame)
            cv2.moveWindow(img_win_name, int(winX + winWidth), - 100)   

            # 设置刷新间隔，并检测按键退出
            key = cv2.waitKey(30)
            if key == ord('q') or key == 27:  # 27 是 ESC 的 ASCII 值
                cv2.destroyAllWindows()
                break        