# a_slider_game_v8_final_3_col_ranking.py

import streamlit as st
import random

############################################################################################################
# 페이지 환경 설정 (사용자 요청에 따라 절대 변경하지 않음)
############################################################################################################
st.set_page_config(
    initial_sidebar_state="expanded",
    # initial_sidebar_state="collapsed", # 사이드바 시작시 닫기
    page_icon="./images/파이.png",       # 이 경로에 파일이 실제로 존재해야 합니다.
    page_title="Math Day!"               # 브라우저 탭에 표시될 제목
)

# --- CSS 스타일 ---
# 슬라이더 툴팁 숨기기 및 모둠 이름 세로 정렬을 위한 스타일
st.markdown("""
<style>
[data-testid="stSliderThumbValue"] { color: transparent; }
[data-testid="stSliderThumbValue"]::before {
    content: '??'; color: red; font-size: 14px; font-weight: bold;
    position: absolute; top: 0; left: 50%; transform: translateX(-50%);
    width: 100%; text-align: center;
}
.team-label {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 49px; /* 슬라이더 높이와 유사하게 맞춰 정렬 */
    font-weight: bold;
    font-size: 1.1em;
}
.result-text {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 49px;
    font-size: 1.1em;
}
</style>
""", unsafe_allow_html=True)


############################################################################################################
# 기본값 및 상태 초기화
############################################################################################################
NUM_TEAMS = 5
TARGET_NUMBER = 31.4

def initialize_game():
    st.session_state.submitted = False
    st.session_state.max_value = round(random.uniform(50.0, 100.0), 1)
    initial_slider_value = st.session_state.max_value / 2.0
    st.session_state.slider_values = {i: initial_slider_value for i in range(1, NUM_TEAMS + 1)}
    st.session_state.scores = {i: 0 for i in range(1, NUM_TEAMS + 1)} # 점수 상태 추가

if 'max_value' not in st.session_state:
    initialize_game()

############################################################################################################
# 점수 계산 함수
############################################################################################################
def calculate_scores():
    """순위에 따라 점수를 계산하고 st.session_state.scores에 저장합니다."""
    results = []
    # 1. 모든 모둠의 결과(모둠 ID, 선택값, 오차)를 수집
    for i in range(1, NUM_TEAMS + 1):
        chosen_value = st.session_state.slider_values[i]
        error = abs(chosen_value - TARGET_NUMBER)
        results.append({"team_id": i, "value": chosen_value, "error": error})

    # 2. TARGET_NUMBER를 초과하지 않은 유효한 시도만 필터링
    valid_attempts = [r for r in results if r["value"] <= TARGET_NUMBER]
    
    # 3. 유효한 시도들을 오차가 작은 순서대로 정렬
    valid_attempts.sort(key=lambda x: x["error"])
    
    # 4. 점수 초기화 및 순위에 따라 점수 부여
    scores = {i: 0 for i in range(1, NUM_TEAMS + 1)}
    points = [3, 2, 1] # 1, 2, 3등 점수
    
    for rank, attempt in enumerate(valid_attempts):
        if rank < len(points):
            scores[attempt["team_id"]] = points[rank]
    
    st.session_state.scores = scores


############################################################################################################
# UI 구성
############################################################################################################
st.markdown("<h1 style='text-align: center; margin-bottom: 20px;'>🎯 π×10 맞추기!</h1>", unsafe_allow_html=True)

info_col, reset_button_col, submit_button_col = st.columns([3, 1, 1])
with info_col:
    st.info(f"**이번 라운드의 최대값은 `{st.session_state.max_value:.1f}` 입니다!**")
with reset_button_col:
    if st.button("🔄 초기화", use_container_width=True):
        initialize_game()
        st.rerun()

# --- [핵심 수정] 3단 메인 레이아웃 ---
team_name_col, slider_col, result_col = st.columns([1, 3, 1.5]) # 결과 컬럼을 조금 더 넓게

# --- 왼쪽: 모둠 이름 ---
with team_name_col:
    st.write("") # 컬럼 상단 여백
    for i in range(NUM_TEAMS):
        team_id = i + 1
        st.markdown(f'<div class="team-label">{team_id}모둠</div>', unsafe_allow_html=True)

# --- 중간: 슬라이더 ---
with slider_col:
    slider_values = {}
    for i in range(NUM_TEAMS):
        team_id = i + 1
        value = st.slider(
            label=f"hidden_label_{team_id}", # 레이블은 숨겨지므로 고유 ID만 부여
            min_value=0.0,
            max_value=st.session_state.max_value,
            value=st.session_state.slider_values.get(team_id, st.session_state.max_value / 2.0),
            step=0.1,
            key=f"slider_{team_id}",
            label_visibility="hidden" 
        )
        slider_values[team_id] = value

with submit_button_col:
    if st.button("결과 확인", type="primary", use_container_width=True):
        st.session_state.submitted = True
        st.session_state.slider_values = slider_values
        calculate_scores() # 버튼 클릭 시 점수 계산
        st.rerun()

# --- 오른쪽: 결과 표시 ---
with result_col:
    if st.session_state.submitted:
        st.markdown(f'<div class="team-label" style="color: green; font-weight: bold;">[정답: {TARGET_NUMBER:.1f}]</div>', unsafe_allow_html=True)

        medals = ["🥇", "🥈", "🥉"]
        
        for i in range(NUM_TEAMS):
            team_id = i + 1
            chosen_value = st.session_state.slider_values[team_id]
            error = abs(chosen_value - TARGET_NUMBER)
            score = st.session_state.scores[team_id]
            
            result_str = ""
            if chosen_value > TARGET_NUMBER:
                result_str = "❌ 0점 (초과)"
            else:
                # 점수에 따라 메달 이모티콘 추가
                if score == 3: result_str = f"🥇 {score}점"
                elif score == 2: result_str = f"🥈 {score}점"
                elif score == 1: result_str = f"🥉 {score}점"
                else: result_str = "0점"
                
                result_str += f" (오차: {error:.1f})"

            st.markdown(f'<div class="result-text">{result_str}</div>', unsafe_allow_html=True)