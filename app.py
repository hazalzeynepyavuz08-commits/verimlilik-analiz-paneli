import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Verimlilik Paneli",layout="wide")

st.title("Haftalık Çalışma ve Verimlilik Analiz Paneli")

df = pd.read_csv("veriler.csv")

st.sidebar.header("Filtreler")
secilen_dersler = st.sidebar.multiselect(
    "Görmek İstediğin Dersleri Seç:",
    options=df["Ders"].unique().tolist(),
    default=df["Ders"].unique().tolist()
)
filtrelenmis_df = df[df["Ders"].isin(secilen_dersler)]

col1, col2, col3 = st.columns(3)

col1.metric("Toplam Çalışma",f"{filtrelenmis_df['Calisma_Saati'].sum():.1f} saat")
col2.metric("Ortalama Odak",f"{filtrelenmis_df['Odak_Puani'].mean():.1f}/10")
col3.metric("Ortalama Uyku",f"{filtrelenmis_df['Uyku_Saati'].mean():.1f}saat")

st.divider()

grafik_col1, grafik_col2 = st.columns(2)

with grafik_col1:
    fig_cubuk = px.bar(
        x=filtrelenmis_df["Gun"].tolist(),
        y=filtrelenmis_df["Calisma_Saati"].tolist(),
        color=filtrelenmis_df["Ders"].tolist(),
        labels={"x": "Gün", "y": "Çalışma Saati", "color": "Ders"},
        title="Günlere Göre Çalışma Saatleri"
    )
    st.plotly_chart(fig_cubuk, use_container_width=True)

with grafik_col2:
    fig_cizgi = px.line(
        x=filtrelenmis_df["Gun"].tolist(),
        y=filtrelenmis_df["Odak_Puani"].tolist(),
        markers=True,
        labels={"x": "Gün", "y": "Odak Puanı"},
        title="Günlük Odak Puanı Değişimi"
    )
    st.plotly_chart(fig_cizgi, use_container_width=True)

st.subheader("📋 Detaylı Veri Tablosu")
st.markdown(filtrelenmis_df.to_html(index=False), unsafe_allow_html=True)

