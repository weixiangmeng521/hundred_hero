
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

        mc.move_top(4)
        time.sleep(.1)

        # back
        def lamada():
            mc.move_down(4)
            mc.move_left(.3)
        return lamada

        


