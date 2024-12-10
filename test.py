

import configparser
from lib.logger_analysis import get_logger_analysis_instance

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

log_analysis = get_logger_analysis_instance(config)
data = log_analysis.get_current_error_message_data()
print(data)

# macos的自带25px的边
# macos自带图片查看器的边框为（80 - 25）px
# 微信小程序百炼英雄的白条win的宽为（125 - 80）px
# 图片查看模式下，下一关按钮的定位为 Point(x=316, y=746)
# 由此可知: 他的坐标为 winX + 316, winY - (80 - 25) - 25 + 746