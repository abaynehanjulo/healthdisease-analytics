
import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# Connect to your PostgreSQL database
password = os.environ.get("PG_PASSWORD")

if not password:
    raise RuntimeError("PG_PASSWORD is not set.")

url = URL.create(
    "postgresql+psycopg",
    username="postgres",
    password=password,
    host="127.0.0.1",
    port=5433,
    database="health_db",
)

engine = create_engine(url)

# Read your existing sample CSV
df = pd.read_csv("data/health_cases.csv")

required = [
    "report_week",
    "region",
    "disease",
    "reported_cases",
    "reporting_facilities",
]

if not set(required).issubset(df.columns):
    raise ValueError("Required CSV columns are missing.")

if df[required].isna().any().any():
    raise ValueError("Missing values found.")

if df.duplicated(
    ["report_week", "region", "disease"]
).any():
    raise ValueError("Duplicate records found.")

df["report_week"] = pd.to_datetime(
    df["report_week"], errors="raise"
)

for col in ["reported_cases", "reporting_facilities"]:
    df[col] = pd.to_numeric(df[col], errors="raise")

    if (df[col] < 0).any():
        raise ValueError(f"Negative values in {col}")

# Replace only the contents of the sample table
with engine.begin() as connection:
    connection.execute(text("DELETE FROM health_cases"))

    for row in df.itertuples(index=False):
        connection.execute(
            text("""
                INSERT INTO health_cases (
                    report_week,
                    region,
                    disease,
                    reported_cases,
                    reporting_facilities
                )
                VALUES (
                    :report_week,
                    :region,
                    :disease,
                    :reported_cases,
                    :reporting_facilities
                )
            """),
            {
                "report_week": row.report_week.date(),
                "region": row.region,
                "disease": row.disease,
                "reported_cases": int(row.reported_cases),
                "reporting_facilities": int(
                    row.reporting_facilities
                ),
            },
        )

print(f"Successfully imported {len(df)} records.")
