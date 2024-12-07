import os
import queue
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
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
        self.app.get("/operate/down")(self.operate_left) 
        self.app.get("/operate/left")(self.operate_right) 
        self.app.get("/operate/right")(self.operate_down) 


    # index
    async def index(self):
        return FileResponse(self.html_path / "index.html", media_type='text/html')

    # 向上走
    async def operate_up(self):
        print(1)
        return {"code": 1, "message": "success"}


    # 向左走
    async def operate_left(self):
        print(1)
        return {"code": 1, "message": "success"}


    # 向右走
    async def operate_right(self):
        print(1)
        return {"code": 1, "message": "success"}
    
    # 向下走
    async def operate_down(self):
        print(1)
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