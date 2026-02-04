import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    "Confirmed last week": "confirmed_last_week",
    "1 week change": "week_change",
    "1 week % increase": "week_pct_increase",
    "WHO Region": "who_region"
})

# 국가명 기준으로 정렬 (알파벳 순)
df = df.sort_values("country").reset_index(drop=True)

# ==================== 그래프 1: 겹친 막대 그래프 ====================
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

# ==================== 그래프 2: 상위 20개 국가 ====================
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
        'text': 'COVID-19 Top 20 Countries by Confirmed Cases<br><sub>Cumulative Statistics (Stacked View)</sub>',
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

# ==================== 그래프 3: 시계열 시뮬레이션 (증가율 기준 상위 15개) ====================
print("\n=== 주간 증가율 상위 15개 국가의 확진자 증가 추이 ===")

# 주간 증가율 기준 상위 15개 국가 선택
df_top15_pct = df.nlargest(15, 'week_pct_increase').copy()

# 각 국가별로 1주일 전과 현재 데이터 준비
timeline_data = []
for _, row in df_top15_pct.iterrows():
    # 1주일 전 데이터
    timeline_data.append({
        'country': row['country'],
        'time_point': 'Last Week',
        'confirmed': row['confirmed_last_week'],
        'percentage': row['week_pct_increase']
    })
    # 현재 데이터
    timeline_data.append({
        'country': row['country'],
        'time_point': 'Current',
        'confirmed': row['cum_confirmed'],
        'percentage': row['week_pct_increase']
    })

timeline_df = pd.DataFrame(timeline_data)

# 증가율 기준으로 정렬 (내림차순)
country_order = df_top15_pct.sort_values('week_pct_increase', ascending=False)['country'].tolist()

# 시계열 라인 차트 생성
fig_timeline = go.Figure()

# 각 국가별로 라인 추가 (증가율 높은 순서대로)
for idx, country in enumerate(country_order):
    country_data = timeline_df[timeline_df['country'] == country]
    pct = country_data['percentage'].iloc[0]
    
    fig_timeline.add_trace(go.Scatter(
        x=country_data['time_point'],
        y=country_data['confirmed'],
        mode='lines+markers',
        name=f'{country} ({pct:.1f}%)',
        line=dict(width=2),
        marker=dict(size=6),
        hovertemplate='<b>%{fullData.name}</b><br>Cases: %{y:,}<extra></extra>'
    ))

fig_timeline.update_layout(
    title={
        'text': 'COVID-19 Weekly Progression - Top 15 Countries by Growth Rate<br><sub>Last Week vs Current Confirmed Cases (Sorted by Percentage Increase)</sub>',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Time Period',
    yaxis_title='Confirmed Cases',
    height=700,
    width=1400,
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02
    ),
    hovermode='x unified',
    xaxis=dict(
        categoryorder='array',
        categoryarray=['Last Week', 'Current']
    )
)

fig_timeline.show(renderer="browser")

# ==================== 그래프 4: 주간 증가율 막대 그래프 (Percentage 기준 정렬) ====================
print("\n=== 상위 20개 국가의 주간 증가율 ===")

# 주간 증가율 기준으로 상위 20개 국가 선택
df_top20_pct = df.nlargest(20, 'week_pct_increase').copy()

# 증가율 기준으로 정렬 (내림차순)
df_top20_pct = df_top20_pct.sort_values('week_pct_increase', ascending=True)  # 막대 그래프는 아래에서 위로

fig_increase = go.Figure()

fig_increase.add_trace(go.Bar(
    x=df_top20_pct['week_pct_increase'],
    y=df_top20_pct['country'],
    orientation='h',  # 수평 막대 그래프
    marker_color='#ff7f0e',
    text=[f'{pct:.1f}%' for pct in df_top20_pct['week_pct_increase']],
    textposition='auto',
    hovertemplate='<b>%{y}</b><br>Weekly Increase: %{customdata:,} cases<br>Growth Rate: %{x:.2f}%<extra></extra>',
    customdata=df_top20_pct['week_change']
))

fig_increase.update_layout(
    title={
        'text': 'COVID-19 Weekly Growth Rate - Top 20 Countries<br><sub>Percentage Increase in Cases (Last Week)</sub>',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Weekly Growth Rate (%)',
    yaxis_title='Country',
    height=700,
    width=1200,
    showlegend=False
)

fig_increase.show(renderer="browser")

# ==================== 그래프 5: 증가량과 증가율 복합 차트 ====================
print("\n=== 주간 증가량 vs 증가율 비교 (상위 20개) ===")

# 증가율 기준 상위 20개
df_top20_combined = df.nlargest(20, 'week_pct_increase').copy()
df_top20_combined = df_top20_combined.sort_values('week_pct_increase', ascending=False)

# 서브플롯 생성 (2개의 y축)
fig_combined = make_subplots(specs=[[{"secondary_y": True}]])

# 증가량 막대 그래프 (첫 번째 y축)
fig_combined.add_trace(
    go.Bar(
        x=df_top20_combined['country'],
        y=df_top20_combined['week_change'],
        name='Weekly Increase (Cases)',
        marker_color='#1f77b4',
        opacity=0.7
    ),
    secondary_y=False
)

# 증가율 라인 그래프 (두 번째 y축)
fig_combined.add_trace(
    go.Scatter(
        x=df_top20_combined['country'],
        y=df_top20_combined['week_pct_increase'],
        name='Growth Rate (%)',
        mode='lines+markers',
        marker_color='#ef553b',
        line=dict(width=3),
        marker=dict(size=8)
    ),
    secondary_y=True
)

fig_combined.update_layout(
    title={
        'text': 'COVID-19 Weekly Increase vs Growth Rate - Top 20 Countries<br><sub>Sorted by Percentage Increase</sub>',
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title='Country',
    height=700,
    width=1600,
    hovermode='x unified',
    xaxis=dict(
        tickangle=-45,
        tickfont=dict(size=10)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

# y축 제목 설정
fig_combined.update_yaxes(title_text="Number of Cases", secondary_y=False)
fig_combined.update_yaxes(title_text="Growth Rate (%)", secondary_y=True)

fig_combined.show(renderer="browser")

print(f"\n총 {len(df)}개 국가의 데이터를 시각화했습니다.")
print("5개의 그래프가 생성되었습니다:")
print("1. 전체 국가 누적 통계 (겹친 막대)")
print("2. 상위 20개 국가 누적 통계 (겹친 막대)")
print("3. 주간 증가율 상위 15개 국가의 증가 추이 (라인 차트)")
print("4. 주간 증가율 상위 20개 국가 (수평 막대 그래프, Percentage 정렬)")
print("5. 증가량 vs 증가율 복합 차트 (막대+라인)")