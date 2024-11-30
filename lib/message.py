
from twilio.rest import Client

from lib import logger

# 消息推送服务
class MessageService:
    # 初始化
    def __init__(self, config):
        self.account_sid = config["TWILIO"]["AccountSid"]
        self.auth_token = config["TWILIO"]["AuthToken"]
        self.twilio_number = config["TWILIO"]["PhoneNumber"]
        self.to_number = config["TWILIO"]["ToNumber"]
        self.app_name = config["APP"]["Name"]
        self.logger = logger.init_logger(config)
        self.is_enable = config.getboolean('TWILIO', 'IsEnable')
    
    # 发短信
    def push(self, message):
        # 如果不允许，就不运行
        if(not self.is_enable): 
            self.logger.debug(f"[twilio] 已被禁止使用")
            return

        # 创建客户端
        client = Client(self.account_sid, self.auth_token)

        # 发送短信
        message = client.messages.create(
            body = f"\n{message}",  # 短信内容
            from_ = self.twilio_number,
            to = self.to_number,
        )
        self.logger.debug(f"[twilio]短信已发送, SID是: {message.sid}")