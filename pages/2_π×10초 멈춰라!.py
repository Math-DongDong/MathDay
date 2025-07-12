import streamlit as st
import time
import random

############################################################################################################
# 페이지 환경 설정
############################################################################################################
st.set_page_config(
    initial_sidebar_state="expanded",
    #initial_sidebar_state="collapsed",  #사이드바 시작시 닫기
    page_icon="./images/파이.png",     # 또는 ".\이미지폴더\파일명.확장자" - 실제 파일 경로 확인 필요
    page_title="Math Day!" # 브라우져 제목
)

############################################################################################################
# 기본값 설정
############################################################################################################
# 모둠 수와 타이머 기본 설정
NUM_TEAMS = 5 
TARGET_TIME = 31.4

# 세션 설정
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = 0.0
if 'stop_times' not in st.session_state:
    st.session_state.stop_times = {}
if 'stop_pressed_status' not in st.session_state:
    st.session_state.stop_pressed_status = {i: False for i in range(1, NUM_TEAMS + 1)}
if 'all_stopped' not in st.session_state:
    st.session_state.all_stopped = False
if 'scores' not in st.session_state:
    st.session_state.scores = {i: 0 for i in range(1, NUM_TEAMS + 1)}

# 점수 계산 함수
def calculate_scores(stop_times):
    scores = {team_id: 0 for team_id in range(1, NUM_TEAMS + 1)}
    valid_attempts = []
    for team_id, stop_time in stop_times.items():
        if stop_time <= TARGET_TIME:
            diff = TARGET_TIME - stop_time
            valid_attempts.append({"team_id": team_id, "diff": diff})
    valid_attempts.sort(key=lambda x: x["diff"])
    points = [3, 2, 1]
    for rank, attempt in enumerate(valid_attempts):
        if rank < len(points):
            scores[attempt["team_id"]] = points[rank]
        else:
            break
    return scores


############################################################################################################
# UI구성
############################################################################################################
st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>π×10초 멈춰라!</h1>", unsafe_allow_html=True)

# 타이머 시작 버튼 (표 위에, 오른쪽 정렬) 배치
start_cols = st.columns([4, 1]) # 왼쪽 공간을 넓게 주고 오른쪽에 버튼 배치
with start_cols[0]: #왼쪽 컬럼에 경고문 출력
    st.warning("**소리로 신호를 주는 등 부정행위 시 해당 모둠은 0점 처리**",icon="⚠️")
with start_cols[1]: # 오른쪽 컬럼에 버튼 생성
    if st.button("타이머 시작", key="start_button", use_container_width=True, disabled=st.session_state.timer_running, type="primary"):
        st.session_state.timer_running = True
        st.session_state.start_time = time.time()
        st.session_state.stop_times = {}
        st.session_state.stop_pressed_status = {i: False for i in range(1, NUM_TEAMS + 1)}
        st.session_state.scores = {i: 0 for i in range(1, NUM_TEAMS + 1)}
        st.session_state.all_stopped = False
        st.toast("31.4초를 맞춰보세요. 시작!", icon="⏱️") # 시작 시 토스트 메시지
        time.sleep(2)
        st.rerun()

# 표 레이아웃 생성 (4행 5열 - 모둠 수만큼)
# 모둠 수만큼의 열만 생성
cols = st.columns(NUM_TEAMS)

#모둠 이름 설정(1행)
for i in range(NUM_TEAMS):
    with cols[i]: # 인덱스 0부터 시작
        st.markdown(f"<h5 style='text-align: center; margin-bottom: 10px;'>{i+1}모둠</h5>", unsafe_allow_html=True) # 하단 여백 추가

#측정시간 표시(2행)
time_display_placeholders = [cols[i].empty() for i in range(NUM_TEAMS)]

# --- 3행: 멈춰 버튼 ---
stop_button_placeholders = [cols[i].empty() for i in range(NUM_TEAMS)]

# --- 4행:모든 모둠이 멈춰를 눌렀을 때 점수 표시 영역 ---
score_display_placeholders = [cols[i].empty() for i in range(NUM_TEAMS)]

#안내문구
st.info("**시간이 기록된 모둠은 연한 녹색이 나타나요.**")

############################################################################################################
# 멈춰 버튼 생성 및 로직 실행 (3행 위치)
############################################################################################################
for i in range(NUM_TEAMS):
    team_id = i + 1 #모둠 번호
    placeholder = stop_button_placeholders[i]
    with placeholder:
        # 타이머가 흐르지 않을 때 또는 스탑상태일때 해당 모둠 멈춰 버튼 비활성화
        is_disabled = not st.session_state.timer_running or st.session_state.stop_pressed_status[team_id]
        if st.button(f"멈춰!", key=f"stop_button_{team_id}", use_container_width=True, disabled=is_disabled):
            if st.session_state.timer_running:
                # 몇초가 흘렀는지 타이머 계산
                elapsed_time = time.time() - st.session_state.start_time
                st.session_state.stop_times[team_id] = elapsed_time
                st.session_state.stop_pressed_status[team_id] = True

                if all(st.session_state.stop_pressed_status.values()):
                    st.session_state.all_stopped = True
                    st.session_state.timer_running = False
                    #점수 계산 함수에 넣어서 점수 계산
                    st.session_state.scores = calculate_scores(st.session_state.stop_times)
                st.rerun()
############################################################################################################
# 측정 시간 및 점수 표시 로직 (2행, 4행 위치)
############################################################################################################
for i in range(NUM_TEAMS):
    team_id = i + 1
    #시간표시
    time_placeholder = time_display_placeholders[i]
    #점수표시
    score_placeholder = score_display_placeholders[i]
    bg_color = "transparent" #시간 영역 배경색 투명
    #초기값 설정
    time_display_text = "-"
    score_display_text = "-"
    #멈춰를 눌렀다면 연한 녹색 반환
    if st.session_state.stop_pressed_status[team_id]:
        bg_color = "#d4edda"
    #모든 모둠이 다 눌러졌는지 확인
    if st.session_state.all_stopped:
        stop_time = st.session_state.stop_times.get(team_id)
        score = st.session_state.scores.get(team_id)
        # 스탑타입이 none가 아닌지(즉 기록이 있는지) 에 따라 텍스트 문구 설정(아직 출력은 아님)
        if stop_time is not None:
            time_display_text = f"{stop_time:.2f} 초"
            diff = abs(stop_time - TARGET_TIME)
            if stop_time > TARGET_TIME:
                 time_display_text += f"\n(초과: 0점)" 
                 score = 0
            else:
                 time_display_text += f"\n(오차: {diff:.2f})"

        # 점수 표시에따라 점수 문구 설정(아직 출력전)
        if score is not None:
            score_display_text = f"{score} 점"

############################################################################################################
# 측정시간과 점수 출력UI
############################################################################################################
    # 측정 시간 업데이트 (2행)
    time_placeholder.markdown(
        f"""
        <div style='background-color: {bg_color}; padding: 10px; border-radius: 5px; text-align: center; min-height: 60px; display: flex; align-items: center; justify-content: center; white-space: pre-wrap; font-weight: bold;'>
            {time_display_text}
        </div>
        """, unsafe_allow_html=True
    )
    # 점수 업데이트 (4행)
    if st.session_state.all_stopped:
        score_placeholder.markdown(
            f"""
            <div style='padding: 5px; text-align: center; min-height: 20px; display: flex; align-items: center; justify-content: center;'>
                {score_display_text}
            </div>
            """, unsafe_allow_html=True
        )

############################################################################################################
# 게임 방법 및 시상UI
############################################################################################################
st.write("---")
st.write("##### [게임 방법]")
st.markdown("""
- 각 팀에 한 명씩 나와서 전자칠판 앞에 나온다.
- **[타이머 시작]** 을 누르면 모든 모둠의 타이머가 **동시에 시작**됩니다.  \n\
  (화면에는 표시되지 않아요!)
- 각 모둠은 **31.4초**에 가장 가깝다고 생각될 때 자신의 모둠 번호 아래  **[멈춰!]**  클릭!
- **모든 모둠**이 '멈춰!'를 누르면, 각 모둠의 **측정 시간**과 **점수**가 표시됩니다.(총 5번 진행)
""")


#화면 분할
col1, col2 = st.columns(2)  #또는 [1,3]이라 입력하면 1:3으로 화면 분할
with col1:
    st.write("##### [점수 부여]")
    """
    - 31.4초를 지난 학생은 0점!
    - 31.4초에 가장 근접한 학생은 3점!!!
    - 31.4초에 두 번째로 근접한 학생은 2점!!
    - 31.4초에 세 번째로 근접한 학생에게 1점!    
    """
#with col2:
#    st.write("##### [시상]")
#    """
#    - **1등** 엄마손파이 8개
#    - **2등** 엄마손파이 7개
#    - **3등** 엄마손파이 5개
#    """