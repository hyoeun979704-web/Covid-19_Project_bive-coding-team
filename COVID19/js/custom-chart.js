// js/custom-chart.js

// 1. 변곡점 데이터
const inflectionData = {
    'China': [
        { date: '2020-02', reason: 'Wuhan outbreak peak (우한 유행 정점)' },
        { date: '2022-03', reason: 'Omicron surge with lockdowns (오미크론 봉쇄)' }
    ],
    'United States of America': [
        { date: '2020-04', reason: 'First wave nationwide (1차 전국 유행)' },
        { date: '2020-12', reason: 'Winter surge - Alpha (알파 변이)' },
        { date: '2021-08', reason: 'Delta variant wave (델타 변이)' },
        { date: '2022-01', reason: 'Omicron surge peak (오미크론 정점)' }
    ],
    'Italy': [
        { date: '2020-03', reason: 'Europe first outbreak (유럽 최초 확산)' },
        { date: '2020-10', reason: 'Second wave (2차 유행)' },
        { date: '2021-11', reason: 'Delta variant surge (델타 유행)' }
    ],
    'Republic of Korea': [
        { date: '2020-02', reason: 'Daegu Shincheonji cluster (대구 신천지)' },
        { date: '2021-12', reason: 'Omicron breakthrough (오미크론 확산)' },
        { date: '2022-03', reason: 'Omicron peak (오미크론 정점)' }
    ],
    'India': [
        { date: '2021-05', reason: 'Delta catastrophic surge (델타 대유행)' },
        { date: '2022-01', reason: 'Omicron wave (오미크론 유행)' }
    ],
    'Brazil': [
        { date: '2021-03', reason: 'Gamma variant surge (감마 변이)' },
        { date: '2022-01', reason: 'Omicron wave (오미크론 유행)' }
    ]
};

// 2. 국가별 색상 팔레트
const countryColors = {
    'China': '#E74C3C',                      // Red
    'United States of America': '#3498DB',   // Blue
    'Italy': '#2ECC71',                      // Green
    'Republic of Korea': '#9B59B6',          // Purple
    'India': '#F39C12',                      // Orange
    'Brazil': '#1ABC9C'                      // Teal
};

// 3. [추가] 국가명 한글 매핑
const countryNameMap = {
    'China': '중국',
    'United States of America': '미국',
    'Italy': '이탈리아',
    'Republic of Korea': '대한민국',
    'India': '인도',
    'Brazil': '브라질',
    'United Kingdom': '영국',
    'France': '프랑스',
    'Germany': '독일'
};

export function initInflectionChart() {
    const canvas = document.getElementById('chart-monthly-comparison');
    if (!canvas) return;

    console.log('📊 변곡점 분석 차트 로딩 중...');

    // CSV 데이터 로드
    Papa.parse('data/covid19_monthly_cases_by_country.csv', {
        download: true,
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        complete: function (results) {
            const data = results.data;
            if (!data || data.length === 0) {
                console.error("데이터 로드 실패");
                return;
            }
            renderInflectionChart(canvas, data);
        },
        error: function (err) {
            console.error("CSV 에러:", err);
        }
    });
}

function renderInflectionChart(canvas, rawData) {
    // 1. 데이터 가공
    const countries = Object.keys(inflectionData);
    const countryDataMap = {};

    countries.forEach(country => {
        countryDataMap[country] = rawData
            .filter(row => row.Country === country)
            .sort((a, b) => new Date(a.year_month) - new Date(b.year_month));
    });

    // X축 라벨 생성
    let allDates = new Set();
    Object.values(countryDataMap).forEach(rows => {
        rows.forEach(r => allDates.add(r.year_month));
    });
    const labels = Array.from(allDates).sort();

    // 2. 차트 데이터셋 생성
    const datasets = [];

    countries.forEach(country => {
        const rows = countryDataMap[country];
        if (!rows || rows.length === 0) return;

        const color = countryColors[country];
        // [수정] 한글 이름 적용
        const koName = countryNameMap[country] || country;

        // (1) 기본 라인 차트 데이터 생성
        const lineData = labels.map(date => {
            const row = rows.find(r => r.year_month === date);
            return row ? row.Cumulative_cases : null;
        });

        datasets.push({
            type: 'line',
            label: koName, // 한글 이름 사용
            data: lineData,
            borderColor: color,
            backgroundColor: color,
            borderWidth: 2,
            tension: 0.4,
            pointRadius: 0,
            pointHoverRadius: 4,
            yAxisID: 'y'
        });

        // (2) 변곡점 마커 데이터 생성
        const scatterData = labels.map(date => {
            const point = inflectionData[country].find(p => date.startsWith(p.date));
            if (point) {
                const row = rows.find(r => r.year_month === date);
                return row ? row.Cumulative_cases : null;
            }
            return null;
        });

        // 툴팁용 메타 데이터
        const tooltips = labels.map(date => {
            const point = inflectionData[country].find(p => date.startsWith(p.date));
            return point ? point.reason : null;
        });

        datasets.push({
            type: 'line',
            label: `${koName} 이벤트`, // 범례 이름도 한글화
            data: scatterData,
            borderColor: color,
            backgroundColor: '#ffffff',
            borderWidth: 2,
            pointStyle: 'rectRot',
            pointRadius: 6,
            pointHoverRadius: 9,
            showLine: false,
            events: tooltips,
            yAxisID: 'y'
        });
    });

    // 3. 차트 그리기
    new Chart(canvas, {
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'nearest',
                intersect: false,
                axis: 'x'
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#cbd5e1',
                        usePointStyle: true,
                        filter: function (item) {
                            // 이벤트 마커는 범례에서 숨김 (깔끔하게)
                            return !item.text.includes('이벤트');
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#fff',
                    bodyColor: '#94a3b8',
                    padding: 10,
                    cornerRadius: 8,
                    callbacks: {
                        title: (items) => items[0].label,
                        label: function (context) {
                            const dataset = context.dataset;
                            const value = context.raw;

                            if (dataset.label.includes('이벤트')) {
                                const reason = dataset.events[context.dataIndex];
                                const countryName = dataset.label.split(' ')[0];
                                return `💎 ${countryName}: ${reason}`;
                            }
                            return ` ${dataset.label}: ${value.toLocaleString()}명`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#64748b' }
                },
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: {
                        color: '#64748b',
                        callback: function (value) {
                            return (value / 1000000).toFixed(0) + 'M';
                        }
                    },
                    beginAtZero: true
                }
            }
        }
    });
}