from pathlib import Path
import pandas as pd

issues = [
    {
        "issue_id": "DQ-001",
        "region": "Region_A",
        "disease": "Malaria",
        "facility_id": "Facility_04",
        "issue_type": "Missing facility report",
        "assigned_team": "Healthcare Operations",
        "priority": "High",
        "status": "Open",
        "report_week": "2026-01-19",
        "resolution_notes": "",
    },
    {
        "issue_id": "DQ-002",
        "region": "Region_A",
        "disease": "Malaria",
        "facility_id": "Facility_08",
        "issue_type": "Missing facility report",
        "assigned_team": "Healthcare Operations",
        "priority": "Medium",
        "status": "Open",
        "report_week": "2026-01-19",
        "resolution_notes": "",
    },
    {
        "issue_id": "DQ-003",
        "region": "Region_A",
        "disease": "Malaria",
        "facility_id": "Facility_02",
        "issue_type": "Reporting pipeline issue",
        "assigned_team": "Data Engineering",
        "priority": "High",
        "status": "In Progress",
        "report_week": "2026-02-09",
        "resolution_notes": "Investigating missing source submission.",
    },
    {
        "issue_id": "DQ-004",
        "region": "Region_A",
        "disease": "Malaria",
        "facility_id": "Facility_05",
        "issue_type": "Reporting pipeline issue",
        "assigned_team": "Data Engineering",
        "priority": "Medium",
        "status": "In Progress",
        "report_week": "2026-02-09",
        "resolution_notes": "Checking ingestion logs.",
    },
    {
        "issue_id": "DQ-005",
        "region": "Region_A",
        "disease": "Malaria",
        "facility_id": "Facility_10",
        "issue_type": "Missing facility report",
        "assigned_team": "Healthcare Operations",
        "priority": "Low",
        "status": "Open",
        "report_week": "2026-02-09",
        "resolution_notes": "",
    },
    {
        "issue_id": "DQ-006",
        "region": "Region_A",
        "disease": "Malaria",
        "facility_id": "Facility_07",
        "issue_type": "Reporting date review",
        "assigned_team": "Development Team",
        "priority": "Low",
        "status": "Resolved",
        "report_week": "2026-02-23",
        "resolution_notes": "Synthetic date mapping issue reviewed.",
    },
]
# Add synthetic Region_B issues that match missing facility reports
region_b_issues = [
    {
        "issue_id": "DQ-007",
        "region": "Region_B",
        "disease": "Malaria",
        "facility_id": "Facility_03",
        "issue_type": "Missing facility report",
        "assigned_team": "Healthcare Operations",
        "priority": "High",
        "status": "Open",
        "report_week": "2026-01-12",
        "resolution_notes": "",
    },
    {
        "issue_id": "DQ-008",
        "region": "Region_B",
        "disease": "Malaria",
        "facility_id": "Facility_02",
        "issue_type": "Missing facility report",
        "assigned_team": "Healthcare Operations",
        "priority": "Medium",
        "status": "Open",
        "report_week": "2026-02-02",
        "resolution_notes": "",
    },
    {
        "issue_id": "DQ-009",
        "region": "Region_B",
        "disease": "Malaria",
        "facility_id": "Facility_06",
        "issue_type": "Missing facility report",
        "assigned_team": "Healthcare Operations",
        "priority": "Medium",
        "status": "In Progress",
        "report_week": "2026-02-02",
        "resolution_notes": "Following up on the missing submission.",
    },
]

issues.extend(region_b_issues)

df = pd.DataFrame(issues)

Path("data").mkdir(exist_ok=True)

df.to_csv("data/data_quality_issues.csv", index=False)

print("Issue tracker dataset created.")
print("Total issues:", len(df))
print("Open:", int((df["status"] == "Open").sum()))
print("In progress:", int((df["status"] == "In Progress").sum()))
print("Resolved:", int((df["status"] == "Resolved").sum()))