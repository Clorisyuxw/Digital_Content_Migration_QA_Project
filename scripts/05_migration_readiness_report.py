from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

# Read migration dataset
migration_file = BASE_DIR / "data" / "bbc-news-migration.csv"

df = pd.read_csv(migration_file)

# Approved categories
valid_categories = [
    "business",
    "entertainment",
    "politics",
    "sport",
    "tech"
]

# Default status
df["Migration_Status"] = "Ready"

# Missing title
df.loc[df["title"].isnull(), "Migration_Status"] = "Review Required"

# Missing category
df.loc[df["category"].isnull(), "Migration_Status"] = "Review Required"

# Invalid category
df.loc[
    ~df["category"].isin(valid_categories)
    & df["category"].notnull(),
    "Migration_Status"
] = "Review Required"

# Truncated content
df.loc[
    df["content"] == "Content missing after migration",
    "Migration_Status"
] = "Review Required"

# Summary
summary = (
    df["Migration_Status"]
    .value_counts()
    .reset_index()
)

summary.columns = [
    "Migration_Status",
    "Record_Count"
]

# Save report
output_file = (
    BASE_DIR
    / "outputs"
    / "migration_readiness_report.csv"
)

summary.to_csv(output_file, index=False)

print("Migration Readiness Report Generated")
print()
print(summary)

print()
print("Output:")
print(output_file)