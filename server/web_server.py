import os
import queue
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from defined import DOWN_MOVE_CMD, FIND_PORTAL, FIND_RECRUIT_NPC, FIND_TRAINING_NPC, LEFT_MOVE_CMD, RIGHT_MOVE_CMD, UP_MOVE_CMD
from lib.logger import init_logger
from pathlib import Path

# Web服务
class WebServer:
    
    def __init__(self, config):
        self.config = config
        self.event_queue = None
        self.logger = init_logger(config)
        self.host = config["WEB_SERVER"]["Host"]
        self.port = config["WEB_SERVER"]["Port"]
        self.app = FastAPI()
        self.html_path = Path(__file__).resolve().parent / "../static/"
        self.setup_routes()


    # 设置路由
    def setup_routes(self):
        self.app.get("/")(self.index)
        
        self.app.get("/operate/up")(self.operate_up) 
        self.app.get("/operate/down")(self.operate_down) 
        self.app.get("/operate/left")(self.operate_left) 
        self.app.get("/operate/right")(self.operate_right) 

        self.app.get("/find/training_npc")(self.find_training_npc) 
        self.app.get("/find/recruit_npc")(self.find_recruit_npc) 
        self.app.get("/find/protal")(self.find_portal) 

    # index
    async def index(self):
        return FileResponse(self.html_path / "index.html", media_type='text/html')


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


    # 启动
    def run(self, event_queue:queue.Queue):
        import uvicorn
        self.event_queue = event_queue

        # 读取静态文件夹
        static_dir = os.path.join(os.path.dirname(__file__), "../static/")
        self.app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # 输出日志
        self.logger.debug(f"Server is running on: {self.host}:{self.port}")
        uvicorn.run(self.app, host=self.host, port=int(self.port))