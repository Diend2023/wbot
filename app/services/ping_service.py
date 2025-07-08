import requests
from flask import current_app


class PingService():
    """ping服务管理器"""

    def __init__(self):
        self.mc_ping_server = "https://wapi.wanqifan.top/minecraft/server/"

    def mc_ping(self, mc_server_domain: str) -> tuple[str, list]:
        """获取Minecraft服务器状态"""
        try:
            response = requests.get(
                url=self.mc_ping_server + mc_server_domain).json()
            if response.get("data"):
                if response.get("data").get("java_status"):
                    java_status = response.get("data").get("java_status")
                    if not java_status.get('online'):
                        return f"\n地址: {mc_server_domain}\n在线状态: {java_status.get('online')}\nerror: {java_status.get('error', '')}", []
                    return f"\n地址: {mc_server_domain}\n延迟: {java_status.get('latency')}\n在线状态: {java_status.get('online')}\n玩家数量: {java_status.get('players', {}).get('online')} / {java_status.get('players', {}).get('max')}\n游戏版本: {java_status.get('version').get('name')}", [java_status.get('favicon', None)]

        except Exception as e:
            current_app.logger.error(f"获取Minecraft服务器状态失败: {e}")
            return f"获取Minecraft服务器状态失败: {e}", []
