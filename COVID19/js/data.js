// js/data.js

export const cities = [
    { name: "Wuhan", country: "China", lat: 30.5928, lng: 114.3055, hub: true, isOrigin: true },
    { name: "Seoul", country: "South Korea", lat: 37.5665, lng: 126.9780 },
    { name: "New York", country: "United States", lat: 40.7128, lng: -74.0060, hub: true },
    { name: "London", country: "United Kingdom", lat: 51.5074, lng: -0.1278, hub: true },
    { name: "Paris", country: "France", lat: 48.8566, lng: 2.3522 },
    { name: "Tokyo", country: "Japan", lat: 35.6762, lng: 139.6503 }
];

const FILES = {
    symptoms: "data/symptoms.csv",
    vaccine: "data/vaccine.csv",
    diagnosis: "data/diagnosis.csv",
    // [추가] 5번째 파일 경로
    variants: "data/covid_variants_timeline.csv"
};

function loadCsv(path) {
    return new Promise((resolve) => {
        if (typeof Papa === 'undefined') {
            console.error('Papa Parse not loaded');
            resolve([]);
            return;
        }
        Papa.parse(path, {
            download: true,
            header: true,
            dynamicTyping: true,
            skipEmptyLines: true,
            complete: (res) => resolve(res.data),
            error: (err) => {
                console.error(`CSV Load Failed: ${path}`, err);
                resolve([]);
            }
        });
    });
}

// [추가] disease.sh API에서 데이터 로드
async function loadCompactFromAPI() {
    try {
        console.log("Loading timeline from disease.sh API...");
        const response = await fetch('https://disease.sh/v3/covid-19/historical/all?lastdays=all');

        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        const data = await response.json();

        const timeline = [];
        const dates = Object.keys(data.cases);

        dates.forEach(date => {
            const [month, day, year] = date.split('/');
            const fullYear = year.length === 2 ? `20${year}` : year;
            const formattedDate = `${fullYear}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;

            timeline.push({
                date: formattedDate,
                cases: data.cases[date] || 0,
                deaths: data.deaths[date] || 0,
                new_cases: data.cases[date] || 0,
                new_deaths: data.deaths[date] || 0
            });
        });

        console.log(`✓ API 데이터 로드 완료: ${timeline.length}개 날짜`);
        return timeline;

    } catch (error) {
        console.error('API 로드 실패:', error);
        return [];
    }
}

export async function loadData() {
    console.log("Loading Data...");

    // [수정] API + CSV 동시 로드
    const [rawCompact, rawSymptoms, rawVaccine, rawDiagnosis, rawVariants] = await Promise.all([
        loadCompactFromAPI(),  // API로 변경
        loadCsv(FILES.symptoms),
        loadCsv(FILES.vaccine),
        loadCsv(FILES.diagnosis),
        loadCsv(FILES.variants)
    ]);

    // 1. Timeline
    let timeline = [];
    if (rawCompact && rawCompact.length > 0) {
        const map = {};
        rawCompact.forEach(r => {
            if (!r.date) return;
            if (!map[r.date]) map[r.date] = { date: r.date, cases: 0, deaths: 0 };
            map[r.date].cases += (r.new_cases || 0);
            map[r.date].deaths += (r.new_deaths || 0);
        });
        timeline = Object.values(map).sort((a, b) => new Date(a.date) - new Date(b.date));
    }

    // 2. Symptoms
    let symData = { labels: [], delta: [], omicron: [] };
    if (rawSymptoms && rawSymptoms.length > 0) {
        // CSV 헤더명과 일치하는지 확인 (이전 대화 기준)
        symData.labels = rawSymptoms.map(d => d['증상'] || d.symptom);
        symData.delta = rawSymptoms.map(d => d['델타_발현율(%)'] || d.delta);
        symData.omicron = rawSymptoms.map(d => d['오미크론_발현율(%)'] || d.omicron);
    }

    // 3. Vaccine
    let vacData = { labels: [], efficacy: [] };
    if (rawVaccine && rawVaccine.length > 0) {
        vacData.labels = rawVaccine.map(d => d['제조사'] || d.maker);
        vacData.efficacy = rawVaccine.map(d => d['전체_예방_효능(%)'] || d.efficacy);
    }

    // 4. Diagnosis
    let diagData = { labels: [], pcr: [], antigen: [] };
    if (rawDiagnosis && rawDiagnosis.length > 0) {
        diagData.labels = rawDiagnosis.map(d => d['Ct값_범위'] || d.ct_range);
        diagData.pcr = rawDiagnosis.map(d => d['RT-PCR_민감도(%)'] || d.pcr);
        diagData.antigen = rawDiagnosis.map(d => d['신속항원검사_민감도(%)'] || d.antigen);
    }

    // 5. [추가] Variants Timeline
    // CSV 그대로 반환하면 variants-timeline.js에서 계산함
    let variantsData = rawVariants || [];

    return {
        timeline,
        symptoms: symData,
        vaccine: vacData,
        diagnosis: diagData,
        variantsTimeline: variantsData, // 추가된 데이터
        compact: timeline
    };
}