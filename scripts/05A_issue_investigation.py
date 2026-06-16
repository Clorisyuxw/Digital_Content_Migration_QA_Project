from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "data" / "bbc-news-migration.csv"
df = pd.read_csv(file_path)

valid_categories = [
    "business",
    "entertainment",
    "politics",
    "sport",
    "tech"
]

# 1. Missing titles
missing_titles = df[df["title"].isnull()]

# 2. Missing categories / metadata
missing_categories = df[df["category"].isnull()]

# 3. Invalid category values
invalid_categories = df[
    df["category"].notnull()
    & ~df["category"].isin(valid_categories)
]

# 4. Truncated content
truncated_content = df[
    df["content"] == "Content missing after migration"
]

# 5. Potential duplicate titles
duplicate_titles = df[
    df["title"].notnull()
    & df["title"].duplicated(keep=False)
].sort_values("title")

# Save investigation outputs
missing_titles.to_csv(
    BASE_DIR / "outputs" / "investigation_missing_titles.csv",
    index=False
)

missing_categories.to_csv(
    BASE_DIR / "outputs" / "investigation_missing_categories.csv",
    index=False
)

invalid_categories.to_csv(
    BASE_DIR / "outputs" / "investigation_invalid_categories.csv",
    index=False
)

truncated_content.to_csv(
    BASE_DIR / "outputs" / "investigation_truncated_content.csv",
    index=False
)

duplicate_titles.to_csv(
    BASE_DIR / "outputs" / "investigation_duplicate_titles.csv",
    index=False
)

print("Issue investigation completed.")
print()
print("Missing Titles:", len(missing_titles))
print("Missing Categories:", len(missing_categories))
print("Invalid Categories:", len(invalid_categories))
print("Truncated Content:", len(truncated_content))
print("Potential Duplicate Titles:", len(duplicate_titles))

print()
print("Invalid category values:")
print(invalid_categories["category"].value_counts())