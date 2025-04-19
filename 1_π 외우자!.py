import streamlit as st
import time
import random
from pathlib import Path # 경로 관리를 위해 사용

#페이지 환경 설정############################################################################################################
st.set_page_config(
    initial_sidebar_state="expanded",
    #initial_sidebar_state="collapsed",  #사이드바 시작시 닫기
    page_icon="./images/파이.png",     # 또는 ".\이미지폴더\파일명.확장자" - 실제 파일 경로 확인 필요
    page_title="Math Day!" # 브라우져 제목
)

#파이 값 설정 (소수점 이하, 공백 제거)##################################################################################################
pi_digits = (
    "14159265358979323846264338327950288419716939937510"
    "58209749445923078164062862089986280348253421170679"
    "82148086513282306647093844609550582231725359408128"
    "48111745028410270193852110555964462294895493038196"
    "44288109756659334461284756482337867831652712019091"
    "45648566923460348610454326648213393607260249141273"
    "72458700660631558817488152092096282925409171536436"
    "78925903600113305305488204665213841469519415116094"
    "33057270365759591953092186117381932611793105118548"
    "07446237996274956735188575272489122793818301194912"
).replace(" ", "")

#파이 값 자르기 함수 설정##################################################################################################
def format_pi_digits(digits):
    """파이 숫자를 5자리씩 띄어쓰고, 6묶음(30자리)마다 줄바꿈합니다."""
    #초기 설정
    formatted = "## "
    group_count = 0
    #반복문 설정(5자리씩 건너띄며 처리)
    for i in range(0, len(digits), 5):
        #5자리씩 파이값 자르기
        group = digits[i:i+5]
        if group_count > 0 and group_count % 6 == 0: #묶음이 6가 되면 줄바꿈
            formatted += "  \n## "
        elif group_count > 0:
                formatted += "    " # 묶음 사이에 4칸 공백 추가
        #잘라낸 그룹을 문자열 뒤에 추가 & 그룹카운트 1증가
        formatted += group
        group_count += 1
    return formatted

#세션 변수 설정##################################################################################################
if 'timer_active' not in st.session_state:  #타이머 표시
    st.session_state.timer_active = False
if 'start_time' not in st.session_state:    #시작시간
    st.session_state.start_time = 0.0
if 'pi_chunk_formatted' not in st.session_state:    #파이 값
    st.session_state.pi_chunk_formatted = ""
if 'range_text' not in st.session_state:    #안내문구
    st.session_state.range_text = ""

#상단 설명 UI 구성##################################################################################################
st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>Math Day!</h1>", unsafe_allow_html=True)
st.write("---") #수평선
st.write("## π 외우자!")
st.write("##### [게임 방법]")
"""
- 한 모둠씩 앞으로 나온다.
- **[π 외우기] 클릭 후 31.4초 동안 외우기 시작!!**  \n 화면에 **π의 소숫점 이하 특정 100자리 숫자가 표시**됩니다.
- 시간이 끝난 뒤 모둠원들은 순서대로 눈을 가린 뒤 차례대로 큰 소리로 외우고,  \n 다른 학생들은 틀린 자리를 확인한다.(각 팀마다 기회는 단 2번!!)
- 가장 많이 외운 팀이 승리!!
"""
st.write("##### [시상]")
"""
- **1등** 찰떡파이 12개
- **2등** 찰떡파이 10개
- **3등** 찰떡파이 8개
"""
st.write("---")

#파이 값 및 표시 영역 설정##################################################################################################
st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>< 외워야 할 π 값 ></h1>", unsafe_allow_html=True)

# 파이 값 표시 영역
if st.session_state.timer_active:
    st.markdown(st.session_state.pi_chunk_formatted)
else:
    # 높이를 조절하여 레이아웃 유지 (예: 5줄 기준 높이, 폰트 크기 고려)
    st.markdown("<div style='height: calc(1.8em * 2 * 5 + 10px); border: 1px dashed #ccc; display: flex; align-items: center; justify-content: center; color: #888;'>버튼을 누르면 여기에  π 값이 표시됩니다.</div>", unsafe_allow_html=True)

#정보 표시영역(파란부분)##################################################################################################
if st.session_state.timer_active:
     st.info(st.session_state.range_text)
else:
     st.info("외워야할 숫자가 여기에 나타납니다.")

#버튼 및 타이머 설정##################################################################################################
col1, col2, col3 = st.columns([1, 3, 1]) # 버튼과 타이머 영역 분리

# timer_placeholder 변수를 미리 정의 (None으로 초기화)
timer_placeholder = None

with col1:
    # 게임 시작 버튼
    if st.button("π 외우기", key="start_button", use_container_width=True):
        st.session_state.timer_active = True
        st.session_state.start_time = time.time() # 현재 시간 기록

        max_start_index = len(pi_digits) - 100
        start_index = random.randint(0, max_start_index) #시작 위치 설정
        end_index = start_index + 100 # 끝위치 설정
        raw_chunk = pi_digits[start_index:end_index] #외워야할 파이값 슬라이싱 for 함수에 넣기 위함
        st.session_state.pi_chunk_formatted = format_pi_digits(raw_chunk) #함수에 대입
        st.session_state.range_text = f"π 소수점 아래 {start_index + 1}번째 자리부터 {end_index}번째 자리까지의 숫자"
        st.rerun()

with col3:
    # 카운트다운 타이머 표시 영역
    if st.session_state.timer_active:
        # col3 내부에 플레이스홀더 생성
        timer_placeholder = st.empty()
        # 타이머 로직 실행 전에 초기 메시지 표시
        if not st.session_state.timer_active:
             timer_placeholder.metric("남은 시간", "-")
    else:
         st.write("") # 빈 공간 유지

#타이머 구현(세션 상태가 active일 때만 실행)##################################################################################################
if st.session_state.timer_active:
    countdown_duration = 31.4

    # timer_placeholder가 위에서 생성되었는지 확인(empty와 다름)
    if timer_placeholder is None:
        st.error("타이머 측정을 위한 공간이 생성되지 않았습니다.") # 비정상 상황 대비
    else:
        while st.session_state.timer_active:
            elapsed_time = time.time() - st.session_state.start_time
            remaining_time = countdown_duration - elapsed_time

            if remaining_time > 0: #시간이 아직 남은 경우
                timer_placeholder.metric("남은 시간", f"{remaining_time:.1f} 초")
                time.sleep(0.1)
            else:  #31.4초가 다 지난 경우
                timer_placeholder.metric("남은 시간", "  -")
                st.balloons()
                st.session_state.timer_active = False
            try:
                if remaining_time > 0:
                     st.rerun()
            except Exception as e:
                st.error(f"화면 업데이트 중 오류: {e}")
                st.session_state.timer_active = False
                break