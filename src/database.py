"""
Модуль для работы с базой данных SQLite.
Загружает данные из CSV и предоставляет функции для запросов.
"""

import sqlite3
import pandas as pd
from pathlib import Path

# Пути
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "SuperStoreOrders.csv"
DB_PATH = BASE_DIR / "data" / "retail.db"


def create_database():
    """Создаёт БД SQLite и загружает данные из CSV."""
    
    # Читаем CSV
    df = pd.read_csv(CSV_PATH, encoding="latin-1")
    
    # Чистим колонки
    df = df.rename(columns={df.columns[0]: 'order_id'})
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Преобразуем числовые колонки
    numeric_cols = ['sales', 'quantity', 'discount', 'profit', 'shipping_cost']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Убираем битые строки
    df = df.dropna(subset=['sales'])
    
    # Подключаемся к БД (создастся, если нет)
    conn = sqlite3.connect(DB_PATH)
    
    # Записываем данные в таблицу
    df.to_sql('orders', conn, if_exists='replace', index=False)
    
    # Проверяем
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM orders")
    count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"✅ База данных создана: {DB_PATH}")
    print(f"✅ Загружено строк: {count}")
    print(f"✅ Колонок: {len(df.columns)}")


def get_connection():
    """Возвращает соединение с БД."""
    return sqlite3.connect(DB_PATH)


def run_query(query, params=None):
    """Выполняет SQL-запрос и возвращает DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


if __name__ == "__main__":
    create_database()