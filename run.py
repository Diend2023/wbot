from app import create_app
from app.config import Config

app = create_app()

if __name__ == '__main__':
    print("=== WBot QQ机器人启动中 ===")
    print(f"Webhook地址: http://{Config.HOST}:{Config.PORT}/webhook")
    print("按 Ctrl+C 停止机器人")
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )