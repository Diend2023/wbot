from flask import Blueprint, request, jsonify, current_app

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    """接收NapCat的消息回调"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"status": "error", "message": "无效的JSON数据"}), 400
        
        post_type = data.get('post_type')
        
        if post_type == 'message':
            current_app.message_handler.handle_message(data)
        elif post_type == 'notice':
            # 处理通知事件（如群成员变动等）
            current_app.logger.info(f"收到通知: {data}")
        elif post_type == 'request':
            # 处理请求事件（如加好友请求等）
            current_app.logger.info(f"收到请求: {data}")
        
        return jsonify({"status": "ok"})
        
    except Exception as e:
        current_app.logger.error(f"处理webhook失败: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@webhook_bp.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "bot_name": current_app.config['BOT_NAME']
    })