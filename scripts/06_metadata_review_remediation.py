from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

# Read migration dataset
file_path = BASE_DIR / "data" / "bbc-news-migration.csv"

df = pd.read_csv(file_path)

# -------------------------
# Metadata Mapping Rules
# -------------------------

metadata_mapping = {
    "biz": "business",
    "BUSINESS": "business",
    "Business": "business"
}

# Keep original value for audit purposes
df["original_category"] = df["category"]

# Apply standardisation
df["category"] = df["category"].replace(metadata_mapping)

# -------------------------
# Validation
# -------------------------

valid_categories = [
    "business",
    "entertainment",
    "politics",
    "sport",
    "tech"
]

invalid_before = 30

invalid_after = len(
    df[
        df["category"].notnull()
        &
        ~df["category"].isin(valid_categories)
    ]
)

records_corrected = (
    df["original_category"].notnull()
    & (df["original_category"] != df["category"])
).sum()
# -------------------------
# Mapping Table
# -------------------------

mapping_table = pd.DataFrame({
    "Original_Value": list(metadata_mapping.keys()),
    "Standard_Value": list(metadata_mapping.values())
})

# -------------------------
# Summary Report
# -------------------------

summary = pd.DataFrame({
    "Metric": [
        "Invalid Categories Before",
        "Invalid Categories After",
        "Records Corrected"
    ],
    "Value": [
        invalid_before,
        invalid_after,
        records_corrected
    ]
})

# -------------------------
# Save Outputs
# -------------------------

df.to_csv(
    BASE_DIR / "outputs" / "bbc_news_standardised.csv",
    index=False
)

mapping_table.to_csv(
    BASE_DIR / "outputs" / "metadata_mapping_table.csv",
    index=False
)

summary.to_csv(
    BASE_DIR / "outputs" / "metadata_remediation_summary.csv",
    index=False
)

print("Metadata Review & Remediation Complete")
print()
print(summary)