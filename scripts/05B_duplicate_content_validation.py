from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "data" / "bbc-news-migration.csv"
df = pd.read_csv(file_path)

# -------------------------
# Step 1: Identify potential duplicate titles
# Definition: same title
# -------------------------
potential_duplicate_titles = df[
    df["title"].notnull()
    & df["title"].duplicated(keep=False)
].copy()

# -------------------------
# Step 2: Validate true duplicate content
# Definition: same title + same content
# -------------------------
true_duplicate_content = df[
    df["title"].notnull()
    & df["content"].notnull()
    & df.duplicated(subset=["title", "content"], keep=False)
].copy()

# -------------------------
# Step 3: Check metadata conflict among true duplicate content
# Definition: same title + same content, but different category values
# -------------------------
metadata_conflict_summary = (
    true_duplicate_content
    .groupby(["title", "content"])["category"]
    .nunique(dropna=False)
    .reset_index(name="Category_Count")
)

metadata_conflict_keys = metadata_conflict_summary[
    metadata_conflict_summary["Category_Count"] > 1
][["title", "content"]]

metadata_conflicts = true_duplicate_content.merge(
    metadata_conflict_keys,
    on=["title", "content"],
    how="inner"
)

# -------------------------
# Step 4: Save outputs
# -------------------------
potential_duplicate_titles.to_csv(
    BASE_DIR / "outputs" / "potential_duplicate_title_records.csv",
    index=False
)

true_duplicate_content.to_csv(
    BASE_DIR / "outputs" / "true_duplicate_content_records.csv",
    index=False
)

metadata_conflicts.to_csv(
    BASE_DIR / "outputs" / "metadata_conflict_records.csv",
    index=False
)

# -------------------------
# Step 5: Summary
# -------------------------
summary = pd.DataFrame({
    "Check": [
        "Potential Duplicate Title",
        "True Duplicate Content",
        "Metadata Conflict within Duplicate Content"
    ],
    "Record_Count": [
        len(potential_duplicate_titles),
        len(true_duplicate_content),
        len(metadata_conflicts)
    ]
})

summary.to_csv(
    BASE_DIR / "outputs" / "duplicate_validation_summary.csv",
    index=False
)

print("Duplicate Content Validation Complete")
print()
print(summary)

print()
print("Metadata Conflict Records")
print(
    metadata_conflicts[
        ["title", "category"]
    ]
)