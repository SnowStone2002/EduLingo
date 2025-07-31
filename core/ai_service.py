"""AI服务模块"""
import openai
import streamlit as st
from typing import List, Dict, Any
from config.settings import config_manager
from config.prompts import prompt_manager


class AIService:
    """AI服务管理器"""
    
    def __init__(self):
        self.setup_client()
    
    def setup_client(self):
        """设置OpenAI客户端"""
        config_manager.setup_environment()
        openai.api_key = config_manager.api_key
    
    def generate_response(self, messages: List[Dict[str, str]], 
                         model: str = "gpt-4o", 
                         temperature: float = 0.5) -> str:
        """
        生成AI回复
        
        Args:
            messages: 对话消息列表
            model: 使用的模型
            temperature: 回复的随机性
            
        Returns:
            AI回复内容
        """
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            return response["choices"][0]["message"]["content"]
        
        except openai.error.AuthenticationError:
            error_msg = "API密钥无效，请检查配置文件中的api_key"
            st.error(error_msg)
            raise Exception(error_msg)
        
        except openai.error.RateLimitError:
            error_msg = "API调用频率限制，请稍后重试"
            st.error(error_msg)
            raise Exception(error_msg)
        
        except openai.error.APIConnectionError:
            error_msg = "网络连接失败，请检查网络设置和代理配置"
            st.error(error_msg)
            raise Exception(error_msg)
        
        except Exception as e:
            error_msg = f"AI服务请求失败: {str(e)}"
            st.error(error_msg)
            raise Exception(error_msg)
    
    def validate_api_key(self) -> bool:
        """
        验证API密钥是否有效
        
        Returns:
            是否有效
        """
        try:
            test_messages = [
                {"role": "system", "content": "Test"},
                {"role": "user", "content": "Hello"}
            ]
            self.generate_response(test_messages)
            return True
        except:
            return False


# 全局AI服务实例
ai_service = AIService()