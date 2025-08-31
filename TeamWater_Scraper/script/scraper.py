"""
scraper.py

Main script to scrape supporter data from TeamWater.org donations page,
clean it, and export to CSV.
"""

import os
import fetcher, parser, cleaner, exporter

print("All libraries installed correctly")




# -----------------------------
# Configuration
# -----------------------------
START_URL = "https://teamwater.org/donations"
OUTPUT_FOLDER = os.path.join(os.getcwd(), "output")
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "teamwater_supporters.csv")

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# -----------------------------
# Main workflow
# -----------------------------
def run_scraper(start_url: str, output_path: str):
    """
    Orchestrates the scraping workflow:
    1. Fetch page(s)
    2. Parse supporter data
    3. Clean data
    4. Export to CSV
    """

    print("[INFO] Starting scraper...")

    # 1. Fetch all pages
    print("[INFO] Fetching pages...")
    pages_html = fetcher.get_all_pages(start_url)
    print(pages_html)

    # 2. Parse supporter data
    # print("[INFO] Parsing supporter data...")
    # raw_data = parser.parse_multiple_pages(pages_html)
    # print(f"[INFO] Found {len(raw_data)} supporter entries")
    # print(f"[INFO] {raw_data}")

    # # 3. Clean data
    # print("[INFO] Cleaning data...")
    # cleaned_data = cleaner.clean_data(raw_data)

    # # 4. Export to CSV
    # print("[INFO] Exporting data to CSV...")
    # exporter.export_to_csv(cleaned_data, output_path)

    # print(f"[INFO] Scraper finished successfully. CSV saved at: {output_path}")


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    run_scraper(START_URL, OUTPUT_FILE)
