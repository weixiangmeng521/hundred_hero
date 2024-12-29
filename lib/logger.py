import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import os


# singleton
is_initialized_logger = False

# 初始化日志管理器
def init_logger(config):
    app_name = config["APP"]["Name"]
    logger_name = f"[{app_name}]"    
    global is_initialized_logger

    if(is_initialized_logger):
        return logging.getLogger(logger_name)

    # 检查日志是否已经初始化
    logger = logging.getLogger(logger_name)
    if logger.handlers:
        return logger

    # 动态生成日志文件夹和文件名
    log_dir = "logs"  # 子文件夹名称
    os.makedirs(log_dir, exist_ok=True)  # 如果文件夹不存在，则创建

    # 使用当前日期生成日志文件名
    log_filename = datetime.datetime.now().strftime("app_%Y-%m-%d.log")
    log_filepath = os.path.join(log_dir, log_filename)

    # 配置日志级别
    logger.setLevel(logging.DEBUG)

    # 配置 TimedRotatingFileHandler
    rotating_handler = TimedRotatingFileHandler(
        log_filepath, when="midnight", interval=1, backupCount=7, encoding="utf-8"
    )
    rotating_handler.setLevel(logging.DEBUG)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    rotating_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加处理器到日志器
    logger.addHandler(rotating_handler)
    logger.addHandler(console_handler)

    is_initialized_logger = True
    return logger