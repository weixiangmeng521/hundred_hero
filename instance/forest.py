from exception.game_status import GameStatusError
import time
from lib.info_reader import InfoReader
from lib.move_controller import MoveControll


class RottenSwamp:

    def __init__ (self, config):
        self.config = config
        self.mc = MoveControll(config)
        self.reader = InfoReader(config)
        

    def check_handle(self, should_check = True):
        if(not should_check):
            return
        isWoodFull, _ = self.reader.read_screen()
        if(isWoodFull): raise GameStatusError("木头满了")


    # 腐烂沼泽上圈
    def crossRoom1(self, should_check = True):
        mc = self.mc
        
        self.check_handle(should_check)
        mc.move_left_top(.6)
        time.sleep(3)

        self.check_handle(should_check)
        mc.move_right_top(1)
        time.sleep(3)

        self.check_handle(should_check)
        mc.move_left_top(.5)
        time.sleep(.1)
        
        self.check_handle(should_check)
        mc.move_right_top(.6)
        time.sleep(3)      
        
        self.check_handle(should_check)
        mc.move_left_top(1)
        time.sleep(5)        
        
        self.check_handle(should_check)
        mc.move_right_top(.8)
        time.sleep(5)      
        
        self.check_handle(should_check)
        mc.move_left_top(.8)
        time.sleep(3)              
        
        self.check_handle(should_check)
        mc.move_right_top(1.6)
        time.sleep(3)              
        
        self.check_handle(should_check)
        mc.move_left_top(.3)
        time.sleep(1.)          
        
        self.check_handle(should_check)
        mc.move_right_top(1.2)
        time.sleep(3)              
        
        self.check_handle(should_check)
        mc.move_left_top(.3)
        time.sleep(.1)          
        
        self.check_handle(should_check)
        mc.move_right_top(.5)
        time.sleep(3)     
        
        self.check_handle(should_check)
        mc.move_left_top(.6)
        time.sleep(3)    
                
        self.check_handle(should_check)
        mc.move_right_top(1)
        time.sleep(3)            
        
        self.check_handle(should_check)
        mc.move_up(1)
        time.sleep(3) 
        
        self.check_handle(should_check)
        mc.move_up(.7)
        time.sleep(3)       
                
        self.check_handle(should_check)# 走弯路begin
        mc.move_right_top(2.6)
        time.sleep(3)            
        
        self.check_handle(should_check)
        mc.move_left_down(2.6)
        time.sleep(.1)            
        # 走弯路end
        
        self.check_handle(should_check)
        mc.move_up(1.5)
        time.sleep(3)       
        
        self.check_handle(should_check)
        mc.move_left(2.3)
        time.sleep(6)      
        
        self.check_handle(should_check)
        mc.move_left_down(1)
        time.sleep(3)     
        
        self.check_handle(should_check)
        mc.move_left_down(1.6)
        time.sleep(3)      
        
        self.check_handle(should_check)
        mc.move_down(1.6)
        time.sleep(3)      
        
        self.check_handle(should_check)
        mc.move_down(1.6)
        time.sleep(3)      
        
        self.check_handle(should_check)
        mc.move_right_down(2.6)
        time.sleep(3)    
        
        self.check_handle(should_check)
        mc.move_down(3.1)
        time.sleep(3)    


        # circle end
    
    # 腐烂沼泽下圈
    def crossRoom2(self, should_check = True):
        mc = self.mc
        
        self.check_handle(should_check)
        mc.move_left(2.6)
        time.sleep(3)

        # 走弯路 begin
        self.check_handle(should_check)
        mc.move_down(1)
        time.sleep(5)

        self.check_handle(should_check)
        mc.move_up(1)
        time.sleep(.1)
        # 走弯路 end

        self.check_handle(should_check)
        mc.move_left(2.6)
        time.sleep(3)

        self.check_handle(should_check)
        mc.move_left(1.7)
        time.sleep(3)

        self.check_handle(should_check)
        mc.move_left(1.7)
        time.sleep(8)

        self.check_handle(should_check)
        mc.move_right(4.6)
        time.sleep(5)

        self.check_handle(should_check)
        mc.move_up(2.4)
        time.sleep(5)

        self.check_handle(should_check)
        mc.move_right(2.5)
        time.sleep(5)

        self.check_handle(should_check)
        mc.move_right(1.5)
        time.sleep(5)

        self.check_handle(should_check)
        mc.move_down(2.3)
        time.sleep(3)
    

    # 污染前哨如圈前跑
    def crossRoom3Begin(self):
        mc = self.mc
        waitTime = 1.5

        mc.move_right(1.8)
        time.sleep(waitTime * 0)

        mc.move_down(.6)
        time.sleep(waitTime)

        mc.move_right(2.3)
        time.sleep(waitTime)



    # 污染前哨的循环圈
    def crossRoom3Loop(self):
        mc = self.mc
        waitTime = 3

        mc.move_up(1.2)
        time.sleep(waitTime)

        mc.move_left(1.4)
        time.sleep(waitTime)

        mc.move_up(2.3)
        time.sleep(waitTime)

        mc.move_up(1.3)
        time.sleep(waitTime)

        mc.move_right(1.3)
        time.sleep(waitTime)

        mc.move_up(1.3)
        time.sleep(waitTime)

        mc.move_right(2.3)
        time.sleep(waitTime)

        mc.move_right(.6)
        time.sleep(waitTime)

        mc.move_right_down(1.8)
        time.sleep(waitTime)

        mc.move_right(2.4)
        time.sleep(waitTime)

        mc.move_right_down(1.4)
        time.sleep(waitTime)

        mc.move_down(2.1)
        time.sleep(waitTime)

        mc.move_left(2.1)
        time.sleep(waitTime)        

        mc.move_down(1.1)
        time.sleep(waitTime)        

        mc.move_right(2.1)
        time.sleep(waitTime)        

        mc.move_down(2.1)
        time.sleep(waitTime)        

        mc.move_left(2.1)
        time.sleep(waitTime)      

        mc.move_left_top(2.1)
        time.sleep(waitTime)      

        mc.move_left_top(2.4)
        time.sleep(waitTime)      

        mc.move_up(2.4)
        time.sleep(waitTime)      

        mc.move_down(2.4)
        time.sleep(waitTime * 0)

        mc.move_left(2.1)
        time.sleep(waitTime)      

        mc.move_down(1.2)
        time.sleep(waitTime)      


    # 进入寒风营地
    def crossColdWindCamp(self):
        mc = self.mc
        waitTime = 1.5

        mc.move_right(1.8)
        time.sleep(waitTime * 0)

        mc.move_up(1.6)
        time.sleep(waitTime)

        mc.move_right(2.8)
        time.sleep(waitTime)

        mc.move_up(1.6)
        time.sleep(waitTime)

        mc.move_left(1.2)
        time.sleep(waitTime)

        mc.move_up(1.6)
        time.sleep(waitTime)

        mc.move_right(2.4)
        time.sleep(waitTime)

        mc.move_up(1.2)
        time.sleep(waitTime)

        mc.move_left(1.8)
        time.sleep(waitTime)

        mc.move_top(1.2)
        time.sleep(waitTime)

        mc.move_left(2.6)
        time.sleep(waitTime)

        mc.move_left_down(1.6)
        time.sleep(waitTime)

        mc.move_down(2)
        time.sleep(waitTime)

        mc.move_left(2)
        time.sleep(waitTime)

        mc.move_left(2.3)
        time.sleep(waitTime)


    # 打蜘蛛
    def killSpiderBoss(self):
        mc = self.mc

        mc.move_top(3.8)
        time.sleep(.1)

        mc.move_right(1.8)
        time.sleep(.1)

        mc.move_top(3.8)
        time.sleep(.1)

        mc.move_right(1.2)
        time.sleep(2)


    # 打树精
    def killTreeSprite(self):
        mc = self.mc

        mc.move_right(1.8)
        mc.move_up(1.2)
        mc.move_right(.3)
        time.sleep(.6)

        def lamda():
            mc.move_left(.3)
            mc.move_down(1.2)
            mc.move_left(1.6)
        return lamda

    # 打岩石巨人
    def killStoneMen(self):
        mc = self.mc

        mc.move_left(5.8)

        time.sleep(3)
        
        # 返回
        def lamda():
            mc.move_right(5.8)
        return lamda
    

    # 砍树
    def farmTree(self):
        mc = self.mc
        waitTime = 1.2

        mc.move_right(1.8)
        time.sleep(0)

        mc.move_down(.6)
        time.sleep(0)

        mc.move_right(2.3)
        time.sleep(waitTime * 5)

        mc.move_left(.3)
        time.sleep(waitTime * 5)

        mc.move_top(1.2)
        time.sleep(waitTime * 5)

        mc.move_down(1.2)
        time.sleep(0)

        mc.move_left(2.3)
        time.sleep(0)

        mc.move_down(.8)
        time.sleep(waitTime * 5)

        mc.move_top(1.4)
        time.sleep(0)       

        mc.move_left(1.5)
        time.sleep(0)   