import datetime
import logging
import os


def init_logger(app_name):
    # 动态生成日志文件夹和文件名
    log_dir = "logs"  # 子文件夹名称
    if not os.path.exists(log_dir):  # 如果文件夹不存在，则创建
        os.makedirs(log_dir)
    
    # 创建日志器
    logger = logging.getLogger(f"[{app_name}]")
    logger.setLevel(logging.DEBUG)

    # 使用当前日期生成日志文件名
    log_filename = datetime.datetime.now().strftime("app_%Y-%m-%d.log")
    log_filepath = os.path.join(log_dir, log_filename)    

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # 创建文件处理器
    file_handler = logging.FileHandler(log_filepath, mode='a')
    file_handler.setLevel(logging.INFO)

    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 添加处理器到日志器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger