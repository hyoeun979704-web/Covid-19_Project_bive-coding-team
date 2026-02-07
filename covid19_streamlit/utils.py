# utils.py 데이터 로딩 및 공통 함수

# utils.py 데이터 로딩 및 공통 함수
import streamlit as st
import pandas as pd
import numpy as np
import requests

@st.cache_data
def load_data():
    """
    데이터 로딩 함수. 
    1. API/CSV 로드 시도
    2. 실패 시 시뮬레이션용 더미 데이터 생성
    """
    data = {}
    
    # 1. Timeline Data (API or Mock)
    try:
        # 실제 API 연결 시도 (타임아웃 설정)
        response = requests.get('https://disease.sh/v3/covid-19/historical/all?lastdays=30', timeout=2)
        if response.status_code == 200:
            json_data = response.json()
            cases = pd.DataFrame(list(json_data['cases'].items()), columns=['date', 'cases'])
            deaths = pd.DataFrame(list(json_data['deaths'].items()), columns=['date', 'deaths'])
            timeline = pd.merge(cases, deaths, on='date')
            timeline['date'] = pd.to_datetime(timeline['date']).dt.strftime('%Y-%m-%d')
            data['timeline'] = timeline
        else:
            raise Exception("API Error")
    except:
        # 실패 시 더미 데이터 생성
        dates = pd.date_range(start='2020-01-22', periods=100)
        data['timeline'] = pd.DataFrame({
            'date': dates.strftime('%Y-%m-%d'),
            'cases': np.linspace(0, 1000000, 100),
            'deaths': np.linspace(0, 50000, 100)
        })

    # 2. Symptoms Data (Mock)
    data['symptoms'] = pd.DataFrame({
        '증상': ['발열', '기침', '피로감', '후각상실', '인후통'],
        '델타_발현율(%)': [90, 80, 70, 60, 50],
        '오미크론_발현율(%)': [40, 50, 60, 10, 80]
    })

    # 3. Variants Data (Mock)
    data['variants'] = pd.DataFrame([
        {'variant': 'Original', 'start_date': '2019-12-01', 'end_date': '2020-09-01', 'color': '#E91E63'},
        {'variant': 'Delta', 'start_date': '2021-04-01', 'end_date': '2021-12-01', 'color': '#2196F3'},
        {'variant': 'Omicron', 'start_date': '2021-11-24', 'end_date': '2023-05-01', 'color': '#06B6D4'},
    ])
    
    return data

def get_cities():
    """3D 지구본에 표시할 주요 도시 좌표"""
    return [
        {"name": "Wuhan", "lat": 30.5928, "lng": 114.3055, "isOrigin": True},
        {"name": "Seoul", "lat": 37.5665, "lng": 126.9780},
        {"name": "New York", "lat": 40.7128, "lng": -74.0060, "hub": True},
        {"name": "London", "lat": 51.5074, "lng": -0.1278, "hub": True},
        {"name": "Paris", "lat": 48.8566, "lng": 2.3522},
        {"name": "Tokyo", "lat": 35.6762, "lng": 139.6503}
    ]
