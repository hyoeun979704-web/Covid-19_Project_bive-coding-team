import pandas as pd
import plotly.express as px

# 0) 데이터 로딩
df = pd.read_csv("country_wise_latest.csv")

# 1) 컬럼 표준화
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

# 데이터 확인 (디버깅용)
print("데이터셋의 국가명 샘플:")
print(df["country"].head(20))
print(f"\n'Korea, South' 존재 여부: {'Korea, South' in df['country'].values}")

# 2) 국가 필터링
country_name = "Korea, South"
country_data = df[df["country"] == country_name]

# 국가 데이터가 없으면 가능한 한국 관련 국가명 찾기
if country_data.empty:
    korea_matches = df[df["country"].str.contains("Korea", case=False, na=False)]
    print("\n한국 관련 국가명:")
    print(korea_matches["country"].values)
    if not korea_matches.empty:
        country_name = korea_matches.iloc[0]["country"]
        country_data = korea_matches.iloc[0:1]
        print(f"\n'{country_name}' 사용")

# 3) 데이터 가공
if not country_data.empty:
    # 딕셔너리 형태로 데이터 재구성
    plot_data = pd.DataFrame({
        "metric_label": ["Confirmed", "Deaths", "Recovered"],
        "value": [
            country_data["cum_confirmed"].values[0],
            country_data["cum_deaths"].values[0],
            country_data["cum_recovered"].values[0]
        ]
    })
    
    print(f"\n{country_name} 데이터:")
    print(plot_data)
    
    # 4) 시각화
    color_map = {
        "Confirmed": "#1f77b4", 
        "Deaths": "#ef553b",    
        "Recovered": "#00cc96"  
    }
    
    fig_country_bar = px.bar(
        plot_data,
        x="metric_label",
        y="value",
        color="metric_label",
        color_discrete_map=color_map,
        title=f"{country_name} - Cumulative COVID-19 Statistics",
        labels={"metric_label": "Metric", "value": "Count"},
        text_auto=True
    )
    
    # 레이아웃 개선
    fig_country_bar.update_layout(
        showlegend=False,
        xaxis_title="",
        yaxis_title="Number of Cases",
        height=500
    )
    
    fig_country_bar.show(renderer="browser")
else:
    print(f"\n오류: '{country_name}' 데이터를 찾을 수 없습니다.")
    print("사용 가능한 국가 목록:")
    print(df["country"].sort_values().unique())