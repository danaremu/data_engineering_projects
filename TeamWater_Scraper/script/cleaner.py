"""
cleaner.py

Module to clean and standardize supporter data before export.
"""

from datetime import datetime

# -----------------------------
# Cleaning functions
# -----------------------------
def clean_name(name: str) -> str:
    """Trim whitespace and unwanted characters."""
    return name.strip()


def clean_amount(amount: str) -> float:
    """Convert donation amount to float."""
    try:
        return float(amount.replace("$", "").replace(",", "").strip())
    except:
        return 0.0


def clean_date(date_str: str) -> str:
    """Standardize date to YYYY-MM-DD format."""
    try:
        dt = datetime.strptime(date_str.strip(), "%d %B %Y")  # Example format
        return dt.strftime("%Y-%m-%d")
    except:
        return ""


def clean_data(data_list: list) -> list:
    """Apply cleaning to entire dataset."""
    cleaned = []
    for entry in data_list:
        cleaned.append({
            "name": clean_name(entry.get("name", "")),
            "amount": clean_amount(entry.get("amount", "0")),
            "date": clean_date(entry.get("date", "")),
            "location": entry.get("location", "").strip(),
            "message": entry.get("message", "").strip()
        })
    return cleaned
