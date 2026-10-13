from pathlib import Path
import pandas as pd

weeks = pd.date_range(
    start="2026-01-05",
    periods=8,
    freq="7D"
)

facilities = [
    f"Facility_{i:02d}"
    for i in range(1, 13)
]

records = []

for week_index, week in enumerate(weeks):
    for facility_index, facility in enumerate(facilities):
        # Illustrative missing submissions
        missing = (
            (week_index == 2 and facility_index in [3, 7])
            or (week_index == 5 and facility_index in [1, 4, 9])
            or (week_index == 7 and facility_index == 6)
        )

        records.append({
            "report_week": week.date(),
            "region": "Region_A",
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
print("Expected submissions:", len(df))
print("Received submissions:", int(df["submitted"].sum()))
print("Missing submissions:", int((~df["submitted"]).sum()))