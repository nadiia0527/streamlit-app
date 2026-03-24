import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="YouTube Analytics Pro", layout="wide")
st.title("📊 Автоматична аналітика YouTube-каналу")

# Шлях до файлу в репозиторії
DEFAULT_FILE = 'data.csv'

# Перевіряємо, чи є файл у папці
if os.path.exists(DEFAULT_FILE):
    df_raw = pd.read_csv(DEFAULT_FILE)
    st.success(f"✅ Дані успішно завантажені з репозиторію ({DEFAULT_FILE})")
else:
    uploaded_file = st.file_uploader("Або завантажте власний CSV файл", type=['csv'])
    if uploaded_file:
        df_raw = pd.read_csv(uploaded_file)
    else:
        st.info("Очікування даних...")
        st.stop()

# --- ОБРОБКА ДАНИХ ---
df = df_raw.copy()
df['date'] = pd.to_datetime(df['date'])

# --- БІЧНА ПАНЕЛЬ ---
st.sidebar.header("Налаштування перегляду")
content_types = df['type'].unique()
selected_types = st.sidebar.multiselect("Тип контенту", content_types, default=content_types)

# Фільтрація
df_filtered = df[df['type'].isin(selected_types)]
df_filtered['ER'] = ((df_filtered['likes'] + df_filtered['comments']) / df_filtered['views']) * 100

# --- ВІЗУАЛІЗАЦІЯ ---
col1, col2, col3 = st.columns(3)
col1.metric("Середній ER", f"{df_filtered['ER'].mean():.2f}%")
col2.metric("Усього переглядів", f"{df_filtered['views'].sum():,}")
col3.metric("Кількість відео", len(df_filtered))

st.subheader("🔥 Теплова карта залучення (за замовчуванням)")
df_filtered['hour'] = df_filtered['date'].dt.hour
df_filtered['day'] = df_filtered['date'].dt.day_name()
pivot = df_filtered.pivot_table(index='day', columns='hour', values='views', aggfunc='sum').fillna(0)

fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
st.pyplot(fig)

st.subheader("📋 Повна таблиця результатів")
st.dataframe(df_filtered)
else:
    st.info("Будь ласка, завантажте CSV файл, щоб почати аналіз.")
