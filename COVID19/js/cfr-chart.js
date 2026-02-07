// js/cfr-chart.js

export function initCFRChart() {
    const canvas = document.getElementById('chart-cfr-trends');
    if (!canvas) {
        console.warn('⚠️ CFR 차트 캔버스를 찾을 수 없습니다.');
        return;
    }

    console.log('📉 CFR 차트 생성 중...');

    // CFR 데이터 (분기별)
    const cfrData = {
        labels: [
            '2021 Q3', '2021 Q4',
            '2022 Q1', '2022 Q2', '2022 Q3', '2022 Q4',
            '2023 Q1', '2023 Q2', '2023 Q3'
        ],
        datasets: [
            {
                label: 'Global CFR (%)',
                data: [1.8, 1.5, 0.9, 0.7, 0.5, 0.4, 0.3, 0.3, 0.25],
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 6,
                pointHoverRadius: 9,
                pointBackgroundColor: '#ef4444',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            },
            {
                label: 'Developed Countries (%)',
                data: [1.0, 0.8, 0.5, 0.4, 0.3, 0.2, 0.2, 0.1, 0.1],
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointHoverRadius: 8,
                borderDash: [5, 5]
            },
            {
                label: 'Developing Countries (%)',
                data: [2.8, 2.3, 1.5, 1.2, 0.9, 0.7, 0.6, 0.5, 0.4],
                borderColor: '#f59e0b',
                backgroundColor: 'rgba(245, 158, 11, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 5,
                pointHoverRadius: 8,
                borderDash: [5, 5]
            }
        ]
    };

    // 기존 차트 삭제
    const chartStatus = Chart.getChart(canvas);
    if (chartStatus != undefined) {
        chartStatus.destroy();
    }

    new Chart(canvas, {
        type: 'line',
        data: cfrData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        color: '#1f2937',
                        font: {
                            size: 12,
                            weight: '600'
                        },
                        padding: 15,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#f1f5f9',
                    bodyColor: '#cbd5e1',
                    padding: 12,
                    cornerRadius: 8,
                    displayColors: true,
                    callbacks: {
                        label: function (context) {
                            return `${context.dataset.label}: ${context.parsed.y.toFixed(2)}%`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(156, 163, 175, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#6b7280',
                        font: { size: 11 },
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(156, 163, 175, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#6b7280',
                        font: { size: 11 },
                        callback: function (value) {
                            return value.toFixed(1) + '%';
                        }
                    },
                    title: {
                        display: true,
                        text: 'Case Fatality Rate (%)',
                        color: '#374151',
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    }
                }
            },
            interaction: {
                mode: 'index',
                intersect: false
            }
        }
    });

    console.log('✅ CFR 차트 생성 완료');
}
