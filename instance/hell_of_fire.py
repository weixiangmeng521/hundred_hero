from exception.game_status import GameStatusError
import time
from lib.info_reader import InfoReader
from lib.move_controller import MoveControll

class HellOfFire:

    def __init__ (self, config):
        self.config = config
        self.mc = MoveControll(config)
        self.pace = 4
        self.reader = InfoReader(config)

    def check_handle(self):
        if(self.reader.is_dead()):
            raise GameStatusError("泼街了，准备复活。")

    def recur(self):
        mc = self.mc

        self.check_handle()
        mc.move_up(1)
        time.sleep(self.pace)

        self.check_handle()
        mc.move_up(2.8)
        time.sleep(self.pace * 1.5)

        self.check_handle()
        mc.move_left_top(1.4)
        time.sleep(self.pace)

        self.check_handle()
        mc.move_left_top(1.4)
        time.sleep(self.pace)

        self.check_handle()
        mc.move_left_down(2.8)
        time.sleep(self.pace * 2)

        self.check_handle()
        mc.move_down(1.2)
        time.sleep(self.pace)

        self.check_handle()
        mc.move_right(1.2)
        time.sleep(self.pace)

        self.check_handle()
        mc.move_down(2)
        time.sleep(self.pace)

        self.check_handle()
        mc.move_down(1)
        time.sleep(self.pace * 2)

        self.check_handle()
        mc.move_up(1)
        time.sleep(.3)

        self.check_handle()
        mc.move_right(1)
        time.sleep(self.pace)
        
        self.check_handle()
        mc.move_right(2.8)
        time.sleep(self.pace) 

        time.sleep(5)
        self.recur()



    def crossRoom1(self):
        mc = self.mc

        time.sleep(self.pace)

        self.check_handle()
        mc.move_left_down(2.6)
        time.sleep(self.pace * 1.5)

        self.recur()
    