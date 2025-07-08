import requests
import json
from typing import Dict, Any, List
from flask import current_app

class ChatService:
    """聊天服务管理器"""
    
    def __init__(self):
        self.conversations = {}
        self.user_models = {}
    
    def chat(self, message: str, user_id: str, model_name: str = None) -> str:
        """发送聊天消息"""
        # 使用指定模型或用户的默认模型
        if model_name:
            self.user_models[user_id] = model_name
        else:
            model_name = self.user_models.get(user_id, 'gpt')
        
        # 获取用户对话历史
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        conversation = self.conversations[user_id]
        
        # 调用对应模型
        if model_name == 'gpt':
            response = self._call_gpt(message, conversation)
        elif model_name == 'deepseek':
            response = self._call_deepseek(message, conversation)
        elif model_name == 'gemini':
            response = self._call_gemini(message, conversation)
        else:
            response = "不支持的模型"
        
        # 保存对话记录
        conversation.append({"role": "user", "content": message})
        conversation.append({"role": "assistant", "content": response})
        
        # 限制对话长度
        if len(conversation) > 20:
            conversation[:] = conversation[-20:]
        
        return response
    
    def _call_gpt(self, message: str, conversation: List[Dict]) -> str:
        """调用GPT API"""
        try:
            api_key = current_app.config.get('OPENAI_API_KEY')
            if not api_key:
                return "GPT API密钥未配置"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            messages = conversation + [{"role": "user", "content": message}]
            
            data = {
                "model": current_app.config.get('OPENAI_MODEL', 'gpt-4o-mini'),
                "messages": messages,
                "max_tokens": 8192,
                "temperature": 0.7
            }
            
            base_url = current_app.config.get('OPENAI_BASE_URL', 'https://api.openai.com/v1')
            response = requests.post(f"{base_url}/chat/completions", 
                                   headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                current_app.logger.error(f"GPT API错误: {response.status_code}")
                return "GPT服务暂时不可用"
                
        except Exception as e:
            current_app.logger.error(f"GPT调用失败: {e}")
            return "抱歉，我遇到了问题"
    
    def _call_deepseek(self, message: str, conversation: List[Dict]) -> str:
        """调用DeepSeek API"""
        try:
            api_key = current_app.config.get('DEEPSEEK_API_KEY')
            if not api_key:
                return "DeepSeek API密钥未配置"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            messages = conversation + [{"role": "user", "content": message}]
            
            data = {
                "model": current_app.config.get('DEEPSEEK_MODEL', 'deepseek-chat'),
                "messages": messages,
                "max_tokens": 8192,
                "temperature": 0.7,
                "stream": False
            }
            
            base_url = current_app.config.get('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')
            response = requests.post(f"{base_url}/chat/completions", 
                                headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                current_app.logger.error(f"DeepSeek API错误: {response.status_code} - {response.text}")
                return "DeepSeek服务暂时不可用"
                
        except Exception as e:
            current_app.logger.error(f"DeepSeek调用失败: {e}")
            return "抱歉，DeepSeek遇到了问题"
    
    def _call_gemini(self, message: str, conversation: List[Dict]) -> str:
        """调用Gemini API（代理模式）"""
        try:
            api_key = current_app.config.get('GEMINI_API_KEY')
            if not api_key:
                return "Gemini API密钥未配置"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            messages = conversation + [{"role": "user", "content": message}]
            
            data = {
                "model": current_app.config.get('GEMINI_MODEL', 'gemini-2.5-flash-preview'),
                "messages": messages,
                "max_tokens": 8192,
                "temperature": 0.7,
                "stream": False
            }
            
            base_url = current_app.config.get('GEMINI_BASE_URL', 'https://gemini.wanqifan.top')
            response = requests.post(f"{base_url}/v1/chat/completions", 
                                headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                current_app.logger.error(f"Gemini API错误: {response.status_code} - {response.text}")
                return "Gemini服务暂时不可用"
                
        except Exception as e:
            current_app.logger.error(f"Gemini调用失败: {e}")
            return "抱歉，Gemini遇到了问题"

    def clear_conversation(self, user_id: str):
        """清除用户对话记录"""
        if user_id in self.conversations:
            self.conversations[user_id] = []
    
    def get_user_model(self, user_id: str) -> str:
        """获取用户当前模型"""
        return self.user_models.get(user_id, 'gpt')