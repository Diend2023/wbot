import requests
import os
import json
import time
import random
from typing import Dict, Any
from flask import current_app

class YRZSService:
    """YRZS服务管理器"""

    def __init__(self):
        self.yrzs_backend_base = "https://backend.1rzs.com"

    def query_profile_by_name(self, name: str) -> Dict[str, Any]:
        """根据用户名查询用户信息"""
        url = f"{self.yrzs_backend_base}/api/user/{name}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                profile = data.get("data", {})
                print(profile)
                if not profile:
                    return {"status": "error", "message": "未找到用户信息"}
                if profile.get("userVO"):
                    return {"status": "success", "message": f"\nid: {profile['userVO']['uid']}\nname: {profile['login']['name']}\nonlineMode: {profile['login']['onlineMode']}\nemail: {profile['userVO']['email']}\nisAdmin: {profile['userVO']['isAdmin']}\ncreateTime: {profile['userVO']['createTime']}\nupdateTime: {profile['userVO']['updateTime']}"}
                else:
                    return {"status": "error", "message": f"\n该用户有数据但是无账号？？？\nname: {profile['login']['name']}\nonlineMode: {profile['login']['onlineMode']}"}
            else:
                current_app.logger.error(f"请求失败，状态码: {response.status_code}")
                return {"status": "error", "message": f"请求失败，状态码: {response.status_code}"}
        except Exception as e:
            current_app.logger.error(f"请求异常: {e}")
            return {"status": "error", "message": f"请求异常: {e}"}
        

    def query_profile_by_qq(self, qq: str) -> Dict[str, Any]:
        """根据QQ号查询用户信息"""
        url = f"{self.yrzs_backend_base}/api/user/{qq}@qq.com"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                profile = data.get("data", {})
                if not profile:
                    return {"status": "error", "message": "未找到用户信息\n只有使用QQ邮箱注册的用户才能使用#qq查询"}
                if profile.get("login"):
                    return {"status": "success", "message": f"\nid: {profile['userVO']['uid']}\nname: {profile['login']['name']}\nonlineMode: {profile['login']['onlineMode']}\nemail: {profile['userVO']['email']}\nisAdmin: {profile['userVO']['isAdmin']}\ncreateTime: {profile['userVO']['createTime']}\nupdateTime: {profile['userVO']['updateTime']}\n只有使用QQ邮箱注册的用户才能使用#qq查询"}
                else:
                    return {"status": "error", "message": f"该用户已注册但是未绑定，详情请看https://www.1rzs.com/profile/{profile['userVO']['uid']}\n只有使用QQ邮箱注册的用户才能使用#qq查询"}
            else:
                return {"status": "error", "message": f"请求失败，状态码: {response.status_code}\n只有使用QQ邮箱注册的用户才能使用#qq查询"}
        except Exception as e:
            return {"status": "error", "message": f"请求异常: {e}\n只有使用QQ邮箱注册的用户才能使用#qq查询"}

    def query_profile_by_uid(self, uid: int) -> Dict[str, Any]:
        """根据UID查询用户信息"""
        url = f"{self.yrzs_backend_base}/user/get/user/{uid}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                profile = data.get("data", {})
                if not profile:
                    return {"status": "error", "message": "未找到用户信息"}
                return {"status": "success", "message": f"\nid: {profile['userVO']['uid']}\nname: {profile['login']['name']}\nonlineMode: {profile['login']['onlineMode']}\nemail: {profile['userVO']['email']}\nisAdmin: {profile['userVO']['isAdmin']}\ncreateTime: {profile['userVO']['createTime']}\nupdateTime: {profile['userVO']['updateTime']}"}
            else:
                return {"status": "error", "message": f"请求失败，状态码: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": f"请求异常: {e}"}


# class YRZSService:
#     """YRZS服务管理器"""

#     def __init__(self):
#         self.yrzs_backend_base = "https://backend.1rzs.com"
#         self.profile_file = os.path.join(current_app.config.get('STATIC_FOLDER'), 'yrzs', 'profile_list.json')
#         self.profile_list = self._load_profile_list()

#     def _load_profile_list(self) -> Dict[str, Any]:
#         """加载用户信息"""
#         if not os.path.exists(self.profile_file):
#             return {}
#         with open(self.profile_file, 'r', encoding='utf-8') as f:
#             return json.load(f)

#     def _get_profile(self, id: int) -> Dict[str, Any]:
#         """获取用户信息"""
#         time.sleep(random.uniform(10, 30))  # 避免请求过于频繁
#         try:
#             response = requests.get(f"{self.yrzs_backend_base}/user/get/user/{id}")
#             if response.status_code == 200:
#                 return response.json()
#             else:
#                 current_app.logger.error(f"请求失败，状态码: {response.status_code}")
#                 return {"status": "error", "message": f"请求失败，状态码: {response.status_code}"}
#         except Exception as e:
#             current_app.logger.error(f"请求异常: {e}")
#             return {"status": "error", "message": f"请求异常: {e}"}
    
