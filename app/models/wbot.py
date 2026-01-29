import requests
import json
import logging
from typing import Dict, Any, Optional


class NapCatBot:
    """NapCat机器人核心类"""

    def __init__(self, host: str, token: str = None, logger: logging.Logger = None, qq: str = None, modes: Optional[Dict[str, Any]] = None):
        """
        初始化机器人
        :param host: NapCat服务地址
        :param token: 访问令牌
        :param logger: 日志记录器
        """
        self.host = host.rstrip('/')
        self.token = token
        self.qq = qq
        self.logger = logger or logging.getLogger(__name__)
        self.modes = modes
        self.headers = {
            'Content-Type': 'application/json'
        }
        if self.token:
            self.headers['Authorization'] = f'Bearer {self.token}'

    def send_group_message(self, group_id: str, message: list) -> Dict[str, Any]:
        """发送群聊消息，message为消息内容列表"""
        url = f"{self.host}/send_group_msg"
        data = {
            "group_id": group_id,
            "message": message,
        }
        try:
            response = requests.post(
                url, json=data, headers=self.headers, timeout=10)
            return response.json()
        except Exception as e:
            self.logger.error(f"发送群消息失败: {e}")
            return {"status": "error", "message": str(e)}

    def send_group_message_text(self, group_id: str, user_id: str, text: str) -> Dict[str, Any]:
        """发送群聊文本消息"""
        url = f"{self.host}/send_group_msg"
        message_data = []
        if user_id:
            message_data.append({
                "type": "at",
                "data": {
                    "qq": user_id,
                }
            })
            message_data.append({
                "type": "text",
                "data": {
                    "text": " "
                }
            })
        message_data.append({
            "type": "text",
            "data": {
                "text": f"{text}"
            }
        })
        data = {
            "group_id": group_id,
            "message": message_data,
        }
        try:
            response = requests.post(
                url, json=data, headers=self.headers, timeout=10)
            if response.json().get('status') != 'ok':
                self.logger.error(f"发送群消息失败: {response.json()}")
            return response.json()
        except Exception as e:
            self.logger.error(f"发送群消息失败: {e}")
            return {"status": "error", "message": str(e)}

    def send_group_message_image(self, group_id: str, user_id: str, image_list: list) -> Dict[str, Any]:
        """发送群聊图片消息，图片必须自带协议"""
        url = f"{self.host}/send_group_msg"
        message_data = []
        if user_id:
            message_data.append({
                "type": "at",
                "data": {
                    "qq": user_id,
                }
            })
        for image in image_list:
            if isinstance(image, str):
                message_data.append({
                    "type": "image",
                    "data": {
                        "file": image
                    }
                })
            else:
                self.logger.error(f"无效的图片格式: {image}")
                return {"status": "error", "message": "无效的图片格式"}
        data = {
            "group_id": group_id,
            "message": message_data,
        }
        try:
            response = requests.post(
                url, json=data, headers=self.headers, timeout=10)
            return response.json()
        except Exception as e:
            self.logger.error(f"发送群图片失败: {e}")
            return {"status": "error", "message": str(e)}

    def send_group_message_image_text(self, group_id: str, user_id: str, image_list: list, text: str) -> Dict[str, Any]:
        """发送群聊图片+文字消息，图片必须自带协议"""
        url = f"{self.host}/send_group_msg"
        message_data = []
        if user_id:
            message_data.append({
                "type": "at",
                "data": {
                    "qq": user_id,
                }
            })
        for image in image_list:
            if isinstance(image, str):
                message_data.append({
                    "type": "image",
                    "data": {
                        "file": image
                    }
                })
            else:
                self.logger.error(f"无效的图片格式: {image}")
                return {"status": "error", "message": "无效的图片格式"}
        message_data.append({
            "type": "text",
            "data": {
                "text": f"{text}"
            }
        })
        data = {
            "group_id": group_id,
            "message": message_data,
        }
        try:
            response = requests.post(
                url, json=data, headers=self.headers, timeout=10)
            return response.json()
        except Exception as e:
            self.logger.error(f"发送群图片+文字失败: {e}")
            return {"status": "error", "message": str(e)}

    def send_group_message_text_image(self, group_id: str, user_id: str, text: str, image_list: list) -> Dict[str, Any]:
        """发送群聊文本+图片消息，图片必须自带协议"""
        url = f"{self.host}/send_group_msg"
        message_data = []
        if user_id:
            message_data.append({
                "type": "at",
                "data": {
                    "qq": user_id,
                }
            })
            message_data.append({
                "type": "text",
                "data": {
                    "text": " "
                }
            })
        message_data.append({
            "type": "text",
            "data": {
                "text": f"{text}"
            }
        })
        for image in image_list:
            if isinstance(image, str):
                message_data.append({
                    "type": "image",
                    "data": {
                        "file": image
                    }
                })
            else:
                self.logger.error(f"无效的图片格式: {image}")
                return {"status": "error", "message": "无效的图片格式"}
        data = {
            "group_id": group_id,
            "message": message_data,
        }
        try:
            response = requests.post(
                url, json=data, headers=self.headers, timeout=10)
            return response.json()
        except Exception as e:
            self.logger.error(f"获取群列表失败: {e}")
            return {"status": "error", "message": str(e)}

    def send_group_message_json(self, group_id: str, data: dict) -> Dict[str, Any]:
        """发送群聊JSON消息"""
        url = f"{self.host}/send_group_msg"
        data = {
            "group_id": group_id,
            "message": {
                "type": "json",
                "data": {
                    "data": data
                }
            },
        }
        try:
            response = requests.post(
                url, json=data, headers=self.headers, timeout=10)
            return response.json()
        except Exception as e:
            self.logger.error(f"发送群聊JSON消息失败: {e}")
            return {"status": "error", "message": str(e)}

    def send_group_message_record(self, group_id: str, record: str) -> Dict[str, Any]:
        """发送群聊音频消息，音频文件必须自带协议"""
        url = f"{self.host}/send_group_msg"
        data = {
            "group_id": group_id,
            "message": {
                "type": "record",
                "data": {
                    "file": record,
                }
            },
        }
        try:
            response = requests.post(
                url, json=data, headers=self.headers)
            return response.json()
        except Exception as e:
            self.logger.error(f"发送群聊音频消息失败: {e}")
            return {"status": "error", "message": str(e)}

    def set_message_emoji_like(self, message_id: str, emoji_id: str) -> Dict[str, Any]:
        """设置消息表情点赞"""
        url = f"{self.host}/set_msg_emoji_like"
        data = {
            "message_id": message_id,
            "emoji_id": emoji_id
        }
        try:
            response = requests.post(
                url, json=data, headers=self.headers)
            return response.json()
        except Exception as e:
            self.logger.error(f"设置消息表情点赞失败: {e}")
            return {"status": "error", "message": str(e)}
        
    def get_group_info(self, group_id: str) -> Dict[str, Any]:
        """获取群信息"""
        url = f"{self.host}/get_group_info"
        params = {
            "group_id": group_id
        }
        try:
            response = requests.get(
                url, params=params, headers=self.headers)
            return response.json()
        except Exception as e:
            self.logger.error(f"获取群信息失败: {e}")
            return {"status": "error", "message": str(e)}