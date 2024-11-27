
import time
from instance import GameStatusError
from lib import MoveControll


class FrontFlatland:
    mc = MoveControll()

    def check_handle(self):
        if(self.reader.is_dead()):
            raise GameStatusError("泼街了，准备复活。")
        

    def killBoss(self):
        mc = self.mc
        
        mc.move_right(.3)
        time.sleep(.1)

        mc.move_top(2.4)
        time.sleep(.1)
        
        mc.move_left(.6)
        time.sleep(.1)

        mc.move_top(1.6)
        time.sleep(.1)



