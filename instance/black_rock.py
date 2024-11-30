import time

from lib.move_controller import MoveControll

class CenterHall():

    def __init__ (self, config):
        self.config = config
        self.mc = MoveControll(config)
    
    # 一块地砖需要走 0.3s

    def crossRoom1(self):
        mc = self.mc
        
        # cuz falldown animation play
        # so wait
        time.sleep(7)

        mc.move_down(1.6)
        time.sleep(5)

        # 弯一结路begin
        mc.move_right(2.3)
        time.sleep(6)

        mc.move_left(2.3)
        time.sleep(3)        
        # 弯一结路end

        # 弯一结路begin
        mc.move_left(1.8)
        time.sleep(6)

        mc.move_right(1.8)
        time.sleep(.1)

        mc.move_down(1.4)
        time.sleep(6)

        mc.move_right(2.1)
        time.sleep(6)

        mc.move_down(1.6)
        time.sleep(6)

        mc.move_up(1.6)
        time.sleep(1)

        mc.move_left(2.1)
        time.sleep(1)

        mc.move_up(2.2)
        time.sleep(5)
        # 弯一结路end

        mc.move_left_top(1.8)
        time.sleep(5)

        mc.move_left_top(1.8)
        time.sleep(5)

        mc.move_right_top(1.6)
        time.sleep(5)

        mc.move_left_top(2.3)
        time.sleep(5)

        mc.move_left_top(1.5)
        time.sleep(5)

        mc.move_right_top(.9)
        time.sleep(5)

        mc.move_left_top(1.9)
        time.sleep(5)        

        # 弯一结路begin
        mc.move_down(1.2)
        time.sleep(8)        

        mc.move_up(1.2)
        time.sleep(.1)        
        # 弯一结路end

        mc.move_left_top(2.6)
        time.sleep(5)

        mc.move_left_down(2)
        time.sleep(5)

        mc.move_left_down(1.4)
        time.sleep(5)

        mc.move_left_down(1.4)
        time.sleep(5)

        mc.move_left_down(1.4)
        time.sleep(5)

        mc.move_left_down(1.4)
        time.sleep(10)
        
        # 走弯路 begin
        mc.move_left_top(1.6)
        time.sleep(5)

        mc.move_right_down(1.6)
        time.sleep(.1)
        # 走弯路 end


        mc.move_right_down(3)
        time.sleep(5)

        mc.move_right_down(2)
        time.sleep(5)

        # 走弯路 begin
        mc.move_right_top(1.8)
        time.sleep(5)

        mc.move_left_down(1.8)
        time.sleep(.3)
        # 走弯路 end

        mc.move_right_down(1.6)
        time.sleep(5)

        mc.move_left_down(1.6)
        time.sleep(5)                

        mc.move_left_down(4.4)
        time.sleep(6)

        mc.recover()
