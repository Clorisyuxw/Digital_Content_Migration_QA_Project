from pathlib import Path
import pandas as pd

# Project path
BASE_DIR = Path(__file__).resolve().parent.parent

# Read original dataset
file_path = BASE_DIR / "data" / "bbc-news-data.csv"
df = pd.read_csv(file_path, sep="\t")

# Make a copy to simulate migrated website content
migration_df = df.copy()

# -------------------------
# Issue 1: Missing metadata
# Missing category after migration
# -------------------------
migration_df.loc[0:9, "category"] = None

# -------------------------
# Issue 2: Invalid metadata / category mapping errors
# Category values changed during migration
# -------------------------
migration_df.loc[10:19, "category"] = "biz"
migration_df.loc[20:29, "category"] = "BUSINESS"
migration_df.loc[30:39, "category"] = "Business"

# -------------------------
# Issue 3: Missing title
# Page title lost during migration
# -------------------------
migration_df.loc[40:49, "title"] = None

# -------------------------
# Issue 4: Truncated content
# Article body content was not migrated correctly
# -------------------------
migration_df.loc[50:59, "content"] = "Content missing after migration"

# Save migrated dataset
output_path = BASE_DIR / "data" / "bbc-news-migration.csv"
migration_df.to_csv(output_path, index=False)

print("Migration dataset created successfully.")
print("Original records:", len(df))
print("Migrated records:", len(migration_df))
print("Output file:", output_path)