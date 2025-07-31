"""
EduLingo - 英语教学AI助手
重构版本 - 使用模块化架构
"""

import streamlit as st
from ui.components import ui_components
from core.ai_service import ai_service
from core.conversation import conversation_manager


def main():
    """主函数"""
    # 设置页面配置
    ui_components.setup_page_config()
    
    # 初始化会话状态
    if "history" not in st.session_state:
        st.session_state.history = conversation_manager.initialize_session()
    
    # 渲染页面头部
    ui_components.render_header()
    
    # 渲染侧边栏并处理操作
    sidebar_action = ui_components.render_sidebar()
    
    # 处理侧边栏操作
    if sidebar_action == "clear_conversation":
        st.session_state.history = conversation_manager.clear_history()
        ui_components.show_success_message("✅ 对话已清空，可以开始新的学习会话！")
        st.rerun()
    
    elif sidebar_action == "export_conversation":
        if len(st.session_state.history) > 1:  # 有实际对话内容
            export_content = conversation_manager.export_conversation(
                st.session_state.history, format="txt"
            )
            st.download_button(
                label="📥 下载对话记录",
                data=export_content,
                file_name=f"edulingo_conversation_{conversation_manager.config_manager.student_id}.txt",
                mime="text/plain"
            )
        else:
            ui_components.show_info_message("📝 暂无对话记录可导出")
    
    # 渲染对话历史
    ui_components.render_conversation_history(st.session_state.history)
    
    # 渲染输入区域
    user_input = ui_components.render_input_area()
    
    # 处理用户输入
    if user_input:
        # 添加用户消息
        st.session_state.history = conversation_manager.add_message(
            st.session_state.history, "user", user_input
        )
        
        # 显示加载动画并生成回复
        with ui_components.render_loading_spinner():
            try:
                ai_reply = ai_service.generate_response(st.session_state.history)
                
                # 添加AI回复
                st.session_state.history = conversation_manager.add_message(
                    st.session_state.history, "assistant", ai_reply
                )
                
                # 刷新页面显示新消息
                st.rerun()
                
            except Exception as e:
                ui_components.show_error_message(f"❌ {str(e)}")
                # 移除最后添加的用户消息，因为处理失败
                st.session_state.history.pop()
                conversation_manager.save_history(st.session_state.history)


if __name__ == "__main__":
    main()
