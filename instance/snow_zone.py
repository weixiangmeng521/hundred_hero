from exception.game_status import GameStatusError
import time
from lib.info_reader import InfoReader
from lib.move_controller import MoveControll


class SnowZone:

    def __init__ (self, config):
        self.config = config
        self.mc = MoveControll(config)
        self.reader = InfoReader(config)


    def check_handle(self, is_check = True):
        if(not is_check):
            return
        _, isMineFull = self.reader.read_screen()
        if(isMineFull): raise GameStatusError("蓝矿满了")


    def recur(self, is_check = True, wait_time = 3):
        mc = self.mc

        self.check_handle(is_check)
        mc.move_up(1.6)
        time.sleep(wait_time)

        self.check_handle(is_check)
        mc.move_up(1.6)
        time.sleep(wait_time)        

        self.check_handle(is_check)
        mc.move_left(1.8)
        time.sleep(wait_time)                

        self.check_handle(is_check)
        mc.move_up(1.8)
        time.sleep(wait_time)        

        self.check_handle(is_check)
        mc.move_left(3.2)
        time.sleep(wait_time)     

        self.check_handle(is_check)
        mc.move_left(2)
        time.sleep(wait_time * 1.5)     

        self.check_handle(is_check)
        mc.move_down(1.6)
        time.sleep(wait_time * 1.5)     

        self.check_handle(is_check)
        mc.move_left(2.3)
        time.sleep(wait_time * 1.5)     

        self.check_handle(is_check)
        mc.move_down(.6)
        time.sleep(wait_time * 1.5) 

        self.check_handle(is_check)
        mc.move_down(1.7)
        time.sleep(wait_time * 1.5)            

        self.check_handle(is_check)
        mc.move_right(1.9)
        time.sleep(wait_time * 1.5)

        # 打boss
        self.check_handle(is_check)        
        mc.move_down(2)
        time.sleep(wait_time * 2)     

        self.check_handle(is_check)
        mc.move_up(2)
        time.sleep(.1) 

        self.check_handle(is_check)
        mc.move_right(2)
        time.sleep(wait_time)    

        # 走弯路 begin
        self.check_handle(is_check)        
        mc.move_up(1.2)
        time.sleep(wait_time * 2)     

        self.check_handle(is_check)
        mc.move_down(1.2)
        time.sleep(.1) 
        # 走弯路 end

        self.check_handle(is_check)
        mc.move_right(1.8)
        time.sleep(wait_time)    

        self.check_handle(is_check)
        mc.move_down(1)
        time.sleep(wait_time) # 6      

        self.check_handle(is_check)
        mc.move_down(3)
        time.sleep(wait_time) # 6    

        self.check_handle(is_check)
        mc.move_right(3.4)
        time.sleep(wait_time) # 6    

        self.check_handle(is_check)
        mc.move_up(2.7)
        time.sleep(wait_time) # 6   

        self.check_handle(is_check)
        mc.move_right(1.2)
        time.sleep(wait_time) # 6   

        self.check_handle(is_check)
        mc.move_left(1.2)
        time.sleep(wait_time) # 6   



    def room1Task(self):
        mc = self.mc

        self.check_handle()
        mc.move_left_down(3)
        time.sleep(3)

        self.check_handle()
        mc.move_left(1.6)
        time.sleep(3) # 6

        self.recur()


    # 北风营地
    def room1TaskBegin(self):
        mc = self.mc

        mc.move_left_down(3)
        # time.sleep(3)

        mc.move_left(1.6)
        time.sleep(1) # 6


    # 北风营地循环圈
    def room1TaskLoop(self, is_check = True, wait_time = 3):
        self.recur(is_check, wait_time)


    def crossRoom1Loop(self):
        mc = self.mc

        mc.move_left_down(3)
        time.sleep(3)

        mc.move_left(1.6)
        time.sleep(3) # 6

        while True:
            self.recur()


    def crossGuildRoom(self):
        mc = self.mc

        pace = 3

        mc.move_left_top(4)
        time.sleep(pace)
 
        mc.move_left(1)
        time.sleep(pace * 2)

        mc.move_up(1.8)
        time.sleep(pace)

        mc.move_right(1.8)
        time.sleep(pace * 2)

        mc.move_up(2.8)
        time.sleep(pace)

        mc.move_left(1.8)
        time.sleep(pace)

        mc.move_up(2.9)
        time.sleep(pace)

        mc.move_left(1.4)
        time.sleep(pace)

        mc.move_down(.6)
        time.sleep(pace)

        mc.move_left(3.6)
        time.sleep(pace)

        mc.move_down(1.6)
        time.sleep(pace)

        mc.move_down(1.6)
        time.sleep(pace)

        mc.move_down(1.7)
        time.sleep(pace)

        mc.move_left(1.2)
        time.sleep(pace)

        mc.move_down(2.1)
        time.sleep(pace)

        # BOSS
        mc.move_right(2.1)
        time.sleep(pace * 2)

        mc.move_down(3.2)
        time.sleep(pace)

        mc.move_right(3.2)
        time.sleep(pace)

        mc.move_up(1.8)
        time.sleep(pace)

        mc.move_down(1.8)
        time.sleep(.1)

        mc.move_right(3)
        time.sleep(pace)

        mc.move_down(1.3)
        time.sleep(pace)

        mc.move_right(1.5)
        time.sleep(pace)

        mc.move_down(2.4)
        time.sleep(pace)

        # BOSS
        mc.move_right(1.5)
        time.sleep(pace * 4)

        mc.move_right(.6)
        time.sleep(pace)

        mc.move_up(2)
        time.sleep(pace)

        mc.move_up(1.2)
        time.sleep(pace)

        mc.move_left(1)
        time.sleep(pace)

        mc.move_up(1.6)
        time.sleep(pace)


    # 杀雪人boss
    def killSnowManBoss(self):
        mc = self.mc

        mc.move_down(4.2)
        time.sleep(2.4)
 
        def lamd():
            mc.move_up(4.5)
        return lamd
    
    # 杀双头蛇
    def killTwoHeadSnakeBoss(self):
        mc = self.mc

        mc.move_left_down(3)
        mc.move_left(8)
        mc.move_down(1)

        time.sleep(3)


    # 击杀猛犸巨像
    def killMammoth(self):
        mc = self.mc

        mc.move_down(.9)
        mc.move_left(1.6)
        mc.move_down(.9)
        mc.move_left(6.6)
        mc.move_top(2.3)

        time.sleep(3)


