import requests

class ARService:
    """Arnetwork服务"""

    def __init__(self):
        self.host = "http://mc2026.cn"

    def get_location_offline(self, username: str) -> dict:
        """获取离线地址"""
        url = f"{self.host}:10/api/player-location?username={username}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                location_link = data.get("mc_link", "")
                uuid = data.get("offline_uuid", "")
                location = f"x：{data.get('world_location', {}).get('x', '')}，y：{data.get('world_location', {}).get('y', '')}，z：{data.get('world_location', {}).get('z', '')}"
                return {"offline_location_link": location_link, "uuid": uuid, "offline_location": location}
            else:
                return f"请求失败，状态码: {response.status_code}"
        except Exception as e:
            return f"请求异常: {e}"
        
    def get_location_online(self, username: str) -> dict:
        """获取在线地址"""
        url = f"{self.host}:10/api/player-location?username={username}&type=joins"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                location_link = data.get("mc_link", "")
                uuid = data.get("offline_uuid", "")
                location = f"x：{data.get('world_location', {}).get('x', '')}，y：{data.get('world_location', {}).get('y', '')}，z：{data.get('world_location', {}).get('z', '')}"
                return {"online_location_link": location_link, "uuid": uuid, "online_location": location}
            else:
                return f"请求失败，状态码: {response.status_code}"
        except Exception as e:
            return f"请求异常: {e}"
        
    def get_location(self, username: str) -> str:
        """获取地址"""
        offline_data = self.get_location_offline(username)
        online_data = self.get_location_online(username)

        result = f"玩家 {username}\n"
        result += f"UUID: {offline_data.get('uuid') if isinstance(offline_data, dict) and offline_data.get('uuid') else (online_data.get('uuid') if isinstance(online_data, dict) and online_data.get('uuid') else '未找到')}"

        if isinstance(offline_data, dict) or offline_data.get('offline_location_link') or offline_data.get('offline_location'):
            result += f"\n\n离线位置链接: {offline_data.get('offline_location_link')}\n"
            result += f"离线位置: {offline_data.get('offline_location')}"
        else:
            result += f"\n\n获取离线位置失败: {offline_data}\n"

        if isinstance(online_data, dict) or online_data.get('online_location_link') or online_data.get('online_location'):
            result += f"\n\n在线位置链接: {online_data.get('online_location_link')}\n"
            result += f"在线位置: {online_data.get('online_location')}"
        else:
            result += f"\n\n获取在线位置失败: {online_data}"

        return result
        