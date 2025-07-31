"""UI组件模块"""
import streamlit as st
from typing import List, Dict, Callable
from config.prompts import prompt_manager


class UIComponents:
    """UI组件管理器"""
    
    @staticmethod
    def setup_page_config():
        """设置页面配置"""
        st.set_page_config(
            page_title="EduLingo - 英语教学助手",
            page_icon="📘",
            layout="wide",
            initial_sidebar_state="auto"
        )
    
    @staticmethod
    def render_header():
        """渲染页面标题"""
        st.title("📘 EduLingo - 英语老师 AI 助手")
        st.markdown("---")
        
        # 添加欢迎信息
        with st.expander("👋 使用指南", expanded=False):
            st.markdown(prompt_manager.get_welcome_message())
    
    @staticmethod
    def render_sidebar():
        """渲染侧边栏"""
        with st.sidebar:
            st.header("🛠️ 功能菜单")
            
            # 学习统计
            st.subheader("📊 学习统计")
            if "history" in st.session_state:
                user_messages = [msg for msg in st.session_state.history 
                               if msg["role"] == "user"]
                st.metric("提问次数", len(user_messages))
            
            st.markdown("---")
            
            # 快捷操作
            st.subheader("⚡ 快捷操作")
            
            if st.button("🗑️ 清空对话", use_container_width=True):
                return "clear_conversation"
            
            if st.button("📥 导出对话", use_container_width=True):
                return "export_conversation"
            
            st.markdown("---")
            
            # 学习建议
            st.subheader("💡 学习建议")
            st.info(
                "💡 **提问技巧:**\n"
                "• 描述具体的语法问题\n"
                "• 提供完整的句子context\n"
                "• 说明您的疑惑点\n"
                "• 询问使用场景"
            )
        
        return None
    
    @staticmethod
    def render_conversation_history(history: List[Dict[str, str]]):
        """
        渲染对话历史
        
        Args:
            history: 对话历史列表
        """
        # 排除系统消息
        display_messages = [msg for msg in history if msg["role"] != "system"]
        
        if not display_messages:
            st.info("💬 开始您的英语学习之旅吧！请在下方输入您的问题。")
            return
        
        # 创建对话容器
        chat_container = st.container()
        
        with chat_container:
            for i, msg in enumerate(display_messages):
                if msg["role"] == "user":
                    UIComponents._render_user_message(msg["content"], i)
                else:
                    UIComponents._render_assistant_message(msg["content"], i)
    
    @staticmethod
    def _render_user_message(content: str, index: int):
        """渲染用户消息"""
        with st.chat_message("user", avatar="👨‍🎓"):
            st.markdown(f"**学生提问：**\n{content}")
    
    @staticmethod
    def _render_assistant_message(content: str, index: int):
        """渲染助手消息"""
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(f"**AI老师：**\n{content}")
    
    @staticmethod
    def render_input_area() -> str:
        """
        渲染输入区域
        
        Returns:
            用户输入内容
        """
        st.markdown("### ✍️ 向AI老师提问")
        
        # 输入区域
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_input = st.text_area(
                label="请输入您的英语问题：",
                height=120,
                placeholder="例如：请解释一下现在完成时的用法...",
                key="user_input"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # 添加垂直间距
            submit_button = st.button(
                "📩 提交问题",
                use_container_width=True,
                type="primary",
                help="点击发送您的问题给AI老师"
            )
        
        # 快捷问题按钮
        st.markdown("**💡 快捷问题：**")
        quick_questions = [
            "解释现在完成时的用法",
            "这个句子有语法错误吗？",
            "如何提高英语写作水平？",
            "常见的英语介词用法"
        ]
        
        cols = st.columns(len(quick_questions))
        for i, question in enumerate(quick_questions):
            if cols[i].button(question, key=f"quick_{i}"):
                st.session_state.user_input = question
                submit_button = True
        
        return user_input if submit_button and user_input.strip() else ""
    
    @staticmethod
    def render_loading_spinner(message: str = "AI老师正在思考..."):
        """渲染加载动画"""
        return st.spinner(message)
    
    @staticmethod
    def show_success_message(message: str):
        """显示成功消息"""
        st.success(message)
    
    @staticmethod
    def show_error_message(message: str):
        """显示错误消息"""
        st.error(message)
    
    @staticmethod
    def show_info_message(message: str):
        """显示信息消息"""
        st.info(message)


# 全局UI组件实例
ui_components = UIComponents()