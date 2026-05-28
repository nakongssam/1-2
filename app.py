import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="연애 코칭 앱",
    page_icon="💖"
)

st.title("💖 연애 코칭 앱")
st.write("간단한 연애 고민을 입력해보세요!")

# 사용자 입력
user_input = st.text_input("고민 입력")

# 버튼 클릭
if st.button("조언 받기"):
    if user_input.strip() == "":
        st.warning("고민을 입력해주세요!")
    else:
        st.success("연애 코칭 결과 💌")

        # 아주 간단한 응답
        if "고백" in user_input:
            st.write("천천히 진심을 표현해보세요 😊")
        elif "싸움" in user_input:
            st.write("감정보다 대화를 먼저 해보는 게 좋아요 🌿")
        elif "이별" in user_input:
            st.write("충분히 힘들 수 있어요. 스스로를 먼저 챙겨주세요 💛")
        else:
            st.write("상대의 마음도 존중하며 솔직하게 이야기해보세요 🙂")
