import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="YouTube Analytics", layout="wide")
st.title("📊 Автоматична аналітика YouTube")

# Ім'я файлу в репозиторії
FILE_NAME = 'data.csv'

# Перевірка наявності файлу
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    st.success("✅ Дані завантажено автоматично з GitHub")
else:
    st.warning(f"⚠️ Файл {FILE_NAME} не знайдено. Будь ласка, завантажте його вручну.")
    uploaded_file = st.file_uploader("Завантажити CSV", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.stop()

# --- ОБРОБКА ДАНИХ ---
df['date'] = pd.to_datetime(df['date'])
df['ER'] = ((df['likes'] + df['comments']) / df['views']) * 100

# Метрики
c1, c2, c3 = st.columns(3)
c1.metric("Середній ER", f"{df['ER'].mean():.2f}%")
c2.metric("Усього переглядів", f"{df['views'].sum():,}")
c3.metric("Кількість відео", len(df))

# Теплова карта
st.subheader("🔥 Теплова карта залучення")
df['hour'] = df['date'].dt.hour
df['day'] = df['date'].dt.day_name()
pivot = df.pivot_table(index='day', columns='hour', values='views', aggfunc='sum').fillna(0)

fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
st.pyplot(fig)

st.subheader("📋 Таблиця даних")
st.dataframe(df)