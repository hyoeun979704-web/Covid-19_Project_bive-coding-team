import pandas as pd
import plotly.graph_objects as go

# 데이터 로딩 (로컬 경로로 수정)
df = pd.read_csv("country_wise_latest.csv")

# 컬럼 표준화
df = df.rename(columns={
    "Country/Region": "country",
    "Confirmed": "cum_confirmed",
    "Deaths": "cum_deaths",
    "Recovered": "cum_recovered",
    "Active": "active",
    "New cases": "new_confirmed",
    "New deaths": "new_deaths",
    "New recovered": "new_recovered",
    "WHO Region": "who_region"
})

# 국가명 기준으로 정렬 (알파벳 순)
df = df.sort_values("country").reset_index(drop=True)

# Plotly 그래프 객체 생성
fig = go.Figure()

# Confirmed (파란색) 막대 추가
fig.add_trace(go.Bar(
    name='Confirmed',
    x=df['country'],
    y=df['cum_confirmed'],
    marker_color='#1f77b4',
    text=df['cum_confirmed'],
    textposition='auto',
))

# Deaths (빨간색) 막대 추가
fig.add_trace(go.Bar(
    name='Deaths',
    x=df['country'],
    y=df['cum_deaths'],
    marker_color='#ef553b',
    text=df['cum_deaths'],
    textposition='auto',
))

# Recovered (녹색) 막대 추가
fig.add_trace(go.Bar(
    name='Recovered',
    x=df['country'],
    y=df['cum_recovered'],
    marker_color='#00cc96',
    text=df['cum_recovered'],
    textposition='auto',
))

# 레이아웃 설정
fig.update_layout(
    title={
        'text': 'COVID-19 Global Statistics by Country<br><sub>Cumulative Confirmed, Deaths, and Recovered Cases</sub>',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Country',
    yaxis_title='Number of Cases',
    barmode='group',  # 막대를 그룹으로 나란히 배치
    height=600,
    width=1800,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    xaxis=dict(
        tickangle=-45,
        tickfont=dict(size=10)
    ),
    hovermode='x unified'
)

# 브라우저에서 그래프 표시
fig.show(renderer="browser")

# 추가: 상위 20개 국가만 보는 그래프
print("\n=== 상위 20개 국가 (확진자 수 기준) ===")
df_top20 = df.nlargest(20, 'cum_confirmed')

fig_top20 = go.Figure()

fig_top20.add_trace(go.Bar(
    name='Confirmed',
    x=df_top20['country'],
    y=df_top20['cum_confirmed'],
    marker_color='#1f77b4',
    text=df_top20['cum_confirmed'],
    textposition='auto',
))

fig_top20.add_trace(go.Bar(
    name='Deaths',
    x=df_top20['country'],
    y=df_top20['cum_deaths'],
    marker_color='#ef553b',
    text=df_top20['cum_deaths'],
    textposition='auto',
))

fig_top20.add_trace(go.Bar(
    name='Recovered',
    x=df_top20['country'],
    y=df_top20['cum_recovered'],
    marker_color='#00cc96',
    text=df_top20['cum_recovered'],
    textposition='auto',
))

fig_top20.update_layout(
    title={
        'text': 'COVID-19 Top 20 Countries by Confirmed Cases<br><sub>Cumulative Statistics</sub>',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Country',
    yaxis_title='Number of Cases',
    barmode='group',
    height=600,
    width=1400,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    xaxis=dict(
        tickangle=-45,
        tickfont=dict(size=11)
    ),
    hovermode='x unified'
)

fig_top20.show(renderer="browser")

print(f"\n총 {len(df)}개 국가의 데이터를 시각화했습니다.")
print(f"상위 20개 국가만 별도로 표시했습니다.")