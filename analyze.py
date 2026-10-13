import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Read sample data
df = pd.read_csv("data/health_cases.csv")

print("\n=== ORIGINAL DATA ===")
print(df.head())

# 2. Check data quality
print("\n=== MISSING VALUES ===")
print(df.isnull().sum())

print("\n=== DUPLICATE ROWS ===")
print(df.duplicated().sum())

# 3. Convert dates and validate case counts
df["report_week"] = pd.to_datetime(df["report_week"])
df["reported_cases"] = pd.to_numeric(
    df["reported_cases"], errors="coerce"
)

if df["reported_cases"].isna().any():
    raise ValueError("Some reported case values are invalid.")

if (df["reported_cases"] < 0).any():
    raise ValueError("Negative case counts found.")

# 4. Calculate total reported cases by region
print("\n=== TOTAL CASES BY REGION ===")
print(df.groupby("region")["reported_cases"].sum())

# 5. Select Region_A malaria data
region_a = df[
    (df["region"] == "Region_A") &
    (df["disease"] == "Malaria")
].copy()

region_a = region_a.sort_values("report_week")

# 6. Calculate week-to-week percentage changes
region_a["percentage_change"] = (
    region_a["reported_cases"].pct_change() * 100
)

print("\n=== REGION A WEEKLY ANALYSIS ===")
print(
    region_a[
        ["report_week", "reported_cases", "percentage_change"]
    ].to_string(index=False)
)

# 7. Flag increases greater than 30%
region_a["increase_flag"] = (
    region_a["percentage_change"] > 30
)

print("\n=== WEEKS WITH LARGE INCREASES ===")
print(
    region_a.loc[
        region_a["increase_flag"],
        ["report_week", "reported_cases", "percentage_change"]
    ].to_string(index=False)
)

# 8. Create a chart
plt.figure(figsize=(10, 5))

plt.plot(
    region_a["report_week"],
    region_a["reported_cases"],
    marker="o",
    label="Reported malaria cases"
)

plt.title("Weekly Malaria Reports - Region A (Synthetic Data)")
plt.xlabel("Reporting Week")
plt.ylabel("Reported Cases")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save chart in reports folder
Path("reports").mkdir(exist_ok=True)
plt.savefig("reports/malaria_trend.png")

plt.show()

print("\nChart saved to reports/malaria_trend.png")
print("Analysis completed successfully!")
# 9. Simple next-week forecast
last_four_weeks = region_a["reported_cases"].tail(4)

forecast = last_four_weeks.mean()

print("\n=== NEXT WEEK FORECAST ===")
print(f"Predicted cases: {forecast:.1f}")

next_week = (
    region_a["report_week"].max()
    + pd.Timedelta(days=7)
)

print(f"Forecast date: {next_week.date()}")