"""Utility functions for the dashboard chatbot.

The chatbot uses an LLM only to classify intent. All business answers come from
existing project outputs so responses stay stable and traceable.
"""

from functools import lru_cache
import os
import re
from pathlib import Path

import pandas as pd

from .config import DATA_OUTPUTS, DATA_PROCESSED, REPORTS_CHARTS


INTENTS = {"top_products", "category_sales", "forecast_product", "show_chart", "unknown"}


@lru_cache(maxsize=1)
def load_data():
    """Load existing project outputs used by the chatbot."""
    merged_df = pd.read_csv(DATA_PROCESSED / "merged_dataset.csv")
    forecast_weekly = pd.read_csv(DATA_OUTPUTS / "forecast_weekly.csv")

    if "Week_End_Date" in merged_df.columns:
        merged_df["Week_End_Date"] = pd.to_datetime(merged_df["Week_End_Date"])
    if "Week_End_Date" in forecast_weekly.columns:
        forecast_weekly["Week_End_Date"] = pd.to_datetime(forecast_weekly["Week_End_Date"])

    return {
        "merged": merged_df,
        "forecast_weekly": forecast_weekly,
        "charts_dir": REPORTS_CHARTS,
    }


def _table_response(df: pd.DataFrame, message: str):
    return {
        "type": "table",
        "data": df.to_dict(orient="records"),
        "columns": df.columns.tolist(),
        "message": message,
    }


def top_products(limit: int = 10) -> pd.DataFrame:
    """Return top products by historical quantity sold."""
    merged_df = load_data()["merged"]
    return (
        merged_df.groupby(["Product_ID", "Product_Name", "Category"], as_index=False)
        .agg(
            Total_Qty_Sold=("Qty_Sold", "sum"),
            Avg_Weekly_Qty=("Qty_Sold", "mean"),
            Avg_Inventory=("Inventory", "mean"),
        )
        .sort_values("Total_Qty_Sold", ascending=False)
        .head(limit)
        .round(2)
    )


def category_sales() -> pd.DataFrame:
    """Return sales summary by product category."""
    merged_df = load_data()["merged"]
    return (
        merged_df.groupby("Category", as_index=False)
        .agg(
            Total_Qty_Sold=("Qty_Sold", "sum"),
            Avg_Weekly_Qty=("Qty_Sold", "mean"),
            Product_Count=("Product_ID", "nunique"),
            Avg_Discount=("Discount", "mean"),
        )
        .sort_values("Total_Qty_Sold", ascending=False)
        .round(2)
    )


def forecast_product(product_id: str) -> pd.DataFrame:
    """Return 12-week forecast for a product."""
    forecast_weekly = load_data()["forecast_weekly"]
    product_id = product_id.upper().strip()
    result = forecast_weekly[forecast_weekly["Product_ID"].str.upper() == product_id].copy()

    if not result.empty:
        result["Week_End_Date"] = result["Week_End_Date"].dt.strftime("%Y-%m-%d")
        result["Forecast_Qty_Sold"] = result["Forecast_Qty_Sold"].round(2)

    return result


def _fallback_classify(query: str) -> str:
    query_lower = query.lower()

    if any(word in query_lower for word in ["chart", "plot", "graph", "visual"]):
        return "show_chart"
    if any(word in query_lower for word in ["forecast", "predict", "next 12", "future"]):
        return "forecast_product"
    if any(word in query_lower for word in ["category", "categories"]):
        return "category_sales"
    if any(word in query_lower for word in ["top", "best", "highest", "product", "products"]):
        return "top_products"

    return "unknown"


def classify_query_llm(query: str) -> str:
    """Classify a user query into one supported intent label."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _fallback_classify(query)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a query classifier. Classify user query into: "
                        "top_products, category_sales, forecast_product, show_chart, unknown. "
                        "Return only label."
                    ),
                },
                {"role": "user", "content": query},
            ],
            temperature=0,
            max_tokens=10,
        )
        intent = response.choices[0].message.content.strip().lower()
        return intent if intent in INTENTS else _fallback_classify(query)
    except Exception:
        return _fallback_classify(query)


def _extract_product_id(query: str) -> str | None:
    match = re.search(r"\b[A-Za-z]{2}\d{3}\b", query)
    return match.group(0).upper() if match else None


def _find_chart(query: str) -> Path | None:
    charts_dir = load_data()["charts_dir"]
    query_lower = query.lower()

    chart_map = [
        (["forecast", "actual"], "forecast_vs_actual.png"),
        (["top", "product"], "top_product_forecast.png"),
        (["category"], "sales_by_category.png"),
        (["demand"], "demand_class_bar.png"),
        (["feature", "importance"], "feature_importance.png"),
        (["model"], "model_comparison.png"),
    ]

    for keywords, filename in chart_map:
        if all(keyword in query_lower for keyword in keywords):
            path = charts_dir / filename
            if path.exists():
                return path

    default_path = charts_dir / "forecast_vs_actual.png"
    return default_path if default_path.exists() else None


def handle_query(query: str):
    """Classify and answer a user query with a structured response."""
    query = query.strip()
    if not query:
        return {"type": "text", "data": None, "message": "Please enter a question."}

    intent = classify_query_llm(query)

    if intent == "top_products":
        df = top_products()
        return _table_response(df, "Top products by historical quantity sold.")

    if intent == "category_sales":
        df = category_sales()
        return _table_response(df, "Category sales summary.")

    if intent == "forecast_product":
        product_id = _extract_product_id(query)
        if not product_id:
            return {
                "type": "text",
                "data": None,
                "message": "Please include a Product_ID, for example TE001.",
            }

        df = forecast_product(product_id)
        if df.empty:
            return {
                "type": "text",
                "data": None,
                "message": f"No forecast found for {product_id}.",
            }
        return _table_response(df, f"12-week forecast for {product_id}.")

    if intent == "show_chart":
        chart_path = _find_chart(query)
        if chart_path is None:
            return {"type": "text", "data": None, "message": "No chart file found."}
        return {
            "type": "image",
            "data": str(chart_path),
            "message": f"Showing chart: {chart_path.name}",
        }

    return {
        "type": "text",
        "data": None,
        "message": (
            "I can help with top products, category sales, product forecasts, "
            "and existing report charts."
        ),
    }
