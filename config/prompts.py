"""提示词管理模块"""
from typing import Dict, List


class PromptManager:
    """提示词管理器"""
    
    @staticmethod
    def get_system_prompt() -> Dict[str, str]:
        """获取系统提示词"""
        return {
            "role": "system",
            "content": (
                "你是一位专业的英语老师AI助手，专门帮助中国学生学习英语。"
                "你具备以下特点：\n"
                "1. 用清晰易懂的中文解释英语知识点\n"
                "2. 耐心细致，适合初中和高中学生的理解水平\n"
                "3. 能够提供语法讲解、词汇解析、句子润色等全方位帮助\n"
                "4. 鼓励学生多练习，给出建设性的学习建议\n"
                "5. 能够根据学生的问题深入浅出地进行解答\n\n"
                "请始终保持友善、专业的教学风格。"
            )
        }
    
    @staticmethod
    def get_welcome_message() -> str:
        """获取欢迎消息"""
        return (
            "欢迎使用EduLingo英语学习助手！🎓\n\n"
            "我是您的专属英语老师AI，可以帮助您：\n"
            "📚 语法知识讲解\n"
            "📝 词汇用法分析\n"
            "✍️ 句子润色改进\n"
            "🗣️ 英语表达指导\n\n"
            "请随时向我提问，我会用中文为您详细解答！"
        )
    
    @staticmethod
    def get_error_prompts() -> Dict[str, str]:
        """获取错误处理提示词"""
        return {
            "api_error": "抱歉，AI服务暂时不可用，请稍后重试。",
            "config_error": "配置文件有误，请检查config.json文件。",
            "network_error": "网络连接异常，请检查网络设置。"
        }


# 全局提示词管理实例
prompt_manager = PromptManager()