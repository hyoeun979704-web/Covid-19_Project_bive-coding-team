import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정 (화면을 꽉 채우기 위해 필수)
st.set_page_config(layout="wide", page_title="2,195일간의 여정", page_icon="🦠")

# 2. Streamlit 고유의 여백/헤더 제거 (완벽한 전체화면을 위해)
st.markdown("""
<style>
    /* Streamlit 기본 UI 숨기기 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 여백 제거하여 화면 꽉 채우기 */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    
    /* iframe 테두리 제거 */
    iframe {
        border: none;
        width: 100vw;
        height: 100vh;
    }
    
    /* 배경색 강제 지정 */
    .stApp {
        background-color: #000000;
    }
</style>
""", unsafe_allow_html=True)

# 3. 원본 웹 소스코드 통합 (HTML + CSS + JS)
# 파일 로딩 없이 이 문자열 자체가 웹사이트입니다.
html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>코로나19 연대기</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    
    <style>
        /* [스타일 복원] Netlify 버전의 CSS 디자인 */
        :root {
            --bg-color: #000000;
            --text-main: #ffffff;
            --text-sub: #94a3b8;
            --accent: #3b82f6;
            --glass: rgba(15, 23, 42, 0.6);
            --border: rgba(255, 255, 255, 0.1);
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'Noto Sans KR', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            overflow-x: hidden; /* 가로 스크롤 방지 */
        }

        /* 1. 히어로 섹션 (제목) */
        .hero-section {
            position: absolute;
            top: 0; left: 0; width: 100%;
            padding: 40px;
            z-index: 10;
            pointer-events: none; /* 클릭 통과 */
            background: linear-gradient(to bottom, rgba(0,0,0,0.8), transparent);
        }
        .hero-title {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(to right, #fff, #a5b4fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .hero-subtitle {
            font-size: 1.2rem;
            color: var(--text-sub);
        }

        /* 2. 지구본 레이아웃 */
        #section-globe {
            position: relative;
            width: 100%;
            height: 100vh;
            overflow: hidden;
        }
        
        #globe-container {
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0; left: 0;
            z-index: 1;
        }

        /* 3. 플로팅 스탯 카드 (왼쪽 위) */
        .stats-sidebar {
            position: absolute;
            top: 180px;
            left: 40px;
            width: 280px;
            z-index: 5;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .stat-card-large {
            background: var(--glass);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: transform 0.3s;
        }
        .stat-card-large:hover { transform: translateX(5px); background: rgba(30, 41, 59, 0.8); }
        
        .stat-icon { font-size: 24px; }
        .stat-label { font-size: 0.9rem; color: var(--text-sub); margin-bottom: 4px; }
        .stat-value { font-size: 1.5rem; font-weight: 700; color: #fff; }
        .stat-value-accent { color: #ef4444; }

        /* 4. 타임라인 컨트롤 (하단 중앙) */
        .timeline-control-new {
            position: absolute;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            width: 80%;
            max-width: 800px;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 20px 30px;
            z-index: 10;
        }
        
        .timeline-header {
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;
        }
        .timeline-date { font-size: 1.5rem; font-weight: bold; color: var(--accent); }
        
        .control-buttons { display: flex; gap: 15px; align-items: center; }
        .control-btn {
            background: var(--accent); color: white; border: none;
            padding: 8px 20px; border-radius: 20px; cursor: pointer; font-weight: bold;
            display: flex; align-items: center; gap: 5px; transition: 0.2s;
        }
        .control-btn:hover { background: #2563eb; transform: scale(1.05); }
        
        input[type=range] { width: 100%; cursor: pointer; accent-color: var(--accent); }

        /* 5. 섹션 스타일 (스크롤 시 나타나는 내용) */
        .page-section {
            position: relative;
            min-height: 100vh;
            padding: 100px 40px;
            background: linear-gradient(to bottom, #000, #0f172a);
            border-top: 1px solid var(--border);
            z-index: 2;
        }
        
        .section-title { font-size: 2.5rem; margin-bottom: 10px; color: white; }
        .section-subtitle { color: var(--text-sub); margin-bottom: 50px; font-size: 1.1rem; }
        
        .card-grid-2 {
            display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 50px;
        }
        
        .metric-card {
            background: #1e293b; border-radius: 20px; padding: 25px;
            border: 1px solid var(--border); height: 400px;
        }
        .metric-card__header { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
        .metric-card__title { font-size: 1.2rem; font-weight: bold; }
        .metric-card__body { width: 100%; height: 320px; position: relative; }

        /* 6. 바이러스 섹션 */
        .virus-layout { display: flex; gap: 40px; height: 600px; }
        .virus-card { flex: 2; position: relative; background: radial-gradient(circle at center, #1e293b 0%, #000 70%); border-radius: 30px; overflow: hidden; }
        #virus-canvas-container { width: 100%; height: 100%; }
        
        .structure-controls-new {
            position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%);
            display: flex; gap: 10px; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 30px;
        }
        .struct-btn {
            background: transparent; border: 1px solid rgba(255,255,255,0.3); color: white;
            padding: 8px 16px; border-radius: 20px; cursor: pointer; display: flex; align-items: center; gap: 6px;
        }
        .struct-btn.active, .struct-btn:hover { background: var(--accent); border-color: var(--accent); }
        .struct-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }

        .virus-info-sidebar { flex: 1; display: flex; flex-direction: column; gap: 20px; }
        .info-card { background: #1e293b; padding: 20px; border-radius: 20px; border: 1px solid var(--border); }
        .variant-btn {
            background: #334155; border: none; color: #cbd5e1; padding: 6px; border-radius: 6px; cursor: pointer;
        }
        .variant-btn.active { background: var(--accent); color: white; }

        /* 로딩 스크린 */
        .loading-screen {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: #000; z-index: 9999; display: flex; justify-content: center; align-items: center;
            flex-direction: column; transition: opacity 0.5s;
        }
        .loading-screen.hidden { opacity: 0; pointer-events: none; }
        .virus-loader { font-size: 5rem; animation: spin 2s linear infinite; margin-bottom: 20px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>

    <div id="loading-screen" class="loading-screen">
        <div class="virus-loader">🦠</div>
        <h2 style="color:white;">데이터 로딩 중...</h2>
    </div>

    <section class="hero-section">
        <h1 class="hero-title">2,195일간의 여정</h1>
        <p class="hero-subtitle">코로나19 연대기: 전 세계 확산 과정을 3D로 추적합니다.</p>
    </section>

    <section id="section-globe">
        <div id="globe-container"></div>
        
        <div class="stats-sidebar">
            <div class="stat-card-large">
                <div class="stat-icon">📅</div>
                <div>
                    <div class="stat-label">현재 날짜</div>
                    <div class="stat-value" id="current-date">Loading...</div>
                </div>
            </div>
            <div class="stat-card-large">
                <div class="stat-icon">🦠</div>
                <div>
                    <div class="stat-label">누적 확진자</div>
                    <div class="stat-value stat-value-accent" id="total-cases">0</div>
                </div>
            </div>
            <div class="stat-card-large">
                <div class="stat-icon">💀</div>
                <div>
                    <div class="stat-label">사망자</div>
                    <div class="stat-value" id="total-deaths">0</div>
                </div>
            </div>
        </div>

        <div class="timeline-control-new">
            <div class="timeline-header">
                <span class="timeline-label" style="color:#cbd5e1">타임라인</span>
                <span class="timeline-date" id="current-date-main">2020-01-22</span>
                <button class="control-btn" id="play-btn">▶ 재생</button>
            </div>
            <input type="range" id="timeline-slider" min="0" max="100" value="0">
        </div>
    </section>

    <section class="page-section">
        <h2 class="section-title">📊 데이터 분석</h2>
        <div class="card-grid-2">
            <div class="metric-card">
                <div class="metric-card__header"><span class="metric-icon">📉</span><div class="metric-card__title">전 세계 확진자 추이</div></div>
                <div class="metric-card__body"><canvas id="chart-cases"></canvas></div>
            </div>
            <div class="metric-card">
                <div class="metric-card__header"><span class="metric-icon">💔</span><div class="metric-card__title">전 세계 사망자 추이</div></div>
                <div class="metric-card__body"><canvas id="chart-deaths"></canvas></div>
            </div>
        </div>
    </section>

    <section class="page-section">
        <h2 class="section-title">🧬 SARS-CoV-2 구조 탐색</h2>
        <div class="virus-layout">
            <div class="virus-card">
                <div id="virus-canvas-container"></div>
                <div class="structure-controls-new">
                    <button class="struct-btn active" onclick="highlight('all')"><span class="struct-dot" style="background:#fff"></span>전체</button>
                    <button class="struct-btn" onclick="highlight('spike')"><span class="struct-dot" style="background:#e91e63"></span>스파이크</button>
                    <button class="struct-btn" onclick="highlight('envelope')"><span class="struct-dot" style="background:#f97316"></span>외막</button>
                    <button class="struct-btn" onclick="highlight('lipid')"><span class="struct-dot" style="background:#334155"></span>지질막</button>
                </div>
            </div>
            <div class="virus-info-sidebar">
                <div class="info-card">
                    <h3 style="color:#3b82f6; margin-bottom:10px;">변이 바이러스 선택</h3>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:5px;">
                        <button class="variant-btn active" onclick="changeVariant('original')">초기형</button>
                        <button class="variant-btn" onclick="changeVariant('delta')">델타</button>
                        <button class="variant-btn" onclick="changeVariant('omicron')">오미크론</button>
                    </div>
                </div>
                <div class="info-card">
                    <h3 id="v-title" style="color:white; margin-bottom:10px;">초기형 (Original)</h3>
                    <p id="v-desc" style="color:#cbd5e1; font-size:0.9rem;">2019년 말 우한에서 발견된 원형 바이러스입니다.</p>
                </div>
            </div>
        </div>
    </section>

    <script>
        // --- 1. 데이터 로드 (API 사용) ---
        let timelineData = [];
        const cities = [
            {name: "Wuhan", lat: 30.5928, lng: 114.3055, isOrigin: true},
            {name: "Seoul", lat: 37.5665, lng: 126.9780},
            {name: "New York", lat: 40.7128, lng: -74.0060},
            {name: "London", lat: 51.5074, lng: -0.1278},
            {name: "Paris", lat: 48.8566, lng: 2.3522},
            {name: "Tokyo", lat: 35.6762, lng: 139.6503}
        ];

        async function initApp() {
            try {
                // API 호출
                const res = await fetch('https://disease.sh/v3/covid-19/historical/all?lastdays=all');
                const data = await res.json();
                
                // 데이터 가공
                const dates = Object.keys(data.cases);
                timelineData = dates.map(date => ({
                    date: date,
                    cases: data.cases[date],
                    deaths: data.deaths[date]
                }));

                // 로딩 제거 및 초기화
                document.getElementById('loading-screen').classList.add('hidden');
                setTimeout(() => document.getElementById('loading-screen').remove(), 500);

                initGlobe();
                initCharts();
                initVirus();

            } catch (e) {
                console.error(e);
                alert("데이터 로드 실패. 새로고침 해주세요.");
            }
        }

        // --- 2. 지구본 (Three.js) ---
        function initGlobe() {
            const container = document.getElementById('globe-container');
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 4000);
            camera.position.z = 250;
            
            const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);
            
            scene.add(new THREE.AmbientLight(0xffffff, 0.6));
            const sun = new THREE.DirectionalLight(0xfff8e1, 1.2);
            sun.position.set(100, 50, 50);
            scene.add(sun);
            
            const earthGroup = new THREE.Group();
            scene.add(earthGroup);
            const loader = new THREE.TextureLoader();
            
            // 지구 & 구름
            const earth = new THREE.Mesh(
                new THREE.SphereGeometry(80, 64, 64),
                new THREE.MeshPhongMaterial({
                    map: loader.load('https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/earth_atmos_2048.jpg'),
                    specular: new THREE.Color(0x333333),
                    shininess: 10
                })
            );
            earthGroup.add(earth);
            
            const clouds = new THREE.Mesh(
                new THREE.SphereGeometry(80.5, 64, 64),
                new THREE.MeshPhongMaterial({
                    map: loader.load('https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/earth_clouds_1024.png'),
                    transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending
                })
            );
            earthGroup.add(clouds);
            
            // 도시 마커
            const markers = [];
            cities.forEach(c => {
                const phi = (90 - c.lat) * (Math.PI / 180);
                const theta = (c.lng + 180) * (Math.PI / 180);
                const r = 80;
                const x = -(r * Math.sin(phi) * Math.cos(theta));
                const y = (r * Math.cos(phi));
                const z = (r * Math.sin(phi) * Math.sin(theta));
                
                const mesh = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.5, 0.5, 5, 8),
                    new THREE.MeshBasicMaterial({ color: 0xff3366 })
                );
                mesh.position.set(x, y, z);
                mesh.lookAt(0,0,0);
                mesh.rotateX(Math.PI/2);
                mesh.translateY(2.5);
                earthGroup.add(mesh);
                markers.push({mesh, phase: Math.random() * Math.PI});
            });

            // 컨트롤 로직
            let playing = false;
            let index = 0;
            const slider = document.getElementById('timeline-slider');
            const playBtn = document.getElementById('play-btn');
            
            if(timelineData.length > 0) slider.max = timelineData.length - 1;
            
            playBtn.onclick = () => {
                playing = !playing;
                playBtn.innerText = playing ? "⏸ 정지" : "▶ 재생";
            };
            
            slider.oninput = (e) => {
                playing = false;
                index = parseInt(e.target.value);
                updateUI();
            };

            function updateUI() {
                if(!timelineData[index]) return;
                const d = timelineData[index];
                document.getElementById('current-date').innerText = d.date;
                document.getElementById('current-date-main').innerText = d.date;
                document.getElementById('total-cases').innerText = d.cases.toLocaleString();
                document.getElementById('total-deaths').innerText = d.deaths.toLocaleString();
            }

            function animate() {
                requestAnimationFrame(animate);
                earthGroup.rotation.y += 0.001;
                clouds.rotation.y += 0.0012;
                
                // 마커 펄스
                const time = Date.now() * 0.003;
                markers.forEach(m => {
                    const s = 1 + Math.sin(time + m.phase) * 0.3;
                    m.mesh.scale.set(1, s, 1);
                });
                
                if(playing && index < timelineData.length - 1) {
                    index++;
                    slider.value = index;
                    updateUI();
                }
                renderer.render(scene, camera);
            }
            animate();
            updateUI(); // 초기값 표시
            
            window.addEventListener('resize', () => {
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            });
        }

        // --- 3. 차트 (Chart.js) ---
        function initCharts() {
            const ctx1 = document.getElementById('chart-cases').getContext('2d');
            new Chart(ctx1, {
                type: 'line',
                data: {
                    labels: timelineData.map(d => d.date),
                    datasets: [{
                        label: '확진자',
                        data: timelineData.map(d => d.cases),
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        fill: true, tension: 0.4, pointRadius: 0
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: {legend:{display:false}}, scales:{x:{display:false}, y:{grid:{color:'rgba(255,255,255,0.1)'}}} }
            });

            const ctx2 = document.getElementById('chart-deaths').getContext('2d');
            new Chart(ctx2, {
                type: 'line',
                data: {
                    labels: timelineData.map(d => d.date),
                    datasets: [{
                        label: '사망자',
                        data: timelineData.map(d => d.deaths),
                        borderColor: '#ef4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        fill: true, tension: 0.4, pointRadius: 0
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: {legend:{display:false}}, scales:{x:{display:false}, y:{grid:{color:'rgba(255,255,255,0.1)'}}} }
            });
        }

        // --- 4. 바이러스 (Three.js) ---
        let virusGroup, virusParts = [];
        function initVirus() {
            const container = document.getElementById('virus-canvas-container');
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.z = 15;
            
            const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.appendChild(renderer.domElement);
            
            scene.add(new THREE.AmbientLight(0xffffff, 0.6));
            const light = new THREE.DirectionalLight(0xffffff, 1);
            light.position.set(10, 10, 10);
            scene.add(light);
            
            buildVirus('original'); // 초기 생성
            
            function animate() {
                requestAnimationFrame(animate);
                if(virusGroup) {
                    virusGroup.rotation.y += 0.002;
                    virusGroup.rotation.x += 0.001;
                }
                renderer.render(scene, camera);
            }
            animate();
        }

        function buildVirus(type) {
            // 기존 삭제 로직은 생략하고 새로고침 방식 사용
            // 여기서는 간단히 그룹만 교체
            // (실제로는 씬에서 제거 필요)
        }
        
        // window 객체에 함수 등록 (HTML onclick에서 쓰기 위해)
        window.highlight = function(part) {
            // 버튼 스타일
            document.querySelectorAll('.struct-btn').forEach(b => b.classList.remove('active'));
            event.currentTarget.classList.add('active');
            // 로직 구현... (시각적 효과)
        };
        
        window.changeVariant = function(v) {
            document.querySelectorAll('.variant-btn').forEach(b => b.classList.remove('active'));
            event.currentTarget.classList.add('active');
            
            const titles = {original: "초기형 (Original)", delta: "델타 (Delta)", omicron: "오미크론 (Omicron)"};
            const descs = {
                original: "2019년 말 우한에서 발견된 원형 바이러스입니다.",
                delta: "2020년 인도 발견. 강력한 독성과 전파력을 가졌습니다.",
                omicron: "2021년 남아공 발견. 전파력이 매우 강하나 치명률은 낮습니다."
            };
            document.getElementById('v-title').innerText = titles[v];
            document.getElementById('v-desc').innerText = descs[v];
        };

        // 앱 시작
        initApp();
    </script>
</body>
</html>
"""

# 4. Streamlit에 HTML 전체 렌더링 (높이 3000px로 스크롤 가능하게)
components.html(html_code, height=2500, scrolling=False)
