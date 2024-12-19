import datetime
import json
import os
import threading
import time

from lib.logger import init_logger

# 单例模式
cache_manager_instance = None
def get_cache_manager_instance(config):
    global cache_manager_instance
    if(cache_manager_instance):
        return cache_manager_instance
    cache_manager_instance = CacheManager(config)
    return cache_manager_instance
    

# 缓存管理
class CacheManager:
    def __init__(self, config):
        self.config = config
        self.cache = {}  # 缓存存储结构
        self.lock = threading.Lock()  # 线程锁保护数据完整性
        self.file_name = config["CACHE"]["FileName"]  # 缓存文件路径
        self.logger = init_logger(config)
        # 初始化时加载缓存文件
        with self.lock:
            self._load_cache()


    # 从文件加载缓存数据，自动清理已过期的键。
    def _load_cache(self):
        # 如果没有设置filename，就直接退出
        if not self.file_name:
            return
        
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as f:
                try:
                    data = json.load(f)
                    now = int(time.time())
                    # 过滤未过期的缓存
                    self.cache = {k: v for k, v in data.items() if v["expiry"] > now}
                    self.logger.debug(f"加载缓存[{self.file_name}]成功.")
                except json.JSONDecodeError:
                    self.logger.debug("缓存文件损坏，无法加载。")


    # 保存当前缓存数据到文件。
    def _save_cache(self):
        # 如果没有设置filename，就直接退出
        if not self.file_name:
            return
        
        # 如果文件不存在，先创建空文件
        if not os.path.exists(self.file_name):
            with open(self.file_name, "w") as f:
                f.write(json.dumps(self.cache))  # 初始化为一个空 JSON 对象

        # 保存缓存数据到文件
        with open(self.file_name, "w") as f:
            json.dump(self.cache, f)


    # 计算下一次过期时间（第二天凌晨 1 点）。
    def _get_next_expiry(self, extra_time = 0):
        now = datetime.datetime.now()
        next_day = now + datetime.timedelta(days=1)  # 修复此处的 timedelta 引用
        expiry_time = datetime.datetime(next_day.year, next_day.month, next_day.day, 1 + extra_time, 0, 0)
        return int(expiry_time.timestamp())


    # 存储键值对到缓存中，设置过期时间为第二天凌晨 1 点。
    def set(self, key, value, extra_expire_time = 0):
        expiry_time = self._get_next_expiry(extra_expire_time)
        with self.lock:
            self.cache[key] = {"value": value, "expiry": expiry_time}
            self._save_cache()  # 每次更新缓存时保存到文件


    # 把过期时间延长一个小时
    def set_next_hour(self, task_name):
        _time = self.get(task_name)
        if _time is not None:
            # 确保 _time 是时间戳，转换为 datetime 对象
            task_time = datetime.datetime.fromtimestamp(_time)
            next_hour = task_time + datetime.timedelta(hours=1)
            self.set(task_name, int(next_hour.timestamp()))
        else:
            self.logger.debug(f"Task '{task_name}' not found.")


    # 获取缓存中的值。如果键不存在或已过期，返回 None。
    def get(self, key):
        with self.lock:
            if key in self.cache:
                item = self.cache[key]
                if int(time.time()) < item["expiry"]:
                    return item["value"]
                else:
                    del self.cache[key]  # 删除已过期的键
                    self._save_cache()  # 保存更新后的缓存
            return None
        
    
    # 读取全部缓存
    def all(self):
        return self.cache


    # 清理所有过期的键。
    def clear_expired(self):
        with self.lock:
            now = int(time.time())
            self.cache = {k: v for k, v in self.cache.items() if v["expiry"] > now}
            self._save_cache()


    # 清理所有缓存。
    def clear_all(self):
        with self.lock:
            self.cache.clear()
            self._save_cache()
        