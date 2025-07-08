import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(app):
    """设置日志"""
    if not app.debug:
        # 创建logs目录
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # 设置文件日志
        file_handler = RotatingFileHandler(
            'logs/wbot.log', 
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('WBot startup')