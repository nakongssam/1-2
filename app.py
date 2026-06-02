import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💕"
)

st.title("💕 연애상담 챗봇")

# API 키 확인
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash-lite")

except Exception:
    st.error("API 키를 확인해주세요.")
    st.stop()

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요💕 연애 고민을 편하게 이야기해주세요."
        }
    ]

# 이전 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자 입력
if prompt := st.chat_input("연애 고민을 입력하세요"):

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    try:
        # 대화 기록 생성
        conversation = ""

        for msg in st.session_state.messages:
            if msg["role"] == "user":
                conversation += f"사용자: {msg['content']}\n"
            else:
                conversation += f"상담사: {msg['content']}\n"

        system_prompt = f"""
당신은 따뜻하고 공감 능력이 뛰어난 연애상담 전문가입니다.

규칙:
- 공감하는 말투 사용
- 비난하지 말 것
- 현실적인 조언 제공
- 한국어로 답변
- 너무 길지 않게 답변

대화:
{conversation}
"""

        response = model.generate_content(system_prompt)
        answer = response.text

    except Exception as e:
        answer = f"오류가 발생했습니다.\n\n{e}"

    # 응답 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.write(answer)
