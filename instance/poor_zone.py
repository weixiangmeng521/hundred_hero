import time
from exception.game_status import GameStatusError
from lib.move_controller import MoveControll
from lib.visual_track import VisualTrack

class PoorZone:
    
    def __init__(self, config):
        self.config = config
        self.mc = MoveControll(config)
        self.vt = VisualTrack(config)

    def check_handle(self):
        if(self.reader.is_dead()):
            raise GameStatusError("泼街了，准备复活。")
        
    # 杀树精boss
    def killTreeBoss(self):
        mc = self.mc
        
        mc.move_right(1.2)

        mc.move_top(.6)

        mc.move_right(.2)
        time.sleep(1)
        
        # back
        def lamda():
            mc.move_left(.2)
            mc.move_down(.6)
            mc.move_left(1.2)
        return lamda


    # 杀牛魔王boss
    def killBullBoos(self):
        mc = self.mc
        
        mc.move_top(4)

        mc.move_right(.5)

        mc.move_top(3.8)

        mc.move_left(1.8)
        time.sleep(1)

        mc.move_top(5.6)
        time.sleep(1)

        # 去最近的传送点
        def lamb():
            mc.move_top(1.2)
            mc.move_right_top(2.1)
            mc.move_top(.7)
            mc.move_left(1.6)
            # 精准找到传送台
        return lamb
    

    # 移动到传送台
    def move_2_port(self):
        x, y, tx, ty = self.vt.find_position((121, 236, 239), 15, 15)
        self.mc.move(x, y, tx, ty)
        time.sleep(.3)