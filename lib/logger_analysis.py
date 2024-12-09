
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


    # 分析最近7天的金币获取数量
    def get_last7days_coin_count_data(self):
        files_list = self.get_recent_logs()
        last7day_map = {}
        for filename in files_list:
            day = filename.replace('app_', '').replace('.log', '')
            path = self.logs_path  / filename
            last7day_map[day] = self.get_single_logger_coin_count(path)
            
        return last7day_map        