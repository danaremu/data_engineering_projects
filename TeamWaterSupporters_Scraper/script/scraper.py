"""
scraper.py

Main script to scrape supporter data from TeamWater.org donations page,
clean it, and export to CSV.
"""

print("[INFO] Start all libraries installation...")
import os
import fetcher, parser, cleaner, exporter
print("[INFO] All libraries installed correctly...")


# -----------------------------
# Logging Levels
# -----------------------------
# Use these levels consistently across all modules for clarity.
# Logging levels to indicate the severity of messages:
# [NOTSET] → Special level; inherits parent logger’s level. Rarely used directly.
# [TRACE] → (optional/custom) Even more granular than DEBUG; logs every small step in the code. Not standard in Python logging but can be added manually.
# [DEBUG] → Very detailed information, for diagnosing problems. Usually turned off in production.
# [VERBOSE] → Similar to TRACE, sometimes used instead of DEBUG for detailed messages.
# [INFO] → regular program flow, like “Page loaded successfully”.
# [NOTICE] → (optional/custom) for important but non-error events. Not a warning. Used in some systems like syslog., e.g., “Fetched 100 records”.
# [WARN] → something unusual, e.g., “Next button is disabled”.
# [ERROR] → caught exceptions or failed operations.
# [ALERT] → (optional/custom) for very serious issues that need immediate attention. May not stop the program.
# [CRITICAL] → unrecoverable failures, e.g., browser failed to start.
#
#
#
# -----------------------------
# All Functions Defined
# -----------------------------
# All functions are defined in their respective modules:
# 
# 0.
# scraper.py - main orchestration script
# # run_scraper(start_url: str, output_path: str)
# # # Orchestrates the scraping workflow:
# # # # 1. Fetch page(s) using fetcher.get_all_pages()
# # # # 2. Parse supporter data using parser.parse_multiple_pages()
# # # # 3. Clean data using cleaner.clean_data()
# # # # 4. Export to CSV using exporter.export_to_csv()
#
# 1.
# fetcher.py - functions to fetch HTML content (static and dynamic)
# # get_all_pages(start_url: str) -> list
# # # Entry point for fetching all pages, handles pagination and dynamic content
# # fetch_static_page(url: str) -> str
# # # Fetches static HTML content using requests
# # fetch_dynamic_page(url: str, driver_path=None) -> str
# # # Fetches dynamically loaded HTML using Selenium, waits for content to load, handles pagination
# # get_driver() -> webdriver.Chrome
# # # Sets up and returns a configured Selenium Chrome driver
# # innerHTMLChanged(locator, oldHTML="") -> callable
# # # Custom Expected Condition: waits until the innerHTML of an element changes
# # findNextButton(locator, searchText="") -> callable
# # # Custom Expected Condition: waits for a button with matching text to appear
# # openNextPage(delay=0) -> bool
# # # Clicks the 'Next' button if available, returns True if navigation succeeds, False otherwise
# parser.py  - functions to parse supporter data from HTML
# 
# 2.
# # parse_supporter_block(html_block) -> dict
# # # Parses a single supporter HTML block and extracts fields:
# # # name, amount, date, location, message
# # safe_get_text(block, tag, class_name, default="")
# # # Helper function: safely get text from a tag with a given class, returns default if missing
# # safe_get_html(block, tag, class_name, default="")
# # # Helper function: safely get innerHTML from a tag with a given class, returns default if missing
# # parse_page(html_content: str, page_no: int) -> list
# # # Parses all supporter blocks in a single HTML page and returns a list of dictionaries
# # parse_multiple_pages(list_of_html: list) -> list
# # # Parses multiple HTML pages and returns a combined list of supporter dictionaries
# 
# 3.
# cleaner.py - functions to clean and standardize parsed data
# # clean_name(name: str) -> str
# # # Trims whitespace and unwanted characters from a name
# # clean_amount(amount: str) -> float
# # # Converts donation amount string (e.g., "$1,000") to a float
# # clean_date(date_str: str) -> str
# # # Converts a date string to standardized YYYY-MM-DD format
# # clean_data(data_list: list) -> list
# # # Applies all cleaning functions to a list of supporter dictionaries and returns cleaned data
# 
# 
# 4.
# exporter.py - functions to export cleaned data to CSV
# # export_to_csv(data_list: list, output_path: str)
# # # Saves the cleaned data list to a CSV file at the specified path
# # validate_csv(output_path: str, sample_csv_path: str = None) -> bool
# # # Optionally validates the CSV file against a sample CSV format, returns True if valid, False otherwise


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
    print(f"[INFO] Fetched {len(pages_html)} pages...")

    # 2. Parse supporter data
    print("[INFO] Parsing supporter data...")
    raw_data = parser.parse_multiple_pages(pages_html)
    print(f"[INFO] Found {len(raw_data)} supporter entries...")

    # 3. Clean data
    print("[INFO] Cleaning data...")
    cleaned_data = cleaner.clean_data(raw_data)

    # 4. Export to CSV
    print("[INFO] Exporting data to CSV...")
    exporter.export_to_csv(cleaned_data, output_path)

    print(f"[INFO] Scraper finished successfully.")


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    run_scraper(START_URL, OUTPUT_FILE)
