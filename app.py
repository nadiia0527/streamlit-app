import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Налаштування сторінки
st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")
st.title("📊 Аналітика YouTube-каналу")

# 2. Завантаження файлу
uploaded_file = st.file_uploader("Завантажте ваш CSV файл", type=['csv'])

if uploaded_file is not None:
    # Зчитуємо дані
    df = pd.read_csv(uploaded_file)
    
    # Перетворюємо стовпець з датою (припустимо, він називається 'date')
    df['date'] = pd.to_datetime(df['date'])
    
    # --- БІЧНА ПАНЕЛЬ (Фільтри) ---
    st.sidebar.header("Фільтрація")
    
    # Фільтр за датами
    start_date = st.sidebar.date_input("Початок періоду", df['date'].min())
    end_date = st.sidebar.date_input("Кінець періоду", df['date'].max())
    
    # Фільтр за типом контенту (якщо є стовпець 'type')
    types = df['type'].unique() if 'type' in df.columns else ["Video"]
    selected_types = st.sidebar.multiselect("Тип контенту", types, default=types)

    # Застосовуємо фільтри до даних
    mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
    if 'type' in df.columns:
        mask &= df['type'].isin(selected_types)
    
    df_filtered = df.loc[mask].copy()

    # --- РОЗРАХУНКИ (Engagement Rate) ---
    # Формула: (Лайки + Коментарі) / Перегляди * 100
    df_filtered['ER'] = ((df_filtered['likes'] + df_filtered['comments']) / df_filtered['views']) * 100
    
    # Вивід основних метрик
    col1, col2, col3 = st.columns(3)
    col1.metric("Середній ER", f"{df_filtered['ER'].mean():.2f}%")
    col2.metric("Усього переглядів", f"{df_filtered['views'].sum():,}")
    col3.metric("Кількість відео", len(df_filtered))

    # --- ВІЗУАЛІЗАЦІЯ (Heatmap) ---
    st.subheader("🔥 Теплова карта активності (по годинах)")
    
    # Створюємо дані для карти
    df_filtered['hour'] = df_filtered['date'].dt.hour
    df_filtered['day'] = df_filtered['date'].dt.day_name()
    
    # Зведена таблиця
    pivot = df_filtered.pivot_table(index='day', columns='hour', values='views', aggfunc='sum').fillna(0)
    
    # Малюємо графік
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
    st.pyplot(fig)

    # Таблиця з результатами
    st.subheader("📋 Детальні дані")
    st.dataframe(df_filtered[['title', 'views', 'likes', 'comments', 'ER']])

else:
    st.info("Будь ласка, завантажте CSV файл, щоб почати аналіз.")