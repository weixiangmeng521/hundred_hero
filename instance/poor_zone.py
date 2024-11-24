import time
from instance import GameStatusEror
from lib import MoveControll


class PoorZone:
    mc = MoveControll()

    def check_handle(self):
        if(self.reader.is_dead()):
            raise GameStatusEror("泼街了，准备复活。")
        

    def killTreeBoss(self):
        mc = self.mc
        
        mc.move_right(1.2)
        time.sleep(.1)

        mc.move_top(.6)
        time.sleep(.1)

        mc.move_right(.6)
        time.sleep(3)



    def killBullBoos(self):
        mc = self.mc
        
        mc.move_top(5)
        time.sleep(.1)

        mc.move_right(.8)
        time.sleep(.1)

        mc.move_top(3.2)
        time.sleep(.1)

        mc.move_left(2.1)
        time.sleep(4)

        mc.move_top(6.4)
        time.sleep(4)
