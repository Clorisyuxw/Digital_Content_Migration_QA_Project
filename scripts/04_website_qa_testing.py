from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "data" / "bbc-news-migration.csv"
df = pd.read_csv(file_path)

valid_categories = ["business", "entertainment", "politics", "sport", "tech"]

issues = []

# QA001 Missing Title
missing_title_rows = df[df["title"].isnull()]
for index, row in missing_title_rows.iterrows():
    issues.append({
        "Issue_ID": f"QA001-{index}",
        "Content_ID": row["filename"],
        "Issue_Type": "Missing Title",
        "Field": "title",
        "Issue_Description": "Page title is missing after migration.",
        "Severity": "High",
        "Status": "Open"
    })

# QA002 Missing Category / Metadata
missing_category_rows = df[df["category"].isnull()]
for index, row in missing_category_rows.iterrows():
    issues.append({
        "Issue_ID": f"QA002-{index}",
        "Content_ID": row["filename"],
        "Issue_Type": "Missing Metadata",
        "Field": "category",
        "Issue_Description": "Content category metadata is missing.",
        "Severity": "High",
        "Status": "Open"
    })

# QA003 Invalid Category Mapping
invalid_category_rows = df[
    df["category"].notnull() &
    (~df["category"].isin(valid_categories))
]
for index, row in invalid_category_rows.iterrows():
    issues.append({
        "Issue_ID": f"QA003-{index}",
        "Content_ID": row["filename"],
        "Issue_Type": "Invalid Category Mapping",
        "Field": "category",
        "Issue_Description": f"Category value '{row['category']}' does not match approved metadata values.",
        "Severity": "Medium",
        "Status": "Open"
    })

# QA004 Truncated Content
truncated_content_rows = df[df["content"] == "Content missing after migration"]
for index, row in truncated_content_rows.iterrows():
    issues.append({
        "Issue_ID": f"QA004-{index}",
        "Content_ID": row["filename"],
        "Issue_Type": "Truncated Content",
        "Field": "content",
        "Issue_Description": "Article body appears incomplete after migration.",
        "Severity": "High",
        "Status": "Open"
    })

# QA005 Potential Duplicate Title
duplicate_title_rows = df[df["title"].notnull() & df["title"].duplicated(keep=False)]
for index, row in duplicate_title_rows.iterrows():
    issues.append({
        "Issue_ID": f"QA005-{index}",
        "Content_ID": row["filename"],
        "Issue_Type": "Potential Duplicate Title",
        "Field": "title",
        "Issue_Description": "Title appears more than once and requires content review.",
        "Severity": "Low",
        "Status": "Review Required"
    })

issue_log = pd.DataFrame(issues)

output_path = BASE_DIR / "outputs" / "content_issue_log.csv"
issue_log.to_csv(output_path, index=False)

print("Website QA testing completed.")
print("Total issues identified:", len(issue_log))
print("\nIssue Summary:")
print(issue_log["Issue_Type"].value_counts())
print("\nOutput file:", output_path)