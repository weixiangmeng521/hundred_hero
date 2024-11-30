# 游戏状态的Error，比方说木头刷满了
class GameStatusError(Exception):

    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.error_info = ErrorInfo

    def __str__(self):
        return self.error_info
    
    def get_error_info(self):
        return self.error_info
        