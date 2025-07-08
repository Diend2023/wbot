# app/__init__.py
from flask import Flask
from app.config import Config
from app.utils.logger import setup_logger

def create_app():
    """Flask应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 设置日志
    setup_logger(app)
    
    # 在应用上下文中初始化服务
    with app.app_context():
        from app.services.chat_service import ChatService
        from app.services.ping_service import PingService
        from app.services.card_service import CardService
        from app.services.mcbot_service import McBotService
        from app.services.detlaforce_service import DetlaforceService
        from app.services.yrzs_service import YRZSService
        from app.handlers.message import MessageHandler
        
        # 创建服务实例并存储到app中
        app.chat_service = ChatService()
        app.ping_service = PingService()
        app.card_service = CardService()
        app.mcbot_service = McBotService()
        app.detlaforce_service = DetlaforceService()
        app.yrzs_service = YRZSService()
        app.message_handler = MessageHandler()

    # 注册蓝图
    from app.routes.webhook import webhook_bp
    from app.routes.api import api_bp
    app.register_blueprint(webhook_bp)
    app.register_blueprint(api_bp)

    return app