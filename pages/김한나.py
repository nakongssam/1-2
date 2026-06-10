import random
import time
import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="평화로운 교실 룰렛", page_icon="🤫", layout="centered"
)

# 2. 세션 상태(Session State) 초기화
if "history" not in st.session_state:
    st.session_state.history = []

# 기본 학생 명단 및 벌칙 리스트 세팅
if "default_students" not in st.session_state:
    st.session_state.default_students = "홍길동, 김철수, 이영희"

if "default_penalties" not in st.session_state:
    st.session_state.default_penalties = (
        "교실 바닥 쓰레기 5개 줍기\n"
        "칠판 깨끗하게 닦아 두기\n"
        "다음 수업 시간 시작 시 '차렷 경례' 구호 크게 외치기\n"
        "선생님께 공손하게 '앞으로 조용히 하겠습니다' 3번 말하기\n"
        "이번 주 우유 급식 배당 도와주기"
    )

# 3. 사이드바: 명단 및 벌칙 설정
st.sidebar.header("⚙️ 룰렛 설정 관리")
st.sidebar.markdown("구분자(,) 또는 줄바꿈으로 입력해주세요.")

# 학생 명단 입력 받기
students_input = st.sidebar.text_area(
    "🤫 오늘의 요주의 학생 명단", value=st.session_state.default_students, height=100
)
# 벌칙 내용 입력 받기
penalties_input = st.sidebar.text_area(
    "💥 교육적인 벌칙 리스트", value=st.session_state.default_penalties, height=150
)

# 데이터 정제 (공백 제거 및 리스트화)
student_list = [
    s.strip()
    for s in students_input.replace("\n", ",").split(",")
    if s.strip()
]
penalty_list = [p.strip() for p in penalties_input.split("\n") if p.strip()]

# 4. 메인 화면 구성
st.title("🤫 평화로운 교실을 위한 벌칙 룰렛")
st.markdown(
    "교실을 시끄럽게 조정한 학생에게 공정하고 유쾌한 규칙을 적용해보세요! 감정 상하지 않는 평화로운 학급 경영을 지원합니다."
)
st.markdown("---")

# 5. 메인 로직 및 예외 처리
if not student_list or not penalty_list:
    st.warning("⚠️ 사이드바에 학생 이름과 벌칙 내용을 최소 1개 이상 입력해주세요!")
else:
    col1, col2 = st.columns(2)
    with col1:
        st.write("🎯 **현재 추첨 대상 학생:**")
        st.info(", ".join(student_list))
    with col2:
        st.write("📋 **등록된 벌칙 종류:**")
        st.caption(" • " + "\n • ".join(penalty_list))

    st.markdown("---")

    # 룰렛 구동 버튼
    if st.button("🎰 룰렛 돌리기! (결과 추첨)", type="primary", use_container_width=True):
        # 셔플 및 당첨자 선정 완료 단계 시각 효과 (애니메이션 느낌 연출)
        status_text = st.empty()
        progress_bar = st.progress(0)

        # 교실 집중용 가짜 카운트다운 효과
        for i in range(1, 11):
            temp_student = random.choice(student_list)
            temp_penalty = random.choice(penalty_list)
            status_text.subheader(
                f"🎲 룰렛 회전 중... 👉 **[{temp_student}]** 학생 일까?!"
            )
            progress_bar.progress(i * 10)
            time.sleep(0.15)  # 속도 조절

        # 최종 결정
        final_student = random.choice(student_list)
        final_penalty = random.choice(penalty_list)

        # 결과 화면 출력
        status_text.empty()
        progress_bar.empty()

        st.error("🎉 [ 당 첨 자 확 정 ] 🎉")
        st.markdown(
            f"""
            <div style="background-color:#ffe6e6; padding:20px; border-radius:10px; border:2px solid #ff4b4b; text-align:center;">
                <h2 style="color:#ff4b4b; margin:0;">👤 {final_student} 학생</h2>
                <p style="font-size:18px; color:#333; margin-top:10px;">당첨된 벌칙: <b>{final_penalty}</b></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 히스토리 저장
        current_time = datetime.datetime.now().strftime("%H:%M:%S") if "datetime" in globals() else time.strftime("%H:%M:%S")
        st.session_state.history.insert(
            0, f"[{current_time}] {final_student} -> {final_penalty}"
        )

        # 경고 효과음 대신 화면 이펙트
        st.snow()

# 6. 추첨 히스토리 관리
st.markdown("---")
st.subheader("📜 오늘의 벌칙 수행 기록")

if st.session_state.history:
    for record in st.session_state.history:
        st.write(record)

    if st.button("기록 초기화"):
        st.session_state.history = []
        st.rerun()
else:
    st.caption("아직 수행된 벌칙 내역이 없습니다. 룰렛을 돌려보세요!")
