// js/charts.js - 개선된 버전 (통일된 차트 스타일)

export function initCharts(data) {
    if (!data) return;

    // 통일된 차트 스타일
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: {
                    color: '#94a3b8',
                    font: {
                        family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                        size: 12,
                        weight: '600'
                    },
                    padding: 16
                }
            },
            tooltip: {
                backgroundColor: 'rgba(15, 23, 42, 0.95)',
                titleColor: '#f1f5f9',
                bodyColor: '#94a3b8',
                borderColor: '#3b82f6',
                borderWidth: 1,
                padding: 12,
                cornerRadius: 8,
                titleFont: {
                    size: 13,
                    weight: 'bold'
                },
                bodyFont: {
                    size: 12
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: '#64748b',
                    font: { size: 11 }
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.06)',
                    borderColor: 'rgba(255, 255, 255, 0.1)'
                }
            },
            y: {
                ticks: {
                    color: '#64748b',
                    font: { size: 11 }
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.06)',
                    borderColor: 'rgba(255, 255, 255, 0.1)'
                }
            }
        }
    };

    // 1. Global Timeline - Confirmed Cases
    new Chart(document.getElementById('chart-global-cases'), {
        type: 'line',
        data: {
            labels: data.timeline.map(d => d.date),
            datasets: [{
                label: 'Confirmed Cases',
                data: data.timeline.map(d => d.cases),
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 4
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    beginAtZero: true
                }
            }
        }
    });

    // 2. Global Timeline - Deaths
    new Chart(document.getElementById('chart-global-deaths'), {
        type: 'line',
        data: {
            labels: data.timeline.map(d => d.date),
            datasets: [{
                label: 'Deaths',
                data: data.timeline.map(d => d.deaths),
                borderColor: '#ec4899',
                backgroundColor: 'rgba(236, 72, 153, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 4
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    beginAtZero: true
                }
            }
        }
    });

    // 3. Symptoms Radar Chart
    new Chart(document.getElementById('chart-symptoms-radar'), {
        type: 'radar',
        data: {
            labels: data.symptoms.labels,
            datasets: [
                {
                    label: 'Delta Variant',
                    data: data.symptoms.delta,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.2)',
                    borderWidth: 2,
                    pointBackgroundColor: '#3b82f6',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#3b82f6'
                },
                {
                    label: 'Omicron Variant',
                    data: data.symptoms.omicron,
                    borderColor: '#06b6d4',
                    backgroundColor: 'rgba(6, 182, 212, 0.2)',
                    borderWidth: 2,
                    pointBackgroundColor: '#06b6d4',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: '#06b6d4'
                }
            ]
        },
        options: {
            ...commonOptions,
            scales: {
                r: {
                    ticks: {
                        color: '#64748b',
                        backdropColor: 'transparent',
                        font: { size: 10 }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    angleLines: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    pointLabels: {
                        color: '#94a3b8',
                        font: { size: 11, weight: '600' }
                    }
                }
            }
        }
    });

    // 4. Symptoms Bar Chart
    new Chart(document.getElementById('chart-symptoms-bar'), {
        type: 'bar',
        data: {
            labels: data.symptoms.labels,
            datasets: [
                {
                    label: 'Delta',
                    data: data.symptoms.delta,
                    backgroundColor: '#3b82f6',
                    borderColor: '#3b82f6',
                    borderWidth: 1,
                    borderRadius: 6
                },
                {
                    label: 'Omicron',
                    data: data.symptoms.omicron,
                    backgroundColor: '#06b6d4',
                    borderColor: '#06b6d4',
                    borderWidth: 1,
                    borderRadius: 6
                }
            ]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    beginAtZero: true
                }
            }
        }
    });

    // 5. Vaccine Efficacy
    new Chart(document.getElementById('chart-vaccine'), {
        type: 'bar',
        data: {
            labels: data.vaccine.labels,
            datasets: [{
                label: 'Efficacy (%)',
                data: data.vaccine.efficacy,
                backgroundColor: [
                    '#10b981',
                    '#06b6d4',
                    '#3b82f6',
                    '#8b5cf6',
                    '#ec4899',
                    '#f59e0b'
                ],
                borderWidth: 0,
                borderRadius: 8
            }]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });

    // 6. Diagnostic Accuracy
    new Chart(document.getElementById('chart-diagnosis'), {
        type: 'line',
        data: {
            labels: data.diagnosis.labels,
            datasets: [
                {
                    label: 'RT-PCR',
                    data: data.diagnosis.pcr,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.3,
                    pointRadius: 4,
                    pointHoverRadius: 6
                },
                {
                    label: 'Rapid Antigen',
                    data: data.diagnosis.antigen,
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.3,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }
            ]
        },
        options: {
            ...commonOptions,
            scales: {
                ...commonOptions.scales,
                y: {
                    ...commonOptions.scales.y,
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}
