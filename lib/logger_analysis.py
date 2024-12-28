
from collections import defaultdict
import datetime
import os
from pathlib import Path
import re


instance = None
def get_logger_analysis_instance(config):
    global instance
    if(instance): return instance
    instance = LoggerAnalysis(config)
    return instance

# 日志分析
class LoggerAnalysis:

    def __init__(self, config):
        self.config = config
        self.logs_path = Path(__file__).resolve().parent / "../logs/"

    
    # 获得最近7天的日志
    def get_recent_logs(self, days=7):
        # 获取当前日期
        today = datetime.datetime.now()
        # 最近几天的日期范围
        recent_dates = [(today - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]
        
        # 在目录中查找符合条件的日志文件
        recent_logs = []
        for filename in os.listdir(self.logs_path):
            if any(date in filename for date in recent_dates):
                recent_logs.append(filename)
        # 排序
        sorted_logs = sorted(recent_logs, key=lambda x: x.split('_')[1].split('.log')[0])
        return sorted_logs


    # 读取文件的内容
    def get_file_content(self, path, chunk_size=1024):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                while True:
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk  # 使用生成器逐块返回内容
        except FileNotFoundError:
            yield f"文件未找到: {path}"
        except PermissionError:
            yield f"没有权限读取: {path}"
        except Exception as e:
            yield f"读取错误: {e}"


    # 获得单个文件里面的card出现次数的统计
    def get_single_logger_cards_count_map(self, path):
        result_map = defaultdict(int)
        target = "当前卡为:"
        # 逐块读取文件内容
        for content in self.get_file_content(path):
            # 按行分割
            lines = content.splitlines()
            for line in lines:
                if target in line:
                    # 提取目标字符串后的部分
                    elements = line.split(target)[-1].strip().split(',')
                    # 统计出现的元素
                    for element in elements:
                        key = element.strip()
                        if key:
                            result_map[key] += 1
        return dict(result_map)


    #获得最近7天的card出现的次数
    def get_last7days_cards_count_map(self):
        files_list = self.get_recent_logs()
        last7day_map = {}
        for filename in files_list:
            day = filename.replace('app_', '').replace('.log', '')
            path = self.logs_path  / filename
            last7day_map[day] = self.get_single_logger_cards_count_map(path)
        return last7day_map
    

    # 获取单个文件里面coin获取的数量
    def get_single_logger_coin_count(self, path):
        _list = []
        target = "总打金:"
        total = 0

        # 逐块读取文件内容
        for content in self.get_file_content(path):
            # 按行分割
            lines = content.splitlines()
            for line in lines:
                if target in line:
                    # 提取目标字符串后的数字
                    match = re.search(r'总打金:\s*(\d+)', line)
                    if match:
                        current_value = int(match.group(1))
                        # 检查断裂点并累加
                        if _list and _list[-1] > current_value:
                            total += _list[-1]
                        _list.append(current_value)

        # 处理最后一个断裂点值（如适用）
        if _list:
            total += _list[-1]

        return total


    # 获取当天的执行异常的data
    def get_today_error_message_data(self):
        filename_list = self.get_recent_logs()
        current_date_filename = filename_list[-1]
        
        data_map = {hour: 0 for hour in range(1, 25)}
        path = self.logs_path  / current_date_filename
        target = "Traceback"
        # 逐块读取文件内容
        for content in self.get_file_content(path):
            # 按行分割
            lines = content.splitlines()
            for line in lines:
                if target in line:
                    # 使用正则表达式提取时间部分
                    match = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}", line)
                    if match:
                        time_str = match.group(0)
                        log_time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S,%f")
                        hour = log_time.hour + 1  # 将小时数转换为1-24
                        data_map[hour] += 1                
        return dict(data_map)
        


    # 分析最近7天的金币获取数量
    def get_last7days_coin_count_data(self):
        files_list = self.get_recent_logs()
        last7day_map = {}
        for filename in files_list:
            day = filename.replace('app_', '').replace('.log', '')
            path = self.logs_path  / filename
            last7day_map[day] = self.get_single_logger_coin_count(path)
            
        return last7day_map        
    

    # 判断是不是符合混合垃圾组合
    def is_worst_cards_group(self, cards):
        tar1, tar2 = '蓝卡', '垃圾'
        # 去除卡片中的空格
        cards = [card.strip() for card in cards]
        # 检查是否所有卡片都在目标类型中
        for card in cards:
            if card not in (tar1, tar2):
                return False
        return True


    # 判断是不是符合混合垃圾组合
    def is_2worst_cards_and_1great_group(self, cards):
        tar1, tar2 = '蓝卡', '垃圾'  # 白卡类型
        special_cards = {'红卡', '黄卡', '紫卡'}  # 特定颜色卡片
        # 去除卡片中的空格
        cards = [card.strip() for card in cards]
        
        # 统计白卡数量
        white_cards = [card for card in cards if card in (tar1, tar2)]
        special_card = [card for card in cards if card in special_cards]

        # 判断是否满足条件
        return len(white_cards) == 2 and len(special_card) == 1


    # 获得最好的卡
    def get_greatest_card_in_group(self, cards):
        special_cards = {'红卡', '黄卡', '紫卡'}  # 特定颜色卡片
        # 去除卡片中的空格
        cards = [card.strip() for card in cards]
        for card in cards:
            if card in special_cards:
                return card
        return None


    # 获取单个文件里面抽卡结果
    def get_single_logger_recruited_hero_count(self, path):
        result_map = defaultdict(int)
        target = "抽卡结果:"
        # 逐块读取文件内容
        for content in self.get_file_content(path):
            # 按行分割
            lines = content.splitlines()
            for line in lines:
                if target in line:
                    # 提取目标字符串后的部分
                    matches = re.findall(r'DEBUG.*?\[(.*?)\]', line)
                    for match in matches:  # 遍历所有匹配项                    
                        result_map[match] += 1  # 使用匹配项作为键
        
        # 混合态的卡牌
        target = "当前卡为:"
        worst_group_times = 0
        # 逐块读取文件内容
        for content in self.get_file_content(path):
            # 按行分割
            lines = content.splitlines()
            for index, line in enumerate(lines):
                if target in line:
                    next_line = ""
                    if index + 1 < len(lines):
                        next_line = lines[index + 1]

                    # 提取目标字符串后的部分
                    elements = line.split(target)[-1].strip().split(',')
                    if(self.is_worst_cards_group(elements)):
                        worst_group_times += 1

                    if(self.is_2worst_cards_and_1great_group(elements) and not ("抽卡结果:" in next_line)):
                        greatest_card = self.get_greatest_card_in_group(elements)
                        if(greatest_card):
                            result_map[greatest_card] += 1

        result_map["垃圾组合"] = worst_group_times
        return dict(result_map)



    #获得当天的card出现的次数
    def get_today_recruited_hero_count_map(self):
        files_list = self.get_recent_logs(1)
        data = []
        for filename in files_list:
            path = self.logs_path  / filename
            data = self.get_single_logger_recruited_hero_count(path)
        return data
     