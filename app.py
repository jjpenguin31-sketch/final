import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="항공기 비행 계산기", page_icon="✈️")

st.title("✈️ 항공기 비행 조건 계산기")
st.write("실제 공항 데이터를 활용한 비행 거리, 시간, 연료 계산 프로그램")

# CSV 데이터 불러오기
df = pd.read_csv("airports.csv", low_memory=False)

# 공항 데이터 정리
df = df[
    (df["type"].isin(["large_airport", "medium_airport", "small_airport"]))
    & df["iata_code"].notna()
    & df["latitude_deg"].notna()
    & df["longitude_deg"].notna()
].copy()

df = df.reset_index(drop=True)

df["label"] = (
    df["name"].astype(str)
    + " ("
    + df["iata_code"].astype(str)
    + ")"
)

airport_list = df["label"].tolist()

st.subheader("1. 공항 선택")

departure = st.selectbox("출발 공항", airport_list)
arrival = st.selectbox("도착 공항", airport_list, index=1)

st.subheader("2. 비행 조건 입력")

speed = st.number_input("비행 속도 (km/h)", 1, 1500, 800)
fuel = st.number_input("시간당 연료 소모량 (L/h)", 1, 10000, 2500)

# 두 공항 사이의 거리 계산
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371

    lat1, lon1, lat2, lon2 = map(
        math.radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    return 2 * R * math.asin(math.sqrt(a))


if st.button("비행 조건 계산하기"):

    if departure == arrival:
        st.error("출발 공항과 도착 공항을 다르게 선택하세요.")

    else:
        start = df[df["label"] == departure].iloc[0]
        end = df[df["label"] == arrival].iloc[0]

        distance = calculate_distance(
            start["latitude_deg"],
            start["longitude_deg"],
            end["latitude_deg"],
            end["longitude_deg"]
        )

        flight_time = distance / speed
        total_fuel = flight_time * fuel

        st.subheader("3. 계산 결과")

        st.metric("비행 거리", f"{distance:,.2f} km")
        st.metric(
            "예상 비행 시간",
            f"{int(flight_time)}시간 {int(flight_time % 1 * 60)}분"
        )
        st.metric("예상 연료 소모량", f"{total_fuel:,.2f} L")

        st.success("계산 완료!")

        st.caption(
            "※ 공항 간 직선거리 기준의 단순 계산이며 "
            "실제 항공 경로와 기상 조건은 반영하지 않습니다."
        )
