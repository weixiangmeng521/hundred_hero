# 多线程管理
import threading
import time

from lib.logger import init_logger

# 多线程管理器
class ThreadsManager:
    def __init__(self, config, event_queue):
        self.config = config
        self.logger = init_logger(config)
        self.threads = {}  # 存储任务信息
        self.running = True  # 控制线程运行状态
        self.event_queue = event_queue
        # 重启时间
        if(not config["THREADS"]["RestartWaitTime"]):
            raise ValueError("RestartWaitTime cannot be invalid. please check config.ini.")

        self.restart_wait_time = int(config["THREADS"]["RestartWaitTime"])


    # 增加线程
    def add_task(self, name, handler):
        self.threads[name] = {'task': handler, 'thread': None}


    # 启动线程
    def start_thread(self, name):
        thread_task = self.threads[name]['task']
        thread = threading.Thread(target=thread_task, args=(self.event_queue,))
        thread.daemon = True  # 守护线程
        thread.start()
        self.threads[name]['thread'] = thread
        self.logger.debug(f"线程[{name}]启动成功")


    # 重启线程
    def restart_thread(self, name):
        self.logger.debug(f"尝试重启线程 {name}")
        self.start_thread(name)
        self.logger.debug(f"线程[{name}]已重启")


    # 运行
    def run(self):
        # 启动所有线程
        for name in self.threads.keys():
            self.start_thread(name)

        # 监控线程状态
        try:
            while self.running:
                for name, info in list(self.threads.items()):
                    thread = info['thread']
                    if not thread.is_alive():  # 检查线程存活状态
                        self.logger.warning(f"线程[{name}]已退出,{self.restart_wait_time}s后重启...")
                        time.sleep(self.restart_wait_time)
                        self.restart_thread(name)
                    time.sleep(1)

        except KeyboardInterrupt:
            self.logger.debug("主线程被手动中断，正在退出...")
            self.running = False
            for name, info in self.threads.items():
                self.logger.debug(f"等待线程[{name}]结束")
                thread = info['thread']
                if thread.is_alive():
                    thread.join(timeout=1)
            self.logger.debug("程序已正常退出")        