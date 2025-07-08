import os
import json
from dotenv import load_dotenv

load_dotenv()


class Config:
    """配置类"""
    # Flask配置
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

    # NapCat配置
    NAPCAT_HOST = os.environ.get('NAPCAT_HOST', 'http://localhost:3000')
    NAPCAT_TOKEN = os.environ.get('NAPCAT_TOKEN', '')

    # 机器人配置
    BOT_NAME = os.environ.get('BOT_NAME', 'WBot')
    BOT_QQ = os.environ.get('BOT_QQ', '')  # 机器人QQ号
    ADMIN_QQ = os.environ.get('ADMIN_QQ', '')  # 管理员QQ号

    # 服务器配置
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5555))

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_FOLDER = os.path.join(BASE_DIR, 'static')

    MODES = {
        'private': {
            'chat': {
                'enable': True,
                'model': 'gpt',
            },
            'voice': {
                'enable': False,
            },
        },
        'group': {
            'chat': {
                'enable': True,
                'model': 'gpt',
            },
            'voice': {
                'enable': False,
            },
        },
    }

    SEND_EMOJI_LIST = json.loads(os.environ.get('SEND_EMOJI_LIST', '[]'))

    # AI设置
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL', 'https://api.qqslyx.com/v1')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')
    DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
    DEEPSEEK_BASE_URL = os.environ.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')
    DEEPSEEK_MODEL = os.environ.get('DEEPSEEK_MODEL', 'deepseek-chat')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    GEMINI_BASE_URL = os.environ.get('GEMINI_BASE_URL', 'https://gemini.wanqifan.top')
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash-preview')
