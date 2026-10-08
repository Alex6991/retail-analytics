"""
FastAPI-приложение для Retail Analytics.
Отдаёт данные о продажах через REST API.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import sys
from pathlib import Path

# Добавляем путь к src, чтобы импортировать database
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from database import run_query

app = FastAPI(
    title="Retail Analytics API",
    description="API для аналитики продаж магазина",
    version="1.0.0"
)


# --- ЭНДПОИНТЫ ---

@app.get("/")
def root():
    """Приветствие."""
    return {
        "message": "Retail Analytics API",
        "docs": "/docs",
        "endpoints": [
            "/api/stats",
            "/api/sales-by-year",
            "/api/categories",
            "/api/targets"
        ]
    }


@app.get("/api/stats")
def get_stats():
    """Общая статистика: заказы, продажи, прибыль."""
    query = """
    SELECT 
        COUNT(*) as total_orders,
        ROUND(SUM(sales), 2) as total_sales,
        ROUND(SUM(profit), 2) as total_profit,
        ROUND(AVG(sales), 2) as avg_order
    FROM orders
    """
    df = run_query(query)
    return df.to_dict(orient="records")[0]


@app.get("/api/sales-by-year")
def get_sales_by_year():
    """Продажи и прибыль по годам."""
    query = """
    SELECT 
        year,
        ROUND(SUM(sales), 2) as sales,
        ROUND(SUM(profit), 2) as profit,
        COUNT(*) as orders_count
    FROM orders
    GROUP BY year
    ORDER BY year
    """
    df = run_query(query)
    return df.to_dict(orient="records")


@app.get("/api/categories")
def get_categories():
    """Продажи и прибыль по категориям."""
    query = """
    SELECT 
        category,
        ROUND(SUM(sales), 2) as sales,
        ROUND(SUM(profit), 2) as profit,
        COUNT(*) as orders_count
    FROM orders
    GROUP BY category
    ORDER BY sales DESC
    """
    df = run_query(query)
    return df.to_dict(orient="records")


@app.get("/api/targets")
def get_targets():
    """Выполнение целей по годам."""
    query = """
    SELECT 
        o.year,
        ROUND(SUM(o.sales), 2) as actual_sales,
        t.target_sales,
        ROUND(SUM(o.sales) - t.target_sales, 2) as difference,
        ROUND(SUM(o.sales) * 100.0 / t.target_sales, 2) as percent_of_target
    FROM orders o
    JOIN targets t ON o.year = t.year
    GROUP BY o.year, t.target_sales
    ORDER BY o.year
    """
    df = run_query(query)
    return df.to_dict(orient="records")
from fastapi.responses import HTMLResponse
from pathlib import Path

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    """HTML-дашборд с графиками."""
    html_path = Path(__file__).resolve().parent.parent / "templates" / "dashboard.html"
    return html_path.read_text(encoding="utf-8")


@app.get("/api/markets")
def get_markets():
    """Продажи по рынкам."""
    query = """
    SELECT 
        market,
        ROUND(SUM(sales), 2) as sales,
        ROUND(SUM(profit), 2) as profit,
        COUNT(*) as orders_count
    FROM orders
    GROUP BY market
    ORDER BY sales DESC
    """
    df = run_query(query)
    return df.to_dict(orient="records")