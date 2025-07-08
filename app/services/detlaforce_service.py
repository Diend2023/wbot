import requests
from datetime import datetime
from flask import current_app

class DetlaforceService:
    def __init__(self):
        self.ovd_data_url = "https://wapi.wanqifan.top/delta_force/ovd_data"
        self.map_key_to_cn = {
            'db': '零号大坝',
            'cgxg': '长弓溪谷',
            'bks': '巴克什',
            'htjd': '航天基地',
            'cxjy': '潮汐监狱'
        }

    def _get_ovd_data(self):
        """获取OVD数据"""
        try:
            response = requests.get(self.ovd_data_url).json()
            if not response or 'data' not in response or 'bdData' not in response['data']:
                return "获取失败，数据格式不正确或数据为空"
            return response
        except Exception as e:
            current_app.logger.error("get_ovd_data 出错:", e)
            return f"获取失败：{e}"

    def get_map_password(self):
        """获取地图密码"""
        try:
            ovd_data = self._get_ovd_data()
            if not ovd_data or 'data' not in ovd_data or 'bdData' not in ovd_data['data']:
                return "获取数据失败，数据格式不正确或数据为空"
            bdData = ovd_data['data']['bdData']
            lines = []
            for key, info in bdData.items():
                cn_name = self.map_key_to_cn.get(key, key.upper())
                raw_time = info['updated']
                dt = datetime.strptime(raw_time, "%Y%m%d%H%M%S")
                formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                block = f"{cn_name}\n密码：{info['password']}\n更新时间：{formatted_time}"
                lines.append(block)
            return "\n" + "\n\n".join(lines)
        except Exception as e:
            current_app.logger.error("get_map_password 出错:", e)
            return f"获取失败：{e}"

    def get_products_recommendation(self):
        """获取产物推荐"""
        try:
            ovd_data = self._get_ovd_data()
            if not ovd_data or 'data' not in ovd_data or 'spData' not in ovd_data['data']:
                return "获取失败，数据格式不正确或数据为空"
            spData = ovd_data['data']['spData']
            lines = []
            for key, info in spData.items():
                placeName = info['placeName']
                item_name = info['itemName']
                profit = int(info['profit'])
                yesterdayHighestPrice = int(info['yesterdayHighestPrice'])
                yesterdayHighestTime = info['yesterdayHighestTime']
                block = f"{placeName}\n产物名称：{item_name}\n当前利润：{profit}\n建议售价：{yesterdayHighestPrice}\n出售时间：{yesterdayHighestTime}"
                lines.append(block)
            return "\n" + "\n\n".join(lines)
        except Exception as e:
            current_app.logger.error("get_product_recommendation 出错:", e)
            return f"获取失败：{e}"
        
    def get_activity_products(self):
        """获取活动物品"""
        try:
            ovd_data = self._get_ovd_data()
            if not ovd_data or 'data' not in ovd_data or 'ariiData' not in ovd_data['data']:
                return "获取失败，数据格式不正确或数据为空"
            ariiData = ovd_data['data']['ariiData']
            lines = []
            for info in ariiData:
                activityName = info['activityName']
                activityTime = info['activityTime']
                itemName = info['itemName']
                currectPrice = int(info['currectPrice'])
                activitySuggestedPrice = int(info['activitySuggestedPrice'])
                block = f"{activityName}\n活动时间：{activityTime}\n物品名称：{itemName}\n当前价格：{currectPrice}\n建议售价：{activitySuggestedPrice}"
                lines.append(block)
            return "\n" + "\n\n".join(lines)
        except Exception as e:
            current_app.logger.error("get_activity_product 出错:", e)
            return f"获取失败：{e}"

    def get_high_price_products(self):
        """获取高价浮动材料"""
        try:
            ovd_data = self._get_ovd_data()
            if not ovd_data or 'data' not in ovd_data or 'smpData' not in ovd_data['data']:
                return "获取失败，数据格式不正确或数据为空"
            smpData = ovd_data['data']['smpData']
            lines = []
            for info in smpData:
                itemName = info['itemName']
                currectPrice = int(info['currectPrice'])
                yesterdayHighestPrice = int(info['yesterdayHighestPrice'])
                yesterdayHighestTime = info['yesterdayHighestTime']
                yesterdayLowestPrice = int(info['yesterdayLowestPrice'])
                yesterdayLowestTime = info['yesterdayLowestTime']
                block = f"{itemName}\n当前价格：{currectPrice}\n最高价格：{yesterdayHighestPrice}\n高价时间：{yesterdayHighestTime}\n最低价格：{yesterdayLowestPrice}\n低价时间：{yesterdayLowestTime}"
                lines.append(block)
            return "\n" + "\n\n".join(lines)
        except Exception as e:
            current_app.logger.error("get_high_price_product 出错:", e)
            return f"获取失败：{e}"
        
    def get_hot_bullets(self):
        """获取热门子弹"""
        try:
            ovd_data = self._get_ovd_data()
            if not ovd_data or 'data' not in ovd_data or 'hapData' not in ovd_data['data']:
                return "获取失败，数据格式不正确或数据为空"
            hapData = ovd_data['data']['hapData']
            lines = []
            for info in hapData:
                objectName = info['objectName']
                block = f"{objectName}"
                lines.append(block)
            return "\n" + "\n".join(lines)
        except Exception as e:
            current_app.logger.error("get_hot_bullets 出错:", e)
            return f"获取失败：{e}"
        
    def get_bullets_profit(self):
        """获取子弹利润"""
        try:
            ovd_data = self._get_ovd_data()
            if not ovd_data or 'data' not in ovd_data or 'dtaData' not in ovd_data['data']:
                return "获取失败，数据格式不正确或数据为空"
            dtaData = ovd_data['data']['dtaData']
            lines = []
            for info in dtaData:
                itemName = info['itemName']
                profit = int(info['profit'])
                block = f"{itemName}\n利润：{profit}"
                lines.append(block)
            return "\n" + "\n\n".join(lines)
        except Exception as e:
            current_app.logger.error("get_bullets_profit 出错:", e)
            return f"获取失败：{e}"