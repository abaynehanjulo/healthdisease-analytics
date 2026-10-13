import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load sample data
df = pd.read_csv("data/health_cases.csv")
df["report_week"] = pd.to_datetime(df["report_week"])

# Select Region A malaria reports
df = df[
    (df["region"] == "Region_A")
    & (df["disease"] == "Malaria")
].sort_values("report_week")

# Use the last four reported weeks
last_four = df["reported_cases"].tail(4)
forecast_value = last_four.mean()

# Forecast the next week
last_date = df["report_week"].max()
next_date = last_date + pd.Timedelta(days=7)

print("=== BASIC FORECAST ===")
print(f"Next reporting week: {next_date.date()}")
print(f"Predicted cases: {forecast_value:.2f}")

# Visualize historical reports and forecast
plt.figure(figsize=(10, 5))

plt.plot(
    df["report_week"],
    df["reported_cases"],
    marker="o",
    label="Historical reports"
)

plt.scatter(
    [next_date],
    [forecast_value],
    color="red",
    s=100,
    label="Next-week forecast"
)

plt.title("Malaria Reports: Historical Data and Forecast")
plt.xlabel("Reporting Week")
plt.ylabel("Reported Cases")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

Path("reports").mkdir(exist_ok=True)
plt.savefig("reports/basic_forecast.png")
plt.show()