import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import json

# 페이지 설정
st.set_page_config(
    page_title="2,195일간의 여정, 코로나19 연대기",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 전체 CSS 스타일 (원본과 동일)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

    * {
        font-family: 'Noto Sans KR', sans-serif;
    }

    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }

    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 700 !important;
    }

    .hero-section {
        text-align: center;
        padding: 80px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 40px;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 20px;
    }

    .hero-subtitle {
        font-size: 1.5rem;
        color: rgba(255,255,255,0.9);
    }

    .section-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 50px 0 15px 0;
        color: #f1f5f9 !important;
    }

    .section-subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        margin-bottom: 30px;
    }

    iframe {
        border: none;
        border-radius: 15px;
    }

    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #60a5fa !important;
        font-weight: 700;
    }

    div[data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
        font-size: 1rem;
    }

    .footer {
        text-align: center;
        padding: 40px;
        background: #1e293b;
        border-radius: 15px
