# EduLingo - 本地化英语老师助手

import streamlit as st
import openai
import os
import json
from prompts import get_system_prompt
from conversation_store import load_history, save_history

# 读取配置
CONFIG_PATH = "config.json"
if not os.path.exists(CONFIG_PATH):
    st.error("未找到 config.json 配置文件")
    st.stop()

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

API_KEY = config.get("api_key")
PROXY = config.get("proxy")
STUDENT_ID = config.get("student_id", "student001")
HISTORY_FILE = f"history/{STUDENT_ID}.json"

# 设置代理和 API 密钥
os.environ["http_proxy"] = PROXY
os.environ["https_proxy"] = PROXY
openai.api_key = API_KEY

# Streamlit 页面配置
st.set_page_config(page_title="EduLingo - 英语教学助手", layout="wide")
st.title("📘 EduLingo - 英语老师 AI 助手")

# 初始化对话历史
if "history" not in st.session_state:
    st.session_state.history = load_history(HISTORY_FILE)
    if not st.session_state.history:
        st.session_state.history = [get_system_prompt()]

# 显示对话历史
for msg in st.session_state.history[1:]:
    role = "👨‍🎓 学生" if msg["role"] == "user" else "🤖 助手"
    st.markdown(f"**{role}**：{msg['content']}")

# 输入区域
user_input = st.text_area("✍️ 学生提问：", height=120)

if st.button("📩 提交问题") and user_input.strip():
    st.session_state.history.append({"role": "user", "content": user_input})
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=st.session_state.history,
            temperature=0.5
        )
        reply = response["choices"][0]["message"]["content"]
        st.session_state.history.append({"role": "assistant", "content": reply})
        save_history(st.session_state.history, HISTORY_FILE)
        st.rerun()
    except Exception as e:
        st.error(f"请求失败：{str(e)}")

if st.button("🗑 清除对话"):
    st.session_state.history = [get_system_prompt()]
    save_history(st.session_state.history, HISTORY_FILE)
    st.success("对话已清除")
