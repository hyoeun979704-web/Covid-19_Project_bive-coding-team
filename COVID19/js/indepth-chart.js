// js/indepth-chart.js

export function initIndepthChart() {
    const timelineCanvas = document.getElementById('chart-variant-timeline');
    const cfrCanvas = document.getElementById('chart-variant-cfr');

    if (!timelineCanvas || !cfrCanvas) return;

    console.log('🧬 심층 분석(변이) 차트 로딩 중...');

    // 데이터셋 (제공해주신 데이터)
    // js/indepth-chart.js

    const variantData = [
        // [수정] 델타: 강렬한 붉은색 (위험 강조)
        { name: '델타 (Delta)', start: '2021.07.25', end: '2022.01.15', duration: 174, cfr: 0.95, symptom: '후각상실, 고열', color: '#EF4444' },

        // [수정] 오미크론 초기: 선명한 파란색
        { name: '오미크론 BA.1/2', start: '2022.01.16', end: '2022.07.09', duration: 174, cfr: 0.10, symptom: '인후통, 피로감', color: '#3B82F6' },

        // [수정] 오미크론 중기: 청록색 (Teal)
        { name: '오미크론 BA.5', start: '2022.07.24', end: '2022.12.31', duration: 160, cfr: 0.07, symptom: '콧물, 두통', color: '#10B981' },

        // [수정] 오미크론 후기: 보라색
        { name: '오미크론 BN.1', start: '2023.01.22', end: '2023.03.25', duration: 62, cfr: 0.10, symptom: '쉰 목소리', color: '#8B5CF6' },

        // [수정] 통합: 주황색
        { name: '오미크론 XBB', start: '2023.04.16', end: '2023.07.31', duration: 106, cfr: 0.04, symptom: '가벼운 증상', color: '#F59E0B' }
    ];

    // 공통 옵션
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: 'rgba(15, 23, 42, 0.95)',
                padding: 12,
                titleColor: '#fff',
                bodyColor: '#cbd5e1',
                cornerRadius: 8
            }
        },
        scales: {
            x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#8b9db8' } },
            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#8b9db8' } }
        }
    };

    // 1. 변이별 우세 지속 기간 차트 (Bar)
    new Chart(timelineCanvas, {
        type: 'bar',
        data: {
            labels: variantData.map(v => v.name),
            datasets: [{
                data: variantData.map(v => v.duration),
                backgroundColor: variantData.map(v => v.color),
                borderRadius: 6,
                barThickness: 25
            }]
        },
        options: {
            ...commonOptions,
            indexAxis: 'y', // 가로 막대
            plugins: {
                ...commonOptions.plugins,
                tooltip: {
                    ...commonOptions.plugins.tooltip,
                    callbacks: {
                        label: function (ctx) {
                            const v = variantData[ctx.dataIndex];
                            return [` 기간: ${v.duration}일`, ` 증상: ${v.symptom}`];
                        }
                    }
                }
            },
            scales: {
                ...commonOptions.scales,
                y: { ticks: { color: '#f1f5f9', font: { weight: '600', size: 11 } } }
            }
        }
    });

    // 2. 치명률(CFR) 변화 추이 차트 (Line)
    new Chart(cfrCanvas, {
        type: 'line',
        data: {
            labels: variantData.map(v => v.name),
            datasets: [{
                data: variantData.map(v => v.cfr),
                borderColor: '#BF5AF2',
                borderWidth: 3,
                pointRadius: 6,
                pointBackgroundColor: variantData.map(v => v.color),
                tension: 0.3,
                fill: false
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    beginAtZero: true,
                    title: { display: true, text: '치명률 (%)', color: '#64748b' }
                },
                x: { ticks: { display: false } } // X축 라벨은 공간상 생략하거나 간소화
            }
        }
    });
}