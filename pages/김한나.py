import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. 페이지 및 기본 설정
# ==========================================
st.set_page_config(page_title="AI 스마트 분리수거 도우미", page_icon="♻️", layout="centered")

# ==========================================
# 2. 헬퍼 함수 (AI API 호출)
# ==========================================
def get_recycling_guide(item_name):
    """Gemini API를 사용하여 분리수거 방법을 안내하는 함수"""
    try:
        # Secrets에서 API 키 가져오기
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            return "오류: Streamlit Secrets에 GEMINI_API_KEY가 설정되지 않았습니다."
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        # 프롬프트 구성 (한국 분리배출 규정 강조)
        prompt = f"""
        당신은 대한민국 환경부 가이드라인을 완벽하게 숙지하고 있는 친절한 분리수거 전문가입니다.
        사용자가 '{item_name}'을(를) 버리는 방법을 물어보았습니다.
        
        다음 규칙에 따라 3~4문장으로 명확하게 답변해 주세요:
        1. 재활용이 가능한지, 아니면 일반 쓰레기(종량제 봉투)로 버려야 하는지 명확히 밝혀주세요.
        2. 분리배출 시 주의할 점(예: 씻어서, 라벨을 떼고 등)을 포함해 주세요.
        3. 친절하고 이해하기 쉬운 말투로 작성해 주세요.
        """
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"AI 응답 생성 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.\n(에러 상세: {e})"

# ==========================================
# 3. 화면 UI 구성
# ==========================================
st.title("♻️ AI 스마트 분리수거 도우미")
st.markdown("헷갈리는 쓰레기 버리는 방법, 이제 AI 전문가에게 물어보세요!")

# 탭 구성
tab1, tab2 = st.tabs(["🔍 어떻게 버릴까?", "🧠 분리수거 상식 퀴즈"])

# --- 탭 1: AI 분리수거 검색기 ---
with tab1:
    st.subheader("버리기 애매한 물건을 입력해 보세요.")
    item_input = st.text_input(
        "물품 이름", 
        placeholder="예: 치킨 뼈, 컵라면 용기, 깨진 화분, 보온병"
    )
    
    if st.button("AI에게 물어보기", type="primary", use_container_width=True):
        if item_input.strip():
            with st.spinner(f"'{item_input}' 버리는 방법을 찾고 있습니다... 🧐"):
                guide = get_recycling_guide(item_input)
                st.success("안내를 확인해 주세요!")
                st.info(guide)
        else:
            st.warning("버리려는 물품의 이름을 먼저 입력해 주세요.")

# --- 탭 2: 분리수거 상식 퀴즈 ---
with tab2:
    st.subheader("당신의 분리수거 점수는? O/X 퀴즈")
    st.markdown("정답을 확인하려면 아래 질문을 클릭해 주세요.")
    
    with st.expander("Q1. 기름이 잔뜩 묻어 지워지지 않는 피자 박스는 종이류로 배출한다?"):
        st.error("**X (일반 쓰레기)**")
        st.write("음식물이 묻어 오염된 종이는 재활용이 어렵습니다. 잘게 찢어서 종량제 봉투에 버려야 합니다.")
        
    with st.expander("Q2. 닭 뼈나 돼지 뼈는 음식물 쓰레기로 버려야 한다?"):
        st.error("**X (일반 쓰레기)**")
        st.write("동물의 뼈, 조개껍데기, 달걀 껍데기 등은 동물이 먹을 수 없으므로 일반 쓰레기(종량제 봉투)로 배출해야 합니다.")
        
    with st.expander("Q3. 펌프형 용기(샴푸 등)는 그대로 플라스틱으로 배출한다?"):
        st.error("**X (분리 후 배출)**")
        st.write("펌프 내부에는 철수프링 등 다른 재질이 섞여 있습니다. 펌프 부분은 일반 쓰레기로 버리고, 몸통 부분만 씻어서 플라스틱으로 배출하는 것이 좋습니다.")

    with st.expander("Q4. 깨진 유리컵은 신문지에 싸서 종량제 봉투에 버린다?"):
        st.success("**O (정답)**")
        st.write("깨진 유리는 재활용이 안 되며 수거하시는 분이 다칠 수 있습니다. 신문지 등으로 두껍게 싼 뒤 '깨진 유리 주의'라고 적어 종량제 봉투(또는 전용 마대)에 버려야 합니다.")
