import pandas as pd
import webbrowser
import os

# 1. 시각화용 HTML 코드 (Chart.js 포함)
html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>코로나19 변이 분석 대시보드</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Noto Sans KR', sans-serif; background: #0a1628; color: #e8edf4; padding: 20px; ㄴ}
        .container { max-width: 1400px; margin: 0 auto; }
        header { margin-bottom: 30px; border-left: 6px solid #BF5AF2; padding-left: 20px; }
        h1 { font-size: 2rem; color: #ffffff; }
        .subtitle { color: #8b9db8; margin-top: 5px; }
        .grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
        .chart-section {
            background: linear-gradient(135deg, #1a2942 0%, #152235 100%);
            border-radius: 20px; padding: 35px; border: 1px solid rgba(139, 157, 184, 0.2);
        }
        .section-title { font-size: 1.4rem; margin-bottom: 20px; color: #BF5AF2; font-weight: 700; }
        .chart-container { position: relative; height: 480px; }
        .axis-label { font-size: 0.85rem; color: #8b9db8; margin-top: 15px; text-align: center; }
        .stats-info { margin-top: 20px; padding: 15px; background: rgba(0,0,0,0.2); border-radius: 10px; font-size: 0.9rem; line-height: 1.6; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>변이 바이러스 분석 (델타 vs 오미크론 계열)</h1>
            <p class="subtitle">질병관리청 논문 기준: 오미크론 세부 계통별 우세 시기 및 특징 비교</p>
        </header>

        <div class="grid-container">
            <div class="chart-section">
                <h2 class="section-title">변이별 우세 지속 기간</h2>
                <div class="chart-container"><canvas id="timelineChart"></canvas></div>
                <p class="axis-label">가로축: 우세 지속 기간 (일) / 세로축: 변이 명칭</p>
            </div>

            <div class="chart-section">
                <h2 class="section-title">치명률(CFR) 변화 추이</h2>
                <div class="chart-container"><canvas id="cfrChart"></canvas></div>
                <p class="axis-label">가로축: 변이 명칭 / 세로축: 치명률 (%)</p>
                <div class="stats-info">
                    <strong>분석 가이드:</strong><br>
                    • <strong>델타:</strong> 높은 치명률(0.95%)과 폐렴 중심의 위중증 유발<br>
                    • <strong>오미크론 계열:</strong> 치명률 급감(0.1% 이하) 및 상기도 감염(인후통) 중심 변화
                </div>
            </div>
        </div>
    </div>

    <script>
        const variantData = [
            { name: '델타 (Delta)', start: '2021.07.25', end: '2022.01.15', duration: 174, cfr: 0.95, symptom: '후각상실, 미각상실, 고열', color: '#FF6B6B' },
            { name: '오미크론 BA.1/BA.2', start: '2022.01.16', end: '2022.07.09', duration: 174, cfr: 0.10, symptom: '극심한 인후통, 기침, 피로감', color: '#BF5AF2' },
            { name: '오미크론 BA.5', start: '2022.07.24', end: '2022.12.31', duration: 160, cfr: 0.07, symptom: '콧물, 인후통, 두통', color: '#9D50BB' },
            { name: '오미크론 BN.1', start: '2023.01.22', end: '2023.03.25', duration: 62, cfr: 0.10, symptom: '인후통, 쉰 목소리, 기침', color: '#6E48AA' },
            { name: '오미크론 XBB (통합)', start: '2023.04.16', end: '2023.07.31', duration: 106, cfr: 0.04, symptom: '가벼운 호흡기 증상, 근육통', color: '#C299FF' }
        ];

        const tlCtx = document.getElementById('timelineChart').getContext('2d');
        new Chart(tlCtx, {
            type: 'bar',
            data: {
                labels: variantData.map(v => v.name),
                datasets: [{
                    data: variantData.map(v => v.duration),
                    backgroundColor: variantData.map(v => v.color),
                    borderRadius: 8,
                    barThickness: 35
                }]
            },
            options: {
                indexAxis: 'y', responsive: true, maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        padding: 15,
                        callbacks: {
                            label: function(context) {
                                const v = variantData[context.dataIndex];
                                return [`기간: ${v.duration}일`, `시작일: ${v.start}`, `종료일: ${v.end}`, `주요 증상: ${v.symptom}`];
                            }
                        }
                    }
                },
                scales: {
                    x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#8b9db8' } },
                    y: { ticks: { color: '#ffffff', font: { weight: '700' } } }
                }
            }
        });

        const cfrCtx = document.getElementById('cfrChart').getContext('2d');
        new Chart(cfrCtx, {
            type: 'line',
            data: {
                labels: variantData.map(v => v.name),
                datasets: [{
                    data: variantData.map(v => v.cfr),
                    borderColor: '#BF5AF2',
                    borderWidth: 4,
                    pointRadius: 10,
                    pointBackgroundColor: variantData.map(v => v.color),
                    tension: 0.3,
                    fill: false
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#8b9db8' } },
                    x: { ticks: { color: '#8b9db8', font: { size: 10 } } }
                }
            }
        });
    </script>
</body>
</html>
"""

# 2. 실행 시 HTML 파일을 생성하고 브라우저로 열어주는 로직
if __name__ == "__main__":
    file_name = "covid_dashboard.html"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"대시보드가 {file_name} 파일로 생성되었습니다.")
    webbrowser.open('file://' + os.path.realpath(file_name))