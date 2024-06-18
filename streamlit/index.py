from langchain_community.llms import Ollama
import streamlit as st
from st_pages import Page, show_pages, add_page_title
import emoji

# 모델명 지정
llm = Ollama(model="llama2")

st.title("KPJC_GPT")

show_pages(
    [
        Page("index.py", "Chatbot", ":speech_balloon:"),
        Page("Translator.py", "Text to Audio translator", ":microphone:"),
        Page("Beta.py", "Other(개발중)", ":wrench:")
    ]
)

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_nickname" not in st.session_state:
    st.session_state.user_nickname = ""

# 사이드바 상단에 이미지 배치
with st.sidebar:
    st.image("./img/logo.png", use_column_width=True)
    st.title("User Settings")
    st.session_state.user_nickname = st.text_input("Enter your nickname", value=st.session_state.user_nickname)

def add_to_chat_history(user_input, bot_response):
    st.session_state.chat_history.append({"type": "user", "message": f"{st.session_state.user_nickname}: {user_input}"})
    st.session_state.chat_history.append({"type": "bot", "message": bot_response})

def display_chat_history():
    for message in st.session_state.chat_history:
        if message["type"] == "user":
            st.markdown(
                f"<div style='display: flex; justify-content: flex-start; margin-bottom: 10px;'>"
                f"<div style='background-color: #e0f0ff; padding: 10px; border-radius: 10px; max-width: 70%; color: #000000;'>"
                f"{emoji.emojize(':bust_in_silhouette:')} {message['message']} </div></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='display: flex; justify-content: flex-end; margin-bottom: 10px;'>"
                f"<div style='background-color: #f1f0f0; padding: 10px; border-radius: 10px; max-width: 70%; color: #000000;'>"
                f"{message['message']} {emoji.emojize(':robot:')} </div></div>",
                unsafe_allow_html=True
            )

def handle_user_input():
    user_input = st.session_state.get("user_input", "")
    if user_input:
        # LLM으로부터 응답받기
        bot_response = llm.invoke(user_input)

        # 대화 기록에 추가
        add_to_chat_history(user_input, bot_response)

        # 사용자 입력란 초기화
        st.session_state.user_input = ""

# 사용자 입력 필드와 전송 버튼을 같은 행에 배치
col1, col2 = st.columns([4, 1])
with col1:
    st.session_state.user_input = st.text_input("메시지를 입력하세요", label_visibility="collapsed", placeholder="메시지를 입력하세요")
with col2:
    send_button = st.button("전송" + emoji.emojize(":heavy_check_mark:"))

if send_button:
    handle_user_input()

# 대화 기록 표시
display_chat_history()
