import streamlit as st
import streamlit.components.v1 as components
import os

# 1. 페이지 설정 (전체화면)
st.set_page_config(layout="wide", page_title="COVID-19 3D 연대기", page_icon="🦠")

# 2. Streamlit 기본 UI 제거 (완벽한 전체화면 구현)
st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        width: 100vw;
        height: 100vh;
        border: none;
        display: block;
    }
    .stApp {
        background-color: black;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# 3. 로컬 파일 읽기 함수
def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"/* {path} 파일을 찾을 수 없습니다. 경로를 확인해주세요. */"

# 4. JS 파일 통합 (모듈 의존성 해결을 위해 순서대로 로드 및 export 제거)
def load_js_bundle():
    # 로드할 파일 목록 (의존성 순서 중요: data -> 세부차트 -> 메인)
    files = [
        "js/data.js",
        "js/cfr-chart.js",
        "js/charts.js",
        "js/custom-chart.js",
        "js/globe.js",
        "js/indepth-chart.js",
        "js/variants-timeline.js",
        "js/virus.js",
        "js/main.js"
    ]
    
    js_bundle = ""
    for file_path in files:
        content = load_file(file_path)
        # 브라우저 호환성을 위해 import/export 키워드 제거 (간이 번들링)
        content = content.replace("export function", "function")
        content = content.replace("export const", "const")
        content = content.replace("export async function", "async function")
        # import 구문은 주석 처리
        lines = content.split('\n')
        cleaned_lines = [line for line in lines if not line.strip().startswith("import ")]
        js_bundle += f"\n// --- {file_path} ---\n" + "\n".join(cleaned_lines) + "\n"
        
    return js_bundle

# 5. HTML 조립
def get_full_html():
    # (1) HTML 뼈대 읽기
    html_content = load_file("index.html")
    
    # (2) CSS 주입
    css_content = load_file("css/style.css")
    # HTML 내의 css 링크 태그를 실제 코드로 교체
    html_content = html_content.replace(
        '<link rel="stylesheet" href="css/style.css">',
        f'<style>{css_content}</style>'
    )
    
    # (3) JS 주입
    js_content = load_js_bundle()
    # HTML 내의 main.js 스크립트 태그를 실제 코드로 교체
    # (type="module"을 제거하고 내용을 직접 삽입)
    html_content = html_content.replace(
        '<script type="module" src="js/main.js"></script>',
        f'<script>{js_content}</script>'
    )
    
    return html_content

# 6. 화면 출력
try:
    full_html = get_full_html()
    components.html(full_html, height=1000, scrolling=False)
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
    st.info("프로젝트 폴더 안에 index.html, css/style.css, js 폴더가 모두 있는지 확인해주세요.")
