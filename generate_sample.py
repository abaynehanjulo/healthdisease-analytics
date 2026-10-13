import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

dates = pd.date_range(
    start="2024-01-01",
    periods=104,
    freq="W-MON"
)

records = []

for region, base in [("Region_A", 110), ("Region_B", 55)]:
    for i, date in enumerate(dates):
        seasonal = 30 * np.sin(2 * np.pi * i / 52)
        trend = 0.25 * i
        noise = rng.normal(0, 10)

        cases = max(
            0,
            round(base + seasonal + trend + noise)
        )

        records.append({
            "report_week": date,
            "region": region,
            "disease": "Malaria",
            "reported_cases": cases,
            "reporting_facilities": 12 if region == "Region_A" else 8
        })

df = pd.DataFrame(records)

df.to_csv("data/health_cases_long.csv", index=False)

print("Created 104 weeks of synthetic data per region.")