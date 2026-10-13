import streamlit as st
import pandas as pd
import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

def calculate_data_quality(data):
    import pandas as pd

    df = data.copy()

    df["report_week"] = pd.to_datetime(
        df["report_week"], errors="coerce"
    )

    df["reported_cases"] = pd.to_numeric(
        df["reported_cases"], errors="coerce"
    )

    df["reporting_facilities"] = pd.to_numeric(
        df["reporting_facilities"], errors="coerce"
    )

    invalid_dates = int(df["report_week"].isna().sum())

    invalid_cases = int((
        df["reported_cases"].isna()
        | (df["reported_cases"] < 0)
        | (df["reported_cases"] % 1 != 0)
    ).sum())

    invalid_facilities = int((
        df["reporting_facilities"].isna()
        | (df["reporting_facilities"] < 0)
        | (df["reporting_facilities"] % 1 != 0)
    ).sum())

    duplicates = int(df.duplicated(
        subset=["report_week", "region", "disease"]
    ).sum())

    valid_dates = df["report_week"].dropna()

    if valid_dates.empty:
        expected_weeks = 0
        observed_weeks = 0
        missing_weeks = 0
    else:
        expected = pd.date_range(
            start=valid_dates.min(),
            end=valid_dates.max(),
            freq="7D"
        )

        observed = pd.DatetimeIndex(
            valid_dates.drop_duplicates()
        )

        expected_weeks = len(expected)
        observed_weeks = len(
            expected.intersection(observed)
        )
        missing_weeks = len(
            expected.difference(observed)
        )

    return {
        "expected_weeks": expected_weeks,
        "observed_weeks": observed_weeks,
        "missing_weeks": missing_weeks,
        "duplicates": duplicates,
        "invalid_dates": invalid_dates,
        "invalid_cases": invalid_cases,
        "invalid_facilities": invalid_facilities,
    }

st.set_page_config(
    page_title="AI Healthcare Dashboard",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Healthcare Disease Analytics Dashboard")
st.caption("Educational project using synthetic healthcare data")

# Database configuration: cloud or local
cloud_url = os.environ.get("DATABASE_URL")

if not cloud_url:
    try:
        cloud_url = st.secrets.get("DATABASE_URL")
    except FileNotFoundError:
        cloud_url = None

if cloud_url:
    # Neon cloud PostgreSQL
    if cloud_url.startswith("postgresql://"):
        cloud_url = cloud_url.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1
        )

    engine = create_engine(
        cloud_url,
        pool_pre_ping=True
    )

else:
    # Local PostgreSQL fallback
    password = os.environ.get("PG_PASSWORD")

    if not password:
        st.error(
            "Database configuration missing. "
            "Set DATABASE_URL or PG_PASSWORD."
        )
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

# ---------------------------------------
# DATA QUALITY MONITORING
# ---------------------------------------

st.subheader("🧪 Data Quality & Reporting Completeness")

quality = calculate_data_quality(selected)

q1, q2, q3, q4 = st.columns(4)

q1.metric("Observed weeks", quality["observed_weeks"])
q2.metric("Missing weeks", quality["missing_weeks"])
q3.metric("Duplicate records", quality["duplicates"])
q4.metric("Invalid case counts", quality["invalid_cases"])

with st.expander("Detailed data-quality checks"):
    st.write("Expected weeks:", quality["expected_weeks"])
    st.write("Invalid dates:", quality["invalid_dates"])
    st.write(
        "Invalid facility counts:",
        quality["invalid_facilities"]
    )

    st.caption(
        "Checks cover the selected region and disease. "
        "Facility-level reporting completeness is not measured."
    )

if any([
    quality["missing_weeks"],
    quality["duplicates"],
    quality["invalid_dates"],
    quality["invalid_cases"],
    quality["invalid_facilities"],
]):
    st.warning("Some data-quality checks require review.")
else:
    st.success("No issues detected by the implemented checks.")

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