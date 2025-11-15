# a_slider_game_v7_final_3_col_layout.py

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

# 슬라이더의 움직이는 툴팁 값을 '??'로 변경하는 CSS
st.markdown("""
<style>
[data-testid="stSliderThumbValue"] {
    color: transparent;
}
[data-testid="stSliderThumbValue"]::before {
    content: '??';
    color: red;
    font-size: 14px;
    font-weight: bold;
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


############################################################################################################
# 기본값 및 상태 초기화
############################################################################################################
NUM_TEAMS = 5
TARGET_NUMBER = 31.4

# 세션 상태를 초기화하는 함수
def initialize_game():
    """게임을 초기화하거나 재시작할 때 필요한 모든 상태 변수를 생성합니다."""
    st.session_state.submitted = False
    st.session_state.max_value = round(random.uniform(50.0, 100.0), 1)
    initial_slider_value = st.session_state.max_value / 2.0
    st.session_state.slider_values = {i: initial_slider_value for i in range(1, NUM_TEAMS + 1)}

# 'max_value'가 session_state에 없는 경우, 무조건 게임을 초기화
if 'max_value' not in st.session_state:
    initialize_game()

############################################################################################################
# UI 구성
############################################################################################################
st.markdown("<h1 style='text-align: center; margin-bottom: 20px;'>🎯 π×10 맞추기!</h1>", unsafe_allow_html=True)

# [핵심 수정] 안내 문구와 버튼들을 3:1:1 비율의 한 줄에 배치합니다.
info_col, reset_button_col, submit_button_col = st.columns([3, 1, 1])

with info_col:
    st.info(f"**이번 라운드의 최대값은 `{st.session_state.max_value:.1f}` 입니다!**")

with reset_button_col:
    # --- 초기화 버튼 ---
    if st.button("초기화", use_container_width=True):
        initialize_game()
        st.rerun()

# --- 슬라이더와 결과 표시를 위한 메인 컬럼 ---
slider_col, result_col = st.columns([2, 1])

with slider_col:
    # --- 슬라이더 생성 ---
    slider_values = {}
    for i in range(NUM_TEAMS):
        team_id = i + 1
        value = st.slider(
            label=f"**{team_id}모둠**의 선택",
            min_value=0.0,
            max_value=st.session_state.max_value,
            value=st.session_state.slider_values.get(team_id, st.session_state.max_value / 2.0),
            step=0.1,
            key=f"slider_{team_id}",
            label_visibility="hidden" 
        )
        slider_values[team_id] = value

with submit_button_col:
    # --- 확인 버튼 ---
    # use_container_width=True로 컬럼 너비에 꽉 차게 만듭니다.
    if st.button("결과 확인", type="primary", use_container_width=True):
        st.session_state.submitted = True
        st.session_state.slider_values = slider_values
        st.rerun()

with result_col:
    # --- 결과 표시 ---
    if st.session_state.submitted:
        st.subheader("🎉 결과 발표!")
        
        for i in range(NUM_TEAMS):
            team_id = i + 1
            chosen_value = st.session_state.slider_values[team_id]
            error = abs(chosen_value - TARGET_NUMBER)
            
            st.markdown(f"**{team_id}모둠:** `{chosen_value:.1f}` (오차: `{error:.1f}`)")