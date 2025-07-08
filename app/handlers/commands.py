from flask import current_app
from typing import Dict, Any, List
from enum import Enum

class PermissionLevel(Enum):
    """权限级别枚举"""
    EVERYONE = "everyone"      # 所有人
    ADMIN = "admin"           # 仅管理员

class CommandHandler:
    """命令处理器"""

    def __init__(self, bot):
        self.bot = bot
        self.commands = {
            # '/help': self._help_command,
            '/关闭聊天': {'handler': self._close_chat_command, 'permission': PermissionLevel.ADMIN},
            '/开启聊天': {'handler': self._open_chat_command, 'permission': PermissionLevel.ADMIN},
            '/gpt': {'handler': self._gpt_model_command, 'permission': PermissionLevel.EVERYONE},
            '/deepseek': {'handler': self._deepseek_model_command, 'permission': PermissionLevel.EVERYONE},
            '/gemini': {'handler': self._gemini_model_command, 'permission': PermissionLevel.EVERYONE},
        }

    def handle_command(self, command: str, user_id: str, group_id: str, sender: Dict[str, Any]) -> str:
        """处理命令"""
        cmd_parts = command.split()
        cmd_name = cmd_parts[0]
        args = cmd_parts[1:] if len(cmd_parts) > 1 else []

        if cmd_name not in self.commands:
            current_app.logger.warning(f"未知命令: {cmd_name}")
            return "未知命令，请使用 /help 查看可用命令"
        
        command_config = self.commands[cmd_name]
        required_permission = command_config['permission']
        
        # 检查权限
        if not self._check_permission(user_id, required_permission):
            current_app.logger.warning(f"用户 {user_id} 尝试使用无权限命令: {cmd_name}")
            return "❌ 权限不足，此命令仅限管理员使用"
        
        # 执行命令
        try:
            handler = command_config['handler']
            result = handler(args, user_id, group_id, sender)
            current_app.logger.info(f"用户 {user_id} 成功执行命令: {cmd_name}")
            return result
        except Exception as e:
            current_app.logger.error(f"执行命令 {cmd_name} 失败: {e}")
            return "❌ 执行命令时发生错误，请稍后再试"
    
    def _check_permission(self, user_id: str, required_permission: PermissionLevel) -> bool:
        """检查用户权限"""
        # 所有人都可以使用的命令
        if required_permission == PermissionLevel.EVERYONE:
            return True
        
        # 检查管理员权限
        if required_permission == PermissionLevel.ADMIN:
            admin_qq = current_app.config.get('ADMIN_QQ', '')
            # 支持多个管理员QQ，用逗号分隔
            admin_qqs = [qq.strip() for qq in admin_qq.split(',') if qq.strip()]
            return user_id in admin_qqs
        
        return False


#     def _help_command(self, args, user_id, group_id, sender):
#         """帮助命令"""
#         help_text = """可用命令:
# /help - 显示帮助信息
# /ping - 测试机器人响应
# /info - 显示机器人信息
# /time - 显示当前时间"""

#         return help_text

    def _open_chat_command(self, args, user_id, group_id, sender):
        """开启聊天功能"""
        self.bot.modes['group']['chat']['enable'] = True
        return "聊天功能已开启"
    
    def _close_chat_command(self, args, user_id, group_id, sender):
        """关闭聊天功能"""
        self.bot.modes['group']['chat']['enable'] = False
        return "聊天功能已关闭"

    def _gpt_model_command(self, args, user_id, group_id, sender):
        """切换到GPT模型"""
        self.bot.modes['group']['chat']['model'] = 'gpt'
        return f"已切换至{current_app.config['OPENAI_MODEL']}"

    def _deepseek_model_command(self, args, user_id, group_id, sender):
        """切换到DeepSeek模型"""
        self.bot.modes['group']['chat']['model'] = 'deepseek'
        return f"已切换至{current_app.config['DEEPSEEK_MODEL']}"
    
    def _gemini_model_command(self, args, user_id, group_id, sender):
        """切换到Gemini模型"""
        self.bot.modes['group']['chat']['model'] = 'gemini'
        return f"已切换至{current_app.config['GEMINI_MODEL']}"