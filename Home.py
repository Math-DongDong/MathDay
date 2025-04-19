import streamlit as st

#페이지 환경 설정
st.set_page_config(
    initial_sidebar_state="expanded",
    #initial_sidebar_state="collapsed",  #사이드바 시작시 닫기
    page_icon="./images/파이.png",     # 또는 ".\이미지폴더\파일명.확장자"
    page_title="Math Day!"              #브라우져 제목
)

#문구출력
st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>Math Day!</h1>", unsafe_allow_html=True)
st.write("---") #수평선
st.write(">  **3월 14일**을 남자가 여자에게 사랑을 고백하는 날이라고 하여 화이트데이라고 부릅니다.  \n그러나 사실 화이트데이는 어떤 제과회사에서 만든 얄팍한 상술에 의해 만들어진 기념일 뿐!  \n수학자들 사이에서는 원주율이 3.141592…임을 기념하기 위한 **파이 데이**로 알려져 있습니다.  \n**math day를 맞이하여 π와 함께 다양한 활동**을 해봅시다.")
st.markdown("## π가 궁금해!")

#화면 분할 후 이미지 출력
col1, col2 = st.columns([1.5,2.5]) 
with col1:
    st.image("./images/원주율설명.png") 
with col2:
    st.image("./images/파이유래.png")


#파이 관련 영상 출력
st.video("https://youtu.be/qX2MP3Om4zg")

st.write("---") #수평선
st.markdown("<h4 style='text-align: center; margin-bottom: 10px;'>잠깐! 활동을 하기에 앞서... 5개의 모둠을 만들어주세요.</h4>", unsafe_allow_html=True)
