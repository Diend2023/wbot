import requests
import csv
import os
from flask import current_app

class CardService:
    """卡片服务管理器"""

    def __init__(self):
        """初始化卡片服务"""
        self.music_card_api = "https://oiapi.net/API/QQMusicJSONArk"
        self.records_url = "https://wanqifan.blob.core.windows.net/records/"
        self.records_file = os.path.join(current_app.config.get('STATIC_FOLDER'), 'ar_records', 'records_list.csv')
        self.records = self._load_records()

    def _load_records(self) -> list:
        """加载唱片"""
        records = []
        try:
            with open(self.records_file, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    records.append(row)
        except Exception as e:
            print(f"加载唱片失败: {e}")
        return records

    def get_record_card(self, num: str) -> dict:
        """获取唱片卡片"""
        record = next((r for r in self.records if r.get('num') == num), None)
        if not record:
            return {"status": "error", "message": "唱片不存在"}

        url = f"{self.records_url}{num}.ogg"
        singer = record.get('content', '')
        cover = f"{self.records_url}{num}.png"
        jump = url

        data = {
            "url": url,
            "song": f"唱片{num}",
            "singer": singer,
            "cover": cover,
            "jump": jump,
            "format": "mihoyo"
        }
        try:
            response = requests.get(f"{self.music_card_api}/?url={url}&song={data['song']}&singer={singer}&cover={cover}&jump={jump}&format={data['format']}")
            if response.status_code == 200:
                res_data = response.json()
                if res_data.get('code') == 1:
                    data = res_data.get('data', {})
                else:
                    return {"status": False, "message": "获取唱片卡片失败"}
            else:
                return {"status": False, "message": f"请求失败，状态码: {response.status_code}"}
        except Exception as e:
            return {"status": False, "message": f"请求异常: {e}"}
        return {"status": True, "data": data, "record_url": url}