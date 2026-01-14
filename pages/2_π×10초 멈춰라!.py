import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(
    page_title="Math Day!",
    page_icon="./images/파이.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("π × 10초 멈춰라!")

# --------------------------------------------------------------------------------
# 자바스크립트 및 HTML/CSS 포함한 게임 로직
# --------------------------------------------------------------------------------
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        /* 기본 폰트 및 스타일 */
        body { font-family: "Source Sans Pro", sans-serif; margin: 0; padding: 5px; }
        
        .game-container {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        /* --- [수정됨] 상단 컨트롤 패널: 한 줄 배치 --- */
        .control-panel {
            display: flex;
            justify-content: space-between; /* 양쪽 끝으로 배치 */
            align-items: center; /* 수직 중앙 정렬 */
            margin-bottom: 10px;
        }

        /* 경고 문구 스타일 (st.warning 흉내) */
        .warning-box {
            background-color: #ffeba0; /* 연한 노란색 배경 */
            color: #9c6500;            /* 짙은 갈색 텍스트 */
            padding: 12px 15px;
            border-radius: 0.5rem;
            font-size: 1rem;
            display: flex;
            align-items: center;
            flex-grow: 1;              /* 남은 공간 차지 */
            margin-right: 20px;        /* 버튼과의 간격 */
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        /* 시작 버튼 스타일 */
        #start-btn {
            background-color: #ff4b4b;
            color: white;
            border: none;
            border-radius: 0.5rem;
            padding: 12px 24px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap; /* 줄바꿈 방지 */
            transition: background 0.2s;
        }
        #start-btn:disabled { background-color: #ffcccb; cursor: not-allowed; }
        #start-btn:hover:not(:disabled) { background-color: #d93e3e; }


        /* 모둠 그리드 레이아웃 */
        .team-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr); /* 5개 모둠 */
            gap: 15px;
        }

        .team-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }

        .team-title { font-size: 1.2rem; font-weight: bold; margin-bottom: 5px; }

        /* 결과 표시 박스 */
        .result-box {
            width: 100%;
            min-height: 80px;
            background-color: #f0f2f6;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-weight: bold;
            font-size: 1.1rem;
            white-space: pre-wrap;
            color: #31333F;
        }

        /* 멈춰 버튼 스타일 */
        .stop-btn {
            background-color: #ffffff;
            border: 1px solid #d6d6d6;
            border-radius: 8px;
            color: #31333F;
            padding: 15px 0;
            width: 100%;
            font-size: 1.2rem;
            font-weight: 600;
            cursor: pointer;
        }
        .stop-btn:hover:not(:disabled) { border-color: #ff4b4b; color: #ff4b4b; }
        .stop-btn:disabled { background-color: #f9f9f9; color: #d0d0d0; cursor: not-allowed; border-color: #e0e0e0; }

        /* 점수 박스 */
        .score-box {
            min-height: 30px;
            font-weight: bold;
            color: #ff4b4b;
            font-size: 1.2rem;
        }
        
        .bg-stopped { background-color: #d4edda !important; }

    </style>
</head>
<body>

    <div class="game-container">
        
        <!-- [수정됨] 상단 영역: 경고문구(좌) + 시작버튼(우) -->
        <div class="control-panel">
            <div class="warning-box">
                <span style="margin-right: 10px; font-size: 1.2rem;">⚠️</span>
                <strong>소리로 신호를 주는 등 부정행위 시 해당 모둠은 0점 처리</strong>
            </div>
            <button id="start-btn" onclick="startGame()">타이머 시작</button>
        </div>

        <!-- 모둠 영역 (5개) -->
        <div class="team-grid">
            <!-- 1모둠 -->
            <div class="team-card">
                <div class="team-title">1모둠</div>
                <div id="result-1" class="result-box">-</div>
                <button id="stop-1" class="stop-btn" onclick="stopTeam(1)" disabled>멈춰!</button>
                <div id="score-1" class="score-box"></div>
            </div>
            <!-- 2모둠 -->
            <div class="team-card">
                <div class="team-title">2모둠</div>
                <div id="result-2" class="result-box">-</div>
                <button id="stop-2" class="stop-btn" onclick="stopTeam(2)" disabled>멈춰!</button>
                <div id="score-2" class="score-box"></div>
            </div>
            <!-- 3모둠 -->
            <div class="team-card">
                <div class="team-title">3모둠</div>
                <div id="result-3" class="result-box">-</div>
                <button id="stop-3" class="stop-btn" onclick="stopTeam(3)" disabled>멈춰!</button>
                <div id="score-3" class="score-box"></div>
            </div>
            <!-- 4모둠 -->
            <div class="team-card">
                <div class="team-title">4모둠</div>
                <div id="result-4" class="result-box">-</div>
                <button id="stop-4" class="stop-btn" onclick="stopTeam(4)" disabled>멈춰!</button>
                <div id="score-4" class="score-box"></div>
            </div>
            <!-- 5모둠 -->
            <div class="team-card">
                <div class="team-title">5모둠</div>
                <div id="result-5" class="result-box">-</div>
                <button id="stop-5" class="stop-btn" onclick="stopTeam(5)" disabled>멈춰!</button>
                <div id="score-5" class="score-box"></div>
            </div>
        </div>
        
        <div style="text-align: center; color: gray; margin-top: 5px; font-size: 0.9em;">
            시간이 기록되면 상단 박스가 연한 녹색으로 변합니다.
        </div>
    </div>

    <script>
        const NUM_TEAMS = 5;
        const TARGET_TIME = 31.4;
        let startTime = 0;
        let teamData = {}; 
        let stoppedCount = 0;
        let isRunning = false;

        function initGame() {
            stoppedCount = 0;
            isRunning = false;
            teamData = {};
            
            document.getElementById('start-btn').disabled = false;
            document.getElementById('start-btn').innerText = "타이머 시작";

            for(let i=1; i<=NUM_TEAMS; i++) {
                teamData[i] = { stopped: false, time: 0 };
                document.getElementById(`stop-${i}`).disabled = true;
                document.getElementById(`result-${i}`).innerText = "-";
                document.getElementById(`result-${i}`).classList.remove('bg-stopped');
                document.getElementById(`score-${i}`).innerText = "";
            }
        }

        function startGame() {
            initGame();
            isRunning = true;
            startTime = Date.now();
            
            document.getElementById('start-btn').disabled = true;
            document.getElementById('start-btn').innerText = "게임 진행 중...";
            
            for(let i=1; i<=NUM_TEAMS; i++) {
                document.getElementById(`stop-${i}`).disabled = false;
            }
        }

        function stopTeam(id) {
            if (!isRunning || teamData[id].stopped) return;

            const now = Date.now();
            const elapsed = (now - startTime) / 1000;
            
            teamData[id].stopped = true;
            teamData[id].time = elapsed;
            stoppedCount++;

            document.getElementById(`stop-${id}`).disabled = true;
            document.getElementById(`result-${id}`).classList.add('bg-stopped');
            document.getElementById(`result-${id}`).innerText = "기록 완료";

            if (stoppedCount === NUM_TEAMS) {
                endGame();
            }
        }

        function endGame() {
            isRunning = false;
            document.getElementById('start-btn').innerText = "결과 확인";
            
            let results = [];

            for(let i=1; i<=NUM_TEAMS; i++) {
                let t = teamData[i].time;
                let displayBox = document.getElementById(`result-${i}`);
                let scoreBox = document.getElementById(`score-${i}`);
                
                let timeText = t.toFixed(2) + "초";
                let diff = Math.abs(t - TARGET_TIME);

                if (t > TARGET_TIME) {
                    displayBox.innerText = timeText + "\\n(초과: 0점)";
                    results.push({id: i, diff: 9999, valid: false}); 
                } else {
                    displayBox.innerText = timeText + "\\n(오차: " + diff.toFixed(2) + ")";
                    results.push({id: i, diff: diff, valid: true});
                }
            }

            let validResults = results.filter(r => r.valid);
            validResults.sort((a, b) => a.diff - b.diff);

            const points = [3, 2, 1];
            
            validResults.forEach((item, index) => {
                if (index < points.length) {
                    document.getElementById(`score-${item.id}`).innerText = points[index] + "점";
                } else {
                    document.getElementById(`score-${item.id}`).innerText = "0점";
                }
            });
            
            results.filter(r => !r.valid).forEach(item => {
                document.getElementById(`score-${item.id}`).innerText = "0점";
            });

            document.getElementById('start-btn').disabled = false;
            document.getElementById('start-btn').innerText = "다시 시작하기";
        }

        initGame();
    </script>
</body>
</html>
"""

components.html(game_html, height=370)

st.write("---")
st.write("##### [게임 방법]")
st.markdown("""
- 각 팀에 한 명씩 나와서 전자칠판 앞에 나온다.
- **[타이머 시작]** 을 누르면 모든 모둠의 타이머가 **동시에 시작**됩니다.  \n\
  (화면에는 표시되지 않아요!)
- 각 모둠은 **31.4초**에 가장 가깝다고 생각될 때 자신의 모둠 번호 아래  **[멈춰!]**  클릭!
- **모든 모둠**이 '멈춰!'를 누르면, 각 모둠의 **측정 시간**과 **점수**가 표시됩니다.(총 5번 진행)
""")

col1, col2 = st.columns(2)
with col1:
    st.write("##### [점수 부여]")
    st.markdown("""
    - 31.4초를 지난 학생은 0점!
    - 31.4초에 가장 근접한 학생은 3점!!!
    - 31.4초에 두 번째로 근접한 학생은 2점!!
    - 31.4초에 세 번째로 근접한 학생에게 1점!    
    """)