// js/variants-timeline.js

// [수정] 인자로 data를 받도록 변경
export function initVariantsTimeline(csvData) {
    const canvas = document.getElementById('chart-variants-timeline');
    if (!canvas) return;

    // 데이터가 없으면 종료
    if (!csvData || csvData.length === 0) {
        console.warn("⚠️ 변이 타임라인 데이터가 없습니다.");
        return;
    }

    console.log('📅 변이 타임라인 차트 생성 중... (CSV 연동)');

    // CSV 데이터를 차트용으로 가공
    // (Start Date와 End Date 사이의 일수 계산)
    const timelineData = csvData.map(d => {
        const start = new Date(d.start_date);
        const end = new Date(d.end_date);
        const diffTime = Math.abs(end - start);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        const months = (diffDays / 30).toFixed(1);

        return {
            name: d.variant,
            start: d.start_date,
            end: d.end_date,
            days: diffDays,
            months: months,
            color: d.color || '#94a3b8' // 색상 없으면 회색
        };
    });

    // 기존 차트가 있다면 삭제 (재로딩 시 중복 방지)
    const chartStatus = Chart.getChart(canvas);
    if (chartStatus != undefined) {
        chartStatus.destroy();
    }

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: timelineData.map(d => d.name),
            datasets: [{
                label: '우세 지속 기간 (일)',
                data: timelineData.map(d => d.days),
                backgroundColor: timelineData.map(d => d.color),
                borderRadius: 8,
                borderWidth: 0,
                barThickness: 40 // 막대 두께 조정
            }]
        },
        options: {
            indexAxis: 'y', // 수평 막대
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#f1f5f9',
                    bodyColor: '#cbd5e1',
                    padding: 12,
                    cornerRadius: 8,
                    displayColors: false,
                    callbacks: {
                        label: function (context) {
                            const d = timelineData[context.dataIndex];
                            return [
                                `기간: ${d.start} ~ ${d.end}`,
                                `지속: ${d.days}일 (약 ${d.months}개월)`
                            ];
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    ticks: { color: '#94a3b8' }
                },
                y: {
                    grid: { display: false },
                    ticks: {
                        color: '#f1f5f9',
                        font: { weight: 'bold' }
                    }
                }
            }
        }
    });
}