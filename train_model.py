import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

df = pd.read_csv(
    "data/health_cases_long.csv",
    parse_dates=["report_week"]
)

df = df[
    (df["region"] == "Region_A") &
    (df["disease"] == "Malaria")
].sort_values("report_week").copy()

# Create features from previous weeks
for lag in [1, 2, 3, 4]:
    df[f"lag_{lag}"] = df["reported_cases"].shift(lag)

# Seasonal features
week = df["report_week"].dt.isocalendar().week.astype(int)

df["week_sin"] = np.sin(2 * np.pi * week / 52)
df["week_cos"] = np.cos(2 * np.pi * week / 52)

df = df.dropna().copy()

features = [
    "lag_1", "lag_2", "lag_3", "lag_4",
    "week_sin", "week_cos"
]

# Keep final 16 weeks for testing
train = df.iloc[:-16]
test = df.iloc[-16:]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    min_samples_leaf=3
)

model.fit(train[features], train["reported_cases"])

predictions = model.predict(test[features])

mae = mean_absolute_error(
    test["reported_cases"], predictions
)

baseline_mae = mean_absolute_error(
    test["reported_cases"], test["lag_1"]
)

print("\n=== MODEL EVALUATION ===")
print(f"Random Forest MAE: {mae:.2f}")
print(f"Previous-week baseline MAE: {baseline_mae:.2f}")

# Train on all historical observations
model.fit(df[features], df["reported_cases"])

# Predict next week
last_date = df["report_week"].iloc[-1]
next_date = last_date + pd.DateOffset(weeks=1)

last = df.iloc[-1]
next_week = int(next_date.isocalendar().week)

next_features = pd.DataFrame([{
    "lag_1": last["reported_cases"],
    "lag_2": last["lag_1"],
    "lag_3": last["lag_2"],
    "lag_4": last["lag_3"],
    "week_sin": np.sin(2 * np.pi * next_week / 52),
    "week_cos": np.cos(2 * np.pi * next_week / 52)
}])

forecast = model.predict(next_features)[0]

print("\n=== NEXT-WEEK AI FORECAST ===")
print(f"Forecast week: {next_date.date()}")
print(f"Predicted cases: {forecast:.1f}")
from pathlib import Path

Path("reports").mkdir(exist_ok=True)

results = pd.DataFrame([{
    "forecast_week": next_date.date(),
    "predicted_cases": round(float(forecast), 1),
    "random_forest_mae": round(float(mae), 2),
    "baseline_mae": round(float(baseline_mae), 2)
}])

results.to_csv("reports/ai_forecast_results.csv", index=False)

print("AI results saved successfully!")