

import configparser
from lib.logger_analysis import get_logger_analysis_instance

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

log_analysis = get_logger_analysis_instance(config)
data = log_analysis.get_last7days_coin_count_data()
print(data)