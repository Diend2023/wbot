from flask import Blueprint, request, jsonify, current_app

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/sendGroupMessage', methods=['POST'])
def sendGroupMessage():
    data = request.json
    group_id = data.get("groupId")
    user_id = data.get("userId")
    message = data.get("message")
    if not group_id or not message:
        return jsonify({"status": "error", "message": "缺少 groupId 或 message 参数"}), 400
    bot = current_app.message_handler.bot
    bot.send_group_message_text(group_id=group_id, user_id=user_id, text=message)
    return jsonify({"status": "success"})
