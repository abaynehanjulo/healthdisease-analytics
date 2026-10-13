
import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

st.set_page_config(
    page_title="AI Healthcare Dashboard",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Healthcare Disease Analytics Dashboard")
st.caption("Educational project using synthetic healthcare data")

password = os.environ.get("PG_PASSWORD")

if not password:
    st.error("PostgreSQL password variable is missing.")
    st.stop()

url = URL.create(
    "postgresql+psycopg",
    username="postgres",
    password=password,
    host="127.0.0.1",
    port=5433,
    database="health_db"
)

engine = create_engine(url)

@st.cache_data(ttl=60)
def load_data():
    with engine.connect() as connection:
        return pd.read_sql(
            text("SELECT * FROM health_cases ORDER BY report_week"),
            connection
        )

try:
    df = load_data()
except Exception as e:
    st.error(f"Database error: {e}")
    st.stop()

if df.empty:
    st.warning("No healthcare records found.")
    st.stop()

df["report_week"] = pd.to_datetime(df["report_week"])

region = st.sidebar.selectbox(
    "Select region",
    sorted(df["region"].unique())
)

disease = st.sidebar.selectbox(
    "Select disease",
    sorted(df[df["region"] == region]["disease"].unique())
)

selected = df[
    (df["region"] == region) &
    (df["disease"] == disease)
].sort_values("report_week").copy()

# Dashboard summary
c1, c2, c3 = st.columns(3)

c1.metric("Total cases", int(selected["reported_cases"].sum()))
c2.metric("Latest weekly cases", int(selected["reported_cases"].iloc[-1]))
c3.metric("Reporting facilities", int(selected["reporting_facilities"].iloc[-1]))

# Historical trend
st.subheader("Weekly reported disease cases")
st.line_chart(
    selected.set_index("report_week")["reported_cases"]
)

# Basic forecast
st.subheader("Next-week forecast")

if len(selected) >= 4:
    forecast = selected["reported_cases"].tail(4).mean()
    last_date = selected["report_week"].iloc[-1]
    next_week = last_date + pd.DateOffset(days=7)

    st.metric("Predicted cases", f"{forecast:.1f}")
    st.write("Forecast week:", next_week.date())
    st.caption("Four-week moving-average forecast, not a trained AI model.")

# Large increases
st.subheader("Unusual increases for review")

selected["change_percent"] = (
    selected["reported_cases"].pct_change() * 100
)
selected["days_between"] = selected["report_week"].diff().dt.days

alerts = selected[
    (selected["change_percent"] > 30) &
    (selected["days_between"] == 7)
]

if alerts.empty:
    st.info("No large increases found.")
else:
    st.warning(f"{len(alerts)} increases above the example 30% threshold.")
    st.dataframe(
        alerts[["report_week", "reported_cases", "change_percent"]],
        hide_index=True
    )

st.caption("These flags are not confirmed disease outbreaks.")

# Data table
st.subheader("Healthcare data")
st.dataframe(selected, hide_index=True)
from pathlib import Path

st.divider()
st.header("🤖 AI Disease Forecasting")

results_path = Path("reports/ai_forecast_results.csv")

if results_path.exists():
    ai = pd.read_csv(results_path).iloc[0]

    st.caption(
        "Random Forest model trained on 104 weeks "
        "of separate synthetic Region A malaria data."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "AI predicted cases",
        f"{ai['predicted_cases']:.1f}"
    )

    col2.metric(
        "Random Forest MAE",
        f"{ai['random_forest_mae']:.2f}"
    )

    col3.metric(
        "Baseline MAE",
        f"{ai['baseline_mae']:.2f}"
    )

    st.write("Forecast week:", ai["forecast_week"])

    st.info(
        "The AI forecast uses a separate synthetic dataset "
        "and is not directly comparable to the "
        "eight-week dashboard forecast."
    )
else:
    st.warning(
        "AI results are missing. Run python train_model.py."
    )
