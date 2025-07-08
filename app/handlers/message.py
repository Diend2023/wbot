from flask import current_app
from app.models.wbot import NapCatBot
from app.handlers.commands import CommandHandler
from typing import Dict, Any


class MessageHandler:
    """消息处理器"""

    def __init__(self):
        self.bot = NapCatBot(
            host=current_app.config['NAPCAT_HOST'],
            token=current_app.config['NAPCAT_TOKEN'],
            qq=current_app.config['BOT_QQ'],
            logger=current_app.logger,
            modes=current_app.config.get('MODES', None)
        )
        self.send_emoji_list = current_app.config.get('SEND_EMOJI_LIST', [])
        self.command_handler = CommandHandler(self.bot)
        self.chat_service = current_app.chat_service
        self.ping_service = current_app.ping_service
        self.card_service = current_app.card_service
        self.mcbot_service = current_app.mcbot_service
        self.detlaforce_service = current_app.detlaforce_service
        self.yrzs_service = current_app.yrzs_service

    def handle_message(self, data: Dict[str, Any]) -> None:
        """总处理消息"""
        try:
            message_type = data.get('message_type')
            message_id = data.get('message_id', '')
            user_id = str(data.get('user_id', ''))
            group_id = str(data.get('group_id', '')
                           ) if message_type == 'group' else None
            message_body = data.get('message', '')
            sender = data.get('sender', {})
            # print(data)

            current_app.logger.info(
                f"收到消息 - 类型: {message_type}, 用户: {user_id}, "
                f"群组: {group_id}, 内容: {message_body}"
            )

            # 检查消息类型
            if message_type == 'private':
                # 私聊消息
                if not user_id:
                    current_app.logger.warning("私聊消息缺少用户ID")
                    return
                self._handle_private_message(
                    message_body=message_body, user_id=user_id, sender=sender)
            elif message_type == 'group':
                # 群聊消息
                if not group_id:
                    current_app.logger.warning("群聊消息缺少群聊ID")
                    return
                is_at, message_body = self._check_at(message_body)
                if is_at:
                    self._handle_group_at_message(
                    message_body=message_body, user_id=user_id, group_id=group_id, sender=sender, message_id=message_id)
                else:
                    self._handle_group_message(
                    message_body=message_body, user_id=user_id, group_id=group_id, sender=sender, message_id=message_id)
            else:
                current_app.logger.warning(
                    f"未知消息类型: {message_type}")
                return
        except Exception as e:
            current_app.logger.error(f"处理消息失败: {e}")

    def _handle_private_message(self, message_body: Dict[str, Any], user_id: str,
                                sender: Dict[str, Any]) -> None:
        """处理私聊消息"""
        pass

    def _handle_group_at_message(self, message_body: Dict[str, Any], user_id: str,
                              group_id: str, sender: Dict[str, Any], message_id: str) -> None:
        """处理群聊@消息"""
        for emoji in self.send_emoji_list:
            if emoji['user_id'] == user_id:
                self.bot.set_message_emoji_like(message_id, emoji['emoji_id'])
        message_text = self._get_message_text(message_body).strip()
        if message_text.startswith('test'):
            self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text="测试")
        elif message_text.startswith('/'):
            # 处理命令
            text = self.command_handler.handle_command(
                command=message_text, user_id=user_id, group_id=group_id, sender=sender)
            self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text=text)
        elif message_text.startswith('mcping'):
            # 处理ping命令
            mc_server_domain = message_text.split(' ')[1]
            text, image = self.ping_service.mc_ping(mc_server_domain)
            self.bot.send_group_message_text_image(group_id=group_id, user_id=user_id, text=text, image_list=image)
        elif message_text.startswith('唱片'):
            # 处理唱片卡片命令
            card_num = message_text.split(' ')[1] if len(message_text.split(' ')) > 1 else None
            response = self.card_service.get_record_card(num=card_num)
            if response.get("status"):
                data = response.get("data")
                record_url = response.get("record_url")
                self.bot.send_group_message_json(group_id=group_id, data=data)
                self.bot.send_group_message_record(group_id=group_id, record=record_url)
            else:
                self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text=response.get("message", "获取唱片卡片失败"))
        elif message_text == '今日密码':
            text = self.detlaforce_service.get_map_password()
            self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text=text)
        elif message_text == '产物推荐':
            text = self.detlaforce_service.get_products_recommendation()
            self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text=text)
        elif message_text == '活动物品':
            text = self.detlaforce_service.get_activity_products()
            self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text=text)
        elif message_text == '高价浮动材料':
            text = self.detlaforce_service.get_high_price_products()
            self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text=text)
        elif message_text == '热门子弹':
            text = self.detlaforce_service.get_hot_bullets()
            self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text=text)
        elif message_text == '子弹利润':
            text = self.detlaforce_service.get_bullets_profit()
            self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text=text)
        else:
            text = self._handle_talk_message(message=message_text, group_id=group_id)
            self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text=text)

    def _handle_group_message(self, message_body: Dict[str, Any], user_id: str,
                                group_id: str, sender: Dict[str, Any], message_id: str) -> None:
        """处理群聊消息"""
        message_text = self._get_message_text(message_body).strip()
        # 自动回应消息
        for emoji in self.send_emoji_list:
            if emoji['user_id'] == user_id:
                self.bot.set_message_emoji_like(message_id, emoji['emoji_id'])
        if message_text.startswith('#') :
            if message_text == "#在线人数":
                # 获取在线玩家列表
                player_list = self.mcbot_service.get_player_list()
                if player_list:
                    self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text=player_list)
                else:
                    self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text="获取在线玩家列表失败")
            elif message_text == "#tps":
                # 获取TPS
                tps = self.mcbot_service.get_tps()
                if tps:
                    self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text=tps)
                else:
                    self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text="获取TPS失败")
            elif message_text.startswith("#id"):
                player_id = message_text.split(" ")[1]
                query_info = self.yrzs_service.query_profile_by_name(player_id)
                self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text=query_info.get("message"))
            elif message_text.startswith("#qq"):
                player_qq = message_text.split(" ")[1]
                query_info = self.yrzs_service.query_profile_by_qq(player_qq)
                self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text=query_info.get("message"))
            elif message_text.startswith("#uid"):
                player_uid = message_text.split(" ")[1]
                query_info = self.yrzs_service.query_profile_by_uid(player_uid)
                self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text=query_info.get("message"))
            # elif message_text == "#更新查询":
            #     self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text="正在更新查询，这将花费很长时间")
            #     # 获取更新查询
            #     update_info = self.yrzs_service.update_profile_list()
            #     self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text=update_info.get("message"))
            else:
                # 转发消息
                text = message_text[1:].strip()
                if text:
                    result = self.mcbot_service.send_message(sender=sender, message=text)
                if result:
                    self.bot.send_group_message_text(group_id=group_id, user_id=user_id, text=result)

    def _handle_talk_message(self, message: str, group_id: str) -> None:
        """处理聊天消息"""
        if not self.bot.modes['group']['chat']['enable']:
            return "聊天未开启"
        response = self.chat_service.chat(message=message, user_id=group_id, model_name=self.bot.modes['group']['chat']['model'])
        return response

    def _get_current_time(self) -> str:
        """获取当前时间"""
        import datetime
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def _check_at(self, message_body: Dict[str, Any]) -> bool:
        """检查消息是否@当前bot"""
        for body in message_body:
            if body.get('type') == 'at' and str(body.get('data').get('qq')) == str(self.bot.qq):
                message_body.remove(body)
                return True, message_body
        return False, message_body

    def _get_message_text(self, message_body: Dict[str, Any]) -> str:
        """获取消息文本"""
        return ''.join([body.get('data', '').get('text', '') for body in message_body if body.get('type') == 'text'])
