from instance import GameStatusEror
from lib import MoveControll
import time
from reader import InfoReader

class SnowZone:

    def __init__ (self):
        self.mc = MoveControll()
        self.reader = InfoReader()

    def check_handle(self):
        _, isMineFull = self.reader.read_screen()
        if(isMineFull): raise GameStatusEror("蓝矿满了")

    def recur(self):
        mc = self.mc

        self.check_handle()
        mc.move_up(1.6)
        time.sleep(3)

        self.check_handle()
        mc.move_up(1.6)
        time.sleep(3)        

        self.check_handle()
        mc.move_left(1.8)
        time.sleep(3)                

        self.check_handle()
        mc.move_up(1.8)
        time.sleep(3)        

        self.check_handle()
        mc.move_left(3.2)
        time.sleep(3)     

        self.check_handle()
        mc.move_left(2)
        time.sleep(5)     

        self.check_handle()
        mc.move_down(1.6)
        time.sleep(5)     

        self.check_handle()
        mc.move_left(2.4)
        time.sleep(5)     

        self.check_handle()
        mc.move_down(2.3)
        time.sleep(5)     

        self.check_handle()
        mc.move_right(1.7)
        time.sleep(5)

        # 打boss
        self.check_handle()        
        mc.move_down(2.3)
        time.sleep(6)     

        self.check_handle()
        mc.move_up(2.3)
        time.sleep(.1) 

        self.check_handle()
        mc.move_right(2)
        time.sleep(3)    

        self.check_handle()
        mc.move_right(1.8)
        time.sleep(3)    

        self.check_handle()
        mc.move_down(4)
        time.sleep(3) # 6      

        self.check_handle()
        mc.move_right(3.4)
        time.sleep(3) # 6    

        self.check_handle()
        mc.move_up(2.7)
        time.sleep(6) # 6   


    def room1Task(self):
        mc = self.mc

        self.check_handle()
        mc.move_left_down(3)
        time.sleep(3)

        self.check_handle()
        mc.move_left(1.6)
        time.sleep(3) # 6

        self.recur()



    def room1TaskBegin(self):
        mc = self.mc

        mc.move_left_down(3)
        time.sleep(3)

        mc.move_left(1.6)
        time.sleep(3) # 6


    def room1TaskLoop(self):
        self.recur()


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
