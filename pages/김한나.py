import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai

# ==========================================
# 1. 페이지 및 기본 설정
# ==========================================
st.set_page_config(page_title="AI 수행평가 매니저", page_icon="📅", layout="wide")

# 세션 상태 초기화 (데이터 저장용)
if 'assessments' not in st.session_state:
    st.session_state.assessments = []

# ==========================================
# 2. 헬퍼 함수
# ==========================================
def calculate_dday(target_date):
    """D-Day를 계산하는 함수"""
    today = datetime.now().date()
    delta = target_date - today
    if delta.days == 0:
        return "D-Day"
    elif delta.days > 0:
        return f"D-{delta.days}"
    else:
        return f"D+{abs(delta.days)} (마감됨)"

def get_ai_strategy(data_list):
    """Gemini API를 사용하여 대비 전략을 생성하는 함수"""
    try:
        # Secrets에서 API 키 가져오기
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            return "오류: Streamlit Secrets에 GEMINI_API_KEY가 설정되지 않았습니다."
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        # 프롬프트 구성
        prompt = "다음은 현재 준비해야 할 수행평가 목록입니다:\n"
        for item in data_list:
            if item['상태'] != "완료":
                prompt += f"- 과목: {item['과목']}, 내용: {item['평가 내용']}, 기한: {item['제출/평가일']}, 남은기간: {item['D-Day']}\n"
        
        prompt += "\n학생이 이 수행평가들을 성공적으로 마칠 수 있도록 남은 기간을 고려한 구체적인 준비 전략과 타임라인을 조언해주세요. 친절하고 격려하는 어조로 작성해주세요."
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"AI 응답 생성 중 오류가 발생했습니다: {e}"

# ==========================================
# 3. 화면 UI 구성
# ==========================================
st.title("📅 AI 수행평가 매니저")
st.markdown("수행평가 일정을 꼼꼼하게 기록하고, **AI에게 맞춤형 준비 전략**을 받아보세요!")

# 사이드바: 입력 폼
with st.sidebar:
    st.header("새로운 평가 등록")
    with st.form("add_assessment_form"):
        subject = st.text_input("과목명", placeholder="예: 정보, 국어, 과학")
        task = st.text_input("평가 내용", placeholder="예: 파이썬 데이터 분석 보고서")
        deadline = st.date_input("제출/평가일")
        status = st.selectbox("진행 상태", ["준비 전", "진행 중", "완료"])
        
        submitted = st.form_submit_button("일정 추가하기")
        
        if submitted:
            if subject and task:
                new_entry = {
                    "id": len(st.session_state.assessments),
                    "과목": subject,
                    "평가 내용": task,
                    "제출/평가일": deadline,
                    "D-Day": calculate_dday(deadline),
                    "상태": status
                }
                st.session_state.assessments.append(new_entry)
                st.success(f"'{subject}' 수행평가가 추가되었습니다!")
                st.rerun()
            else:
                st.warning("과목명과 평가 내용을 모두 입력해주세요.")

    if st.button("목록 전체 초기화", type="primary", use_container_width=True):
        st.session_state.assessments = []
        st.rerun()

# 메인 화면: 탭 구성
tab1, tab2 = st.tabs(["📋 전체 일정 보기", "🤖 AI 대비 전략 받기"])

with tab1:
    st.subheader("현재 등록된 수행평가")
    if not st.session_state.assessments:
        st.info("왼쪽 사이드바에서 새로운 수행평가 일정을 등록해주세요.")
    else:
        # 최신 D-Day 업데이트를 위해 리스트 갱신
        for item in st.session_state.assessments:
            item["D-Day"] = calculate_dday(item["제출/평가일"])
            
        # 데이터프레임으로 변환하여 표시 (id 컬럼 제외)
        df = pd.DataFrame(st.session_state.assessments)
        display_df = df.drop(columns=['id'])
        
        # 상태 업데이트를 위해 data_editor 사용
        edited_df = st.data_editor(
            display_df,
            column_config={
                "상태": st.column_config.SelectboxColumn(
                    "상태",
                    help="현재 진행 상태를 선택하세요",
                    options=["준비 전", "진행 중", "완료"],
                    required=True,
                )
            },
            disabled=["과목", "평가 내용", "제출/평가일", "D-Day"],
            use_container_width=True,
            hide_index=True
        )
        
        # 사용자가 상태를 변경하면 session_state에 반영
        if not edited_df.equals(display_df):
            for index, row in edited_df.iterrows():
                st.session_state.assessments[index]['상태'] = row['상태']

with tab2:
    st.subheader("AI 맞춤형 준비 계획")
    pending_tasks = [task for task in st.session_state.assessments if task['상태'] != "완료"]
    
    if not pending_tasks:
        st.success("현재 준비해야 할 수행평가가 없습니다! 훌륭합니다. 🎉")
    else:
        st.info(f"현재 완료되지 않은 수행평가가 **{len(pending_tasks)}개** 있습니다. AI에게 우선순위와 준비 전략을 물어보세요.")
        if st.button("✨ AI 대비 전략 생성하기", type="primary"):
            with st.spinner("AI가 최적의 타임라인을 계산하고 있습니다..."):
                strategy = get_ai_strategy(pending_tasks)
                st.markdown("---")
                st.markdown(strategy)
