# 休息爆出的异常
class GameRestWarning(Exception):

    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.error_info = ErrorInfo

    def __str__(self):
        return self.error_info
    
    def get_error_info(self):
        return self.error_info
        