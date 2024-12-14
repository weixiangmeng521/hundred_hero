import base64
import datetime
import os
import queue
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from defined import DOWN_MOVE_CMD, FIND_ARENA, FIND_PORTAL, FIND_RECRUIT_NPC, FIND_TOWER, FIND_TRAINING_NPC, LEFT_MOVE_CMD, RIGHT_MOVE_CMD, UP_MOVE_CMD
from lib.cache import get_cache_manager_instance
from lib.controll_wechat import init_controll_wechat
from lib.logger import init_logger
from pathlib import Path

from lib.logger_analysis import get_logger_analysis_instance

# Web服务
class WebServer:
    
    def __init__(self, config):
        self.config = config
        self.event_queue = None
        self.logger = init_logger(config)
        self.host = config["WEB_SERVER"]["Host"]
        self.port = config["WEB_SERVER"]["Port"]
        self.app = FastAPI()
        self.cache = get_cache_manager_instance(config)
        self.html_path = Path(__file__).resolve().parent / "../static/"
        self.logs_path = Path(__file__).resolve().parent / "../logs/"
        self.qr_code_path = Path(__file__).resolve().parent / "../QR_code/QRcode.png"
        self.logger_analysis = get_logger_analysis_instance(config)
        self.controll_wechat = init_controll_wechat(config)
        self.setup_routes()


    # 设置路由
    def setup_routes(self):
        # 页面
        self.app.get("/")(self.index)
        self.app.get("/controll")(self.controll_page)
        self.app.get("/logger")(self.logger_page)
        
        self.app.get("/operate/up")(self.operate_up) 
        self.app.get("/operate/down")(self.operate_down) 
        self.app.get("/operate/left")(self.operate_left) 
        self.app.get("/operate/right")(self.operate_right) 
        self.app.get("/operate/status")(self.get_operate_status) 

        self.app.get("/find/training_npc")(self.find_training_npc) 
        self.app.get("/find/recruit_npc")(self.find_recruit_npc) 
        self.app.get("/find/protal")(self.find_portal) 
        self.app.get("/find/arena")(self.find_arena) 
        self.app.get("/find/tower")(self.find_tower) 

        self.app.get("/task/list")(self.get_task_list)

        self.app.get("/system/config")(self.get_config)
        self.app.get("/system/logs")(self.get_logs)
        self.app.get("/system/qr_code")(self.get_login_code)

        self.app.get("/graph/last7days_cards_map")(self.get_recent7days_cards_data)
        self.app.get("/graph/last7days_coins_data")(self.get_recent7days_coins_data)
        self.app.get("/graph/today_error_data")(self.get_today_error_data)

    # index
    async def index(self):
        return FileResponse(self.html_path / "index.html", media_type='text/html')

    # controll
    async def controll_page(self):
        return FileResponse(self.html_path / "controll.html", media_type='text/html')

    # controll
    async def logger_page(self):
        return FileResponse(self.html_path / "logger.html", media_type='text/html')

    # 获取QR code
    async def get_login_code(self):
        code = self.controll_wechat.get_state()
        base64Img = self.get_QRcode_img_base64()

        return {
            "code": 1,
            "data": {
                "state": code,
                "img": base64Img,
            }
        }
    
    # 获取base64
    def get_QRcode_img_base64(self):
        with open(self.qr_code_path, "rb") as image_file:
            img_base64 = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/png;base64,{img_base64}"


    # 获取控制服务状态
    async def get_operate_status(self):
        status = self.config.getboolean('TASK', 'EnableVirtualMap')
        return {"code": 1 if status == True else "-1"}


    # 获得最近7日的抽卡数据
    async def get_recent7days_cards_data(self):
        data = self.logger_analysis.get_last7days_cards_count_map()
        return {"code": 1, "message": "success", "data": data}


    # 获得最近7日的刷钱数据
    async def get_recent7days_coins_data(self):
        data = self.logger_analysis.get_last7days_coin_count_data()
        return {"code": 1, "message": "success", "data": data}


    # 获取当天的错误信息
    async def get_today_error_data(self):
        data = self.logger_analysis.get_today_error_message_data()
        return {"code": 1, "message": "success", "data": data}


    # 获取日志
    async def get_logs(self):
        filename = datetime.datetime.now().strftime("app_%Y-%m-%d.log")
        res = self.tail_log(self.logs_path / filename)
        return {"code": 1, "message": "success", "data": res}


    # 获取task的进展情况
    async def get_task_list(self):
        task_list = self.cache.all()
        return {"code": 1, "message": "success", "data": task_list}


    # 获取系统配置
    async def get_config(self):
        return {"code": 1, "message": "success","data": self.config}


    # 向上走
    async def operate_up(self):
        if(not self.event_queue):
            return {"code": -1, "message": "event_queue cannot be null pointer"}
        
        self.event_queue.put(UP_MOVE_CMD)
        return {"code": 1, "message": "success"}


    # 向左走
    async def operate_left(self):
        if(not self.event_queue):
            return {"code": -1, "message": "event_queue cannot be null pointer"}
        
        self.event_queue.put(LEFT_MOVE_CMD)
        return {"code": 1, "message": "success"}


    # 向右走
    async def operate_right(self):
        if(not self.event_queue):
            return {"code": -1, "message": "event_queue cannot be null pointer"}
        
        self.event_queue.put(RIGHT_MOVE_CMD)
        return {"code": 1, "message": "success"}
    

    # 向下走
    async def operate_down(self):
        if(not self.event_queue):
            return {"code": -1, "message": "event_queue cannot be null pointer"}
        
        self.event_queue.put(DOWN_MOVE_CMD)
        return {"code": 1, "message": "success"}


    # 找到训练营NPC
    async def find_training_npc(self):
        if(not self.event_queue):
            return {"code": -1, "message": "event_queue cannot be null pointer"}
        
        self.event_queue.put(FIND_TRAINING_NPC)
        return {"code": 1, "message": "success"}


    # 找到招募大厅NPC
    async def find_recruit_npc(self):
        if(not self.event_queue):
            return {"code": -1, "message": "event_queue cannot be null pointer"}
        
        self.event_queue.put(FIND_RECRUIT_NPC)
        return {"code": 1, "message": "success"}
    

    # 找到传送阵
    async def find_portal(self):
        if(not self.event_queue):
            return {"code": -1, "message": "event_queue cannot be null pointer"}
        
        self.event_queue.put(FIND_PORTAL)
        return {"code": 1, "message": "success"}


    # 找到决斗场
    async def find_arena(self):
        if(not self.event_queue):
            return {"code": -1, "message": "event_queue cannot be null pointer"}
        
        self.event_queue.put(FIND_ARENA)
        return {"code": 1, "message": "success"}
    

    # 找到塔
    async def find_tower(self):
        if(not self.event_queue):
            return {"code": -1, "message": "event_queue cannot be null pointer"}
        
        self.event_queue.put(FIND_TOWER)
        return {"code": 1, "message": "success"}


    # 输出最后300行
    def tail_log(self, file_path, lines=300, buffer_size=8192):
        with open(file_path, 'rb') as f:
            f.seek(0, 2)  # 文件指针移动到末尾
            file_size = f.tell()
            block_size = buffer_size
            data = b''
            line_count = 0
            
            while file_size > 0 and line_count <= lines:
                if file_size - block_size < 0:
                    block_size = file_size
                f.seek(file_size - block_size, 0)
                data = f.read(block_size) + data
                file_size -= block_size
                line_count = data.count(b'\n')

            return data.decode('utf-8', errors='ignore').splitlines()[-lines:]




    # 启动
    def run(self, event_queue:queue.Queue):
        import uvicorn
        self.event_queue = event_queue

        # 读取静态文件夹
        static_dir = os.path.join(os.path.dirname(__file__), "../static/")
        self.app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
        # self.app.add_middleware(
        #     CORSMiddleware,
        #     allow_origins=['*'],
        #     allow_credentials=True,
        #     allow_methods=["*"],
        #     allow_headers=["*"],
        # )
        # 输出日志
        self.logger.debug(f"Server is running on: {self.host}:{self.port}")
        
        ENABLE_VIRTUAL_MAP = self.config.getboolean('TASK', 'EnableVirtualMap')
        if(ENABLE_VIRTUAL_MAP): self.logger.debug("当前为虚拟MAP测试模式.")
        
        uvicorn.run(self.app, host=self.host, port=int(self.port))