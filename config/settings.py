"""配置管理模块"""
import os
import json
import streamlit as st
from typing import Dict, Any


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self._config = None
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if self._config is not None:
            return self._config
            
        if not os.path.exists(self.config_path):
            st.error(f"未找到配置文件: {self.config_path}")
            st.stop()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            return self._config
        except Exception as e:
            st.error(f"配置文件读取失败: {str(e)}")
            st.stop()
    
    @property
    def api_key(self) -> str:
        """获取API密钥"""
        return self.load_config().get("api_key", "")
    
    @property
    def proxy(self) -> str:
        """获取代理设置"""
        return self.load_config().get("proxy", "")
    
    @property
    def student_id(self) -> str:
        """获取学生ID"""
        return self.load_config().get("student_id", "student001")
    
    @property
    def history_file(self) -> str:
        """获取历史记录文件路径"""
        return f"history/{self.student_id}.json"
    
    def setup_environment(self):
        """设置环境变量"""
        if self.proxy:
            os.environ["http_proxy"] = self.proxy
            os.environ["https_proxy"] = self.proxy


# 全局配置实例
config_manager = ConfigManager()