import time
from exception.game_status import GameStatusError
from lib.info_reader import InfoReader
from lib.move_controller import MoveControll


class TwoCentipede:
    
    def __init__(self, config):
        self.config = config
        self.mc = MoveControll(config)
        self.reader = InfoReader(config)


    def check_handle(self):
        if(self.reader.is_dead()):
            raise GameStatusError("泼街了，准备复活。")

    # 移动到boss前面
    def move_to_front_of_BOSS(self):
        mc = self.mc

        self.check_handle()
        mc.move_right_down(5)
        time.sleep(.1)

        mc.move_right_top(5.6)