#     def _save_profile_list(self, data: Dict[str, Any]) -> None:
#         """保存用户信息到文件"""
#         with open(self.profile_file, 'w', encoding='utf-8') as f:
#             json.dump(data, f, ensure_ascii=False, indent=4)

#     def update_profile_list(self, start_id: int = 1, profile_list: list = None, retry_count: int = 0) -> Dict[str, Any]:
#         """更新用户信息"""
#         if profile_list is None:
#             profile_list = []
#         update_time = self.profile_list.get("update_time", "2023-10-01T12:00:00Z")
#         # 每天只能更新一次
#         if start_id == 1 and time.strftime("%Y-%m-%d", time.gmtime()) == update_time.split("T")[0]:
#             current_app.logger.info("今天已经更新过用户信息")
#             return {"status": "failed", "message": "今天已经更新过用户信息"}
        
#         max_retries = 5
#         if retry_count >= max_retries:
#             current_app.logger.error(f"达到最大重试次数 {max_retries}，停止更新。当前ID: {start_id}")
#             if profile_list:
#                 self._save_profile_list({"update_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "data": profile_list})
#                 self.profile_list = self._load_profile_list()  # 更新内存中的profile_list
#                 current_app.logger.info(f"查询信息更新成功，当前ID: {id}, 用户数量: {len(profile_list)}，重试次数: {retry_count}")
#                 return {"status": "success", "message": "查询信息更新成功"}
#             return {"status": "error", "message": "没有获取到任何用户信息，更新失败"}
#         try:
#             id = start_id
#             while True:
#                 data = self._get_profile(id)
#                 if data.get("status") == "error":
#                     return self.update_profile_list(start_id=id, profile_list=profile_list, retry_count=retry_count + 1)
#                 if data.get("data"):
#                     profile = {
#                         "id": id,
#                         "login": data["data"].get("login"),
#                         "userVO": data["data"].get("userVO"),
#                     }
#                     profile_list.append(profile)
#                 elif data.get("data") is None:
#                     break
#                 id += 1
#             self._save_profile_list({"update_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "data": profile_list})
#             self.profile_list = self._load_profile_list()  # 更新内存中的profile_list
#             current_app.logger.info(f"查询信息更新成功，当前ID: {id}, 用户数量: {len(profile_list)}，重试次数: {retry_count}")
#             return {"status": "success", "message": "查询信息更新成功"}
#         except Exception as e:
#             current_app.logger.error(f"更新用户信息失败: {e}")
#             return {"status": "error", "message": f"更新用户信息失败: {e}"}
        
#     def query_profile_by_name(self, name: str) -> Dict[str, Any]:
#         """根据用户名查询用户信息"""
#         update_time = self.profile_list.get("update_time", "2023-10-01T12:00:00Z")
#         for profile in self.profile_list.get("data", []):
#             if profile.get("login", {}) and profile.get("login", {}).get("name") == name:
#                 return {"status": "success", "message": f"\nid: {profile['login']['id']}\nname: {profile['login']['name']}\nonlineMode: {profile['login']['onlineMode']}\nemail: {profile['userVO']['email']}\nisAdmin: {profile['userVO']['isAdmin']}\ncreateTime: {profile['userVO']['createTime']}\nupdateTime: {profile['userVO']['updateTime']}\n该数据不一定准确，更新时间: {update_time}"}
#         return {"status": "error", "message": "未找到用户信息，数据更新时间: " + update_time}
    
#     def query_profile_by_qq(self, qq: str) -> Dict[str, Any]:
#         """根据QQ号查询用户信息"""
#         update_time = self.profile_list.get("update_time", "2023-10-01T12:00:00Z")
#         for profile in self.profile_list.get("data", []):
#             if profile.get("userVO", {}).get("email").endswith("@qq.com") and profile.get("userVO", {}).get("email").startswith(qq):
#                 if profile.get("login"):
#                     return {"status": "success", "message": f"\nid: {profile['login']['id']}\nname: {profile['login']['name']}\nonlineMode: {profile['login']['onlineMode']}\nemail: {profile['userVO']['email']}\nisAdmin: {profile['userVO']['isAdmin']}\ncreateTime: {profile['userVO']['createTime']}\nupdateTime: {profile['userVO']['updateTime']}\n该数据不一定准确，更新时间: {update_time}"}
#                 else:
#                     return {"status": "error", "message": f"该用户未绑定，数据更新时间: {update_time}"}
#         return {"status": "error", "message": "未找到用户信息，数据更新时间: " + update_time}