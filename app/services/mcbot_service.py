import requests
from typing import Dict, Any
from flask import current_app

class McBotService:
    """Minecraft Bot服务"""

    def __init__(self):
        self.host = "http://119.91.220.130:25564"

    def send_message(self, sender: Dict[str, Any], message: str) -> None:
        """发送消息"""
        url = f"{self.host}/mcbot/chat"
        message = message.replace('\n', ' ').replace('\r', ' ').strip()
        name = sender.get("card", "")
        if not name:
            name = sender.get("nickname", "???")
        message = "[群] " + name + " > " + message
        data = {"message": message}
        try:
            response = requests.post(url, json=data)
            if response.json().get("success") == False:
                return "消息发送失败"
            else:
                current_app.logger.info(f"消息发送成功: {response.text}")
        except Exception as e:
            current_app.logger.error(f"发送消息失败: {e}")

    def get_player_list(self) -> str:
        """获取玩家列表"""
        url = f"{self.host}/mcbot/players"
        try:
            response = requests.get(url)
            if (response.json().get("success")):
                current_app.logger.info(f"获取玩家列表成功: {response.text}")
                return "\n" + response.json().get("data", {}).get("playerList", "")
            current_app.logger.warning(f"获取玩家列表失败: {response.text}")
            return response.json().get("message", "获取玩家列表失败")
        except Exception as e:
            current_app.logger.error(f"获取玩家列表失败: {e}")
            return "获取玩家列表失败"

    def get_tps(self) -> str:
        """获取TPS"""
        url = f"{self.host}/mcbot/tps"
        try:
            response = requests.get(url)
            if (response.json().get("success")):
                current_app.logger.info(f"获取TPS成功: {response.text}")
                return "\n" + str(response.json().get("data", {}).get("tps", ""))
            current_app.logger.warning(f"获取TPS失败: {response.text}")
            return response.json().get("message", "获取TPS失败")
        except Exception as e:
            current_app.logger.error(f"获取TPS失败: {e}")
            return "获取TPS失败"