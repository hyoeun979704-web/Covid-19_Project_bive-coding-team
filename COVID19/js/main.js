// js/main.js

import { loadData } from './data.js';
import { initGlobe } from './globe.js';
import { initCharts } from './charts.js';
import { initVirus } from './virus.js';
import { initVariantsTimeline } from './variants-timeline.js';

// [중요 수정] 파일명은 custom-chart.js지만, 내보내는 함수는 initInflectionChart입니다.
import { initInflectionChart } from './custom-chart.js';

import { initIndepthChart } from './indepth-chart.js';

// =========================================
// 로딩 화면 및 전역 변수 설정
// =========================================
const covidFacts = [
    "🧼 20초 동안 손을 씻으면 생일 축하 노래를 두 번 부를 수 있어요!",
    "😷 마스크는 패션 아이템이자 생명 보호 아이템! 양쪽 다 챙기세요.",
    "🦠 코로나바이러스는 약 30,000개의 염기쌍을 가진 RNA 바이러스입니다.",
    "🏠 사회적 거리두기 덕분에 우리는 집에서 새로운 취미를 발견했어요!",
    "📊 전 세계가 하나의 목표를 향해 협력한 역사적인 시간이었습니다.",
    "💉 COVID-19 백신은 역사상 가장 빠르게 개발된 백신 중 하나입니다.",
    "🌍 팬데믹은 '모든 사람들'을 뜻하는 그리스어에서 유래했어요.",
    "🧬 변이는 바이러스의 생존 전략이지만, 우리에겐 과학이 있죠!",
    "👨‍⚕️ 전 세계 의료진에게 감사를! 진정한 영웅들입니다.",
    "📱 비대면 기술이 이렇게 빨리 발전할 줄 누가 알았을까요?",
    "🤧 기침 예절: 팔꿈치 안쪽으로! 이제는 상식이 되었죠.",
    "🔬 mRNA 백신 기술은 미래 의학의 게임 체인저가 될 거예요!"
];

let factInterval;
let progressInterval;
let lastFactIndex = -1;

function showRandomFact() {
    const factText = document.getElementById('fact-text');
    if (!factText) return;

    factText.classList.add('text-hidden');

    setTimeout(() => {
        let randomIndex;
        do {
            randomIndex = Math.floor(Math.random() * covidFacts.length);
        } while (randomIndex === lastFactIndex);

        lastFactIndex = randomIndex;
        factText.textContent = covidFacts[randomIndex];
        factText.classList.remove('text-hidden');
    }, 500);
}

function initLoadingScreen() {
    const progressBar = document.getElementById('loading-progress');
    let loadingProgress = 0;

    showRandomFact();

    factInterval = setInterval(() => {
        showRandomFact();
    }, 2000);

    progressInterval = setInterval(() => {
        loadingProgress += Math.random() * 5;
        if (loadingProgress > 95) loadingProgress = 95;
        if (progressBar) progressBar.style.width = loadingProgress + '%';
    }, 200);
}

function hideLoadingScreen() {
    const progressBar = document.getElementById('loading-progress');
    const loadingScreen = document.getElementById('loading-screen');

    clearInterval(factInterval);
    clearInterval(progressInterval);

    if (progressBar) progressBar.style.width = '100%';

    setTimeout(() => {
        if (loadingScreen) {
            loadingScreen.classList.add('hidden');
            setTimeout(() => {
                loadingScreen.remove();
            }, 500);
        }
    }, 500);
}

function initProgressBar() {
    const progressBar = document.getElementById('progressBar');
    if (!progressBar) return;
    window.addEventListener('scroll', () => {
        const windowHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrolled = (window.scrollY / windowHeight) * 100;
        progressBar.style.width = Math.min(scrolled, 100) + '%';
    });
}

function initBackToTop() {
    const backToTop = document.getElementById('backToTop');
    if (!backToTop) return;
    window.addEventListener('scroll', () => {
        backToTop.classList.toggle('visible', window.scrollY > 500);
    });
    backToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// =========================================
// 메인 실행 로직
// =========================================
document.addEventListener('DOMContentLoaded', async () => {
    initLoadingScreen();
    initProgressBar();
    initBackToTop();

    try {
        console.log('📥 데이터 로딩 시작...');

        const minLoadTime = new Promise(resolve => setTimeout(resolve, 3000));
        const dataLoadPromise = loadData();

        const [_, data] = await Promise.all([minLoadTime, dataLoadPromise]);

        window.covidData = data;
        console.log('✅ 데이터 로드 및 최소 대기 시간 완료');

        hideLoadingScreen();

        if (data.timeline && data.timeline.length > 0) {
            initGlobe(data.timeline);
        }

        initCharts(data);
        initVirus();
        initVariantsTimeline(data.variantsTimeline);

        // [핵심 수정] 여기서 initCustomChart()가 아니라 initInflectionChart()를 호출해야 합니다!
        console.log('📊 변곡점 차트 초기화 중...');
        initInflectionChart();

        initIndepthChart();

        console.log('🎉 모든 초기화 완료!');

    } catch (error) {
        console.error('❌ 초기화 오류:', error);
        hideLoadingScreen();
        alert('오류가 발생했습니다. 콘솔을 확인하세요.');
    }
});