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

# Confirmed (파란색) 막대 추가 - 가장 먼저 (뒤에)
fig.add_trace(go.Bar(
    name='Confirmed',
    x=df['country'],
    y=df['cum_confirmed'],
    marker_color='#1f77b4',
    opacity=0.8,
))

# Recovered (녹색) 막대 추가 - 두 번째 (중간)
fig.add_trace(go.Bar(
    name='Recovered',
    x=df['country'],
    y=df['cum_recovered'],
    marker_color='#00cc96',
    opacity=0.8,
))

# Deaths (빨간색) 막대 추가 - 마지막 (앞에)
fig.add_trace(go.Bar(
    name='Deaths',
    x=df['country'],
    y=df['cum_deaths'],
    marker_color='#ef553b',
    opacity=0.8,
))

# 레이아웃 설정
fig.update_layout(
    title={
        'text': 'COVID-19 Global Statistics by Country<br><sub>Cumulative Confirmed, Recovered, and Deaths (Stacked View)</sub>',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Country',
    yaxis_title='Number of Cases',
    barmode='overlay',  # 막대를 겹쳐서 표시
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

# Confirmed (파란색) 막대 추가 - 가장 먼저 (뒤에)
fig_top20.add_trace(go.Bar(
    name='Confirmed',
    x=df_top20['country'],
    y=df_top20['cum_confirmed'],
    marker_color='#1f77b4',
    opacity=0.8,
))

# Recovered (녹색) 막대 추가 - 두 번째 (중간)
fig_top20.add_trace(go.Bar(
    name='Recovered',
    x=df_top20['country'],
    y=df_top20['cum_recovered'],
    marker_color='#00cc96',
    opacity=0.8,
))

# Deaths (빨간색) 막대 추가 - 마지막 (앞에)
fig_top20.add_trace(go.Bar(
    name='Deaths',
    x=df_top20['country'],
    y=df_top20['cum_deaths'],
    marker_color='#ef553b',
    opacity=0.8,
))

fig_top20.update_layout(
    title={
        'text': 'COVID-19 Top 20 Countries by Confirmed Cases<br><sub>Cumulative Statistics ( 2020-8-18 Stacked View)</sub>',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Country',
    yaxis_title='Number of Cases',
    barmode='overlay',  # 막대를 겹쳐서 표시
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
print("\n※ 막대 그래프가 겹쳐져 있어 Confirmed(파란색) 위에 Recovered(녹색), 그 위에 Deaths(빨간색)가 표시됩니다.")