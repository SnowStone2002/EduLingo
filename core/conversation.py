"""对话管理模块"""
import os
import json
import streamlit as st
from typing import List, Dict, Any
from config.settings import config_manager
from config.prompts import prompt_manager


class ConversationManager:
    """对话管理器"""
    
    def __init__(self):
        self.config_manager = config_manager
        self.history_file = config_manager.history_file
    
    def load_history(self) -> List[Dict[str, str]]:
        """
        加载对话历史
        
        Returns:
            对话历史列表
        """
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                st.warning(f"历史记录加载失败: {str(e)}")
                return []
        return []
    
    def save_history(self, history: List[Dict[str, str]]):
        """
        保存对话历史
        
        Args:
            history: 对话历史列表
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            st.error(f"历史记录保存失败: {str(e)}")
    
    def initialize_session(self) -> List[Dict[str, str]]:
        """
        初始化会话
        
        Returns:
            初始化后的对话历史
        """
        history = self.load_history()
        if not history:
            history = [prompt_manager.get_system_prompt()]
            self.save_history(history)
        return history
    
    def add_message(self, history: List[Dict[str, str]], 
                   role: str, content: str) -> List[Dict[str, str]]:
        """
        添加消息到对话历史
        
        Args:
            history: 当前对话历史
            role: 角色 (user/assistant)
            content: 消息内容
            
        Returns:
            更新后的对话历史
        """
        history.append({"role": role, "content": content})
        self.save_history(history)
        return history
    
    def clear_history(self) -> List[Dict[str, str]]:
        """
        清除对话历史
        
        Returns:
            重置后的对话历史
        """
        history = [prompt_manager.get_system_prompt()]
        self.save_history(history)
        return history
    
    def get_display_messages(self, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        获取用于显示的消息列表（排除系统消息）
        
        Args:
            history: 完整对话历史
            
        Returns:
            显示用的消息列表
        """
        return [msg for msg in history if msg["role"] != "system"]
    
    def export_conversation(self, history: List[Dict[str, str]], 
                          format: str = "txt") -> str:
        """
        导出对话记录
        
        Args:
            history: 对话历史
            format: 导出格式 (txt/json)
            
        Returns:
            导出内容
        """
        if format == "json":
            return json.dumps(history, ensure_ascii=False, indent=2)
        
        elif format == "txt":
            lines = []
            for msg in self.get_display_messages(history):
                role = "学生" if msg["role"] == "user" else "AI助手"
                lines.append(f"【{role}】: {msg['content']}\n")
            return "\n".join(lines)
        
        else:
            raise ValueError(f"不支持的导出格式: {format}")


# 全局对话管理实例
conversation_manager = ConversationManager()