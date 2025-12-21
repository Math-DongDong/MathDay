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

# --- [핵심 수정] 각 행별로 3열 레이아웃 (모둠명 / 슬라이더 / 결과) ---
st.write("")
for team_id in range(1, NUM_TEAMS + 1):
    col_name, col_slider, col_result = st.columns([1, 6, 2])

    with col_name:
        st.markdown(f'<div class="team-label">{team_id}모둠</div>', unsafe_allow_html=True)

    with col_slider:
        # 초기값은 세션에 저장된 값 또는 max의 절반
        initial = st.session_state.slider_values.get(team_id, st.session_state.max_value / 2.0)
        st.slider(
            label=f"hidden_label_{team_id}",
            min_value=0.0,
            max_value=st.session_state.max_value,
            value=initial,
            step=0.1,
            key=f"slider_{team_id}",
            label_visibility="hidden"
        )

    with col_result:
        # 제출 전에는 현재 선택값을, 제출 후에는 점수/메달을 보여줍니다.
        if st.session_state.get('submitted'):
            chosen_value = st.session_state.slider_values.get(team_id, st.session_state.get(f"slider_{team_id}", 0.0))
            if chosen_value > TARGET_NUMBER:
                result_str = "❌ 0점 (초과)"
            else:
                score = st.session_state.scores.get(team_id, 0)
                if score == 3:
                    result_str = f"🥇 {score}점"
                elif score == 2:
                    result_str = f"🥈 {score}점"
                elif score == 1:
                    result_str = f"🥉 {score}점"
                else:
                    result_str = "0점"
                error = abs(chosen_value - TARGET_NUMBER)
                result_str += f" (오차: {error:.1f})"

            st.markdown(f'<div class="result-text">{result_str}</div>', unsafe_allow_html=True)
        else:
            # 제출 전에는 현재 슬라이더 값을 간단히 표시
            current = st.session_state.get(f"slider_{team_id}", initial)
            st.markdown(f'<div class="result-text">선택: {current:.1f}</div>', unsafe_allow_html=True)

# 제출 버튼은 모든 행 아래에 하나만 배치
st.write("")
submit_col_left, submit_col_center, submit_col_right = st.columns([1, 2, 1])
with submit_col_center:
    if st.button("결과 확인", type="primary", use_container_width=True):
        # 각 슬라이더 키에서 값을 모아 세션의 slider_values에 저장
        for tid in range(1, NUM_TEAMS + 1):
            st.session_state.slider_values[tid] = st.session_state.get(f"slider_{tid}", st.session_state.slider_values.get(tid, st.session_state.max_value / 2.0))

        st.session_state.submitted = True
        calculate_scores()
        st.rerun()
