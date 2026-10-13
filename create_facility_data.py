from pathlib import Path
import pandas as pd

weeks = pd.date_range(
    start="2026-01-05",
    periods=8,
    freq="7D"
)

regions = {
    "Region_A": 12,
    "Region_B": 8,
}

records = []

for region, facility_count in regions.items():
    for week_index, week in enumerate(weeks):
        for facility_index in range(facility_count):

            facility = f"Facility_{facility_index + 1:02d}"

            if region == "Region_A":
                missing = (
                    (week_index == 2 and facility_index in [3, 7])
                    or (week_index == 5 and facility_index in [1, 4, 9])
                    or (week_index == 7 and facility_index == 6)
                )
            else:
                missing = (
                    (week_index == 1 and facility_index == 2)
                    or (week_index == 4 and facility_index in [1, 5])
                )

            records.append({
                "report_week": week.date(),
                "region": region,
                "disease": "Malaria",
                "facility_id": facility,
                "submitted": not missing
            })

df = pd.DataFrame(records)

Path("data").mkdir(exist_ok=True)

df.to_csv(
    "data/facility_reporting.csv",
    index=False
)

print("Facility reporting dataset created.")

for region in regions:
    subset = df[df["region"] == region]

    print(f"\n{region}")
    print("Expected:", len(subset))
    print("Received:", int(subset["submitted"].sum()))
    print("Missing:", int((~subset["submitted"]).sum()))