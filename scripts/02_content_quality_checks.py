from pathlib import Path
import pandas as pd

# Project path
BASE_DIR = Path(__file__).resolve().parent.parent

# Read dataset
file_path = BASE_DIR / "data" / "bbc-news-data.csv"

df = pd.read_csv(file_path, sep="\t")

# -------------------------
# QA Check 1
# Missing Title
# -------------------------
missing_title = df["title"].isnull().sum()

# -------------------------
# QA Check 2
# Missing Content
# -------------------------
missing_content = df["content"].isnull().sum()

# -------------------------
# QA Check 3
# Missing Category
# -------------------------
missing_category = df["category"].isnull().sum()

# -------------------------
# QA Check 4
# Duplicate Titles
# -------------------------
duplicate_titles = df["title"].duplicated().sum()

print("===== WEBSITE QA TEST RESULTS =====")
print()

print("Missing Titles:", missing_title)
print("Missing Content:", missing_content)
print("Missing Categories:", missing_category)
print("Duplicate Titles:", duplicate_titles)