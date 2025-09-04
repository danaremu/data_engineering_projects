"""
exporter.py

Module to export cleaned supporter data to CSV.
"""
print("[INFO] --- Installing 'EXPORTER' libraries...")

import pandas as pd



# -----------------------------
# Configuration
# -----------------------------

# -----------------------------
# Export functions
# -----------------------------
def export_to_csv(data_list: list, output_path: str):
    """Save the cleaned data to a CSV file."""
    df = pd.DataFrame(data_list)
    df.to_csv(output_path, index=False)
    print(f"[INFO] CSV exported to: {output_path}")


def validate_csv(output_path: str, sample_csv_path: str = None) -> bool:
    """
    Optional: Validate CSV against sample format.
    Returns True if valid, else False.
    """
    try:
        df = pd.read_csv(output_path)
        if sample_csv_path:
            sample_df = pd.read_csv(sample_csv_path)
            if list(df.columns) != list(sample_df.columns):
                print("[WARN] CSV headers do not match sample")
                return False
        return True
    except Exception as e:
        print(f"[ERROR] CSV validation failed: {e}")
        return False
