"""
scraper.py

Main script to scrape supporter data from TeamWater.org donations page,
clean it, and export to CSV.
"""

print("[INFO] Start all libraries installation...")
import os
import fetcher, parser, cleaner, exporter
print("[INFO] All libraries installed correctly...")



#
# -----------------------------
# All Functions Defined
# -----------------------------
# All functions are defined in their respective modules:
# 
# 0.
# scraper.py - main orchestration script
# # run_scraper(start_urls: list, output_path: str)
# # # Orchestrates the scraping workflow:
# # # # 1. Iterates through the 8 target portals
# # # # 2. Fetch page(s) using fetcher.get_all_pages()
# # # # 3. Parse property data using parser.parse_multiple_pages()
# # # # 4. Clean data using cleaner.clean_data()
# # # # 5. Export consolidated results using exporter.export_to_csv()
#
# 
# 1.
# fetcher.py - functions to fetch HTML content (static and dynamic)
# # get_driver() -> webdriver.Chrome
# # # Sets up and returns a configured Selenium Chrome driver
# # fetch_static_page(url: str) -> str
# # # Fetches static HTML content using requests
# # fetch_dynamic_page(url: str, driver_path=None) -> str
# # # Fetches dynamically loaded HTML using Selenium, waits for content to load
# # get_all_pages(start_url: str) -> list
# # # Entry point for fetching all pages for a given URL, handles pagination and dynamic content
# # innerHTMLChanged(locator, oldHTML="") -> callable
# # # Custom Expected Condition: waits until the innerHTML of an element changes
# # findNextButton(locator, searchText="Next") -> callable
# # # Custom Expected Condition: waits for a button with matching text to appear
# # openNextPage(delay=0) -> bool
# # # Clicks the 'Next' button if available, returns True if navigation succeeds, False otherwise
#
# 
# 2.
# parser.py - functions to parse property data from HTML
# # parse_property_block(block) -> dict
# # # Parses a single property block and extracts fields (address, price, beds, baths, sqft, agent, url)
# # safe_get_text(block, selector: str, default="") -> str
# # # Helper: safely extract text from a CSS selector, return default if missing
# # safe_get_attr(block, selector: str, attr: str, default="") -> str
# # # Helper: safely extract an attribute (like href) from a CSS selector
# # parse_page(html_content: str, page_index: int) -> list
# # # Parses all property blocks in a single HTML page, returns list of dictionaries
# # parse_multiple_pages(list_of_html: list) -> list
# # # Parses multiple HTML pages, aggregates property dictionaries
#
# 
# 3.
# cleaner.py - functions to clean and standardize parsed data
# # clean_price(price_str: str) -> float
# # # Converts price string (e.g., "$1,250,000") to float
# # clean_sqft(sqft_str: str) -> int
# # # Converts square footage string to integer
# # clean_beds(beds_str: str) -> int
# # # Extracts integer from bedroom count string
# # clean_baths(baths_str: str) -> float
# # # Extracts number (including halves) from bathroom string
# # clean_date(date_str: str) -> str
# # # Converts listing date to standardized YYYY-MM-DD format
# # clean_data(data_list: list) -> list
# # # Applies all cleaning functions, deduplicates by address+price, and returns cleaned data
#
#
# 4.
# exporter.py - functions to export cleaned data
# # export_to_csv(data_list: list, output_path: str)
# # # Saves cleaned property data to CSV at specified path
# # export_to_json(data_list: list, output_path: str)
# # # Saves cleaned property data to JSON file
# # validate_output(data_list: list, required_fields: list) -> bool
# # # Ensures required fields (address, price, etc.) exist in all rows, returns True if valid



# -----------------------------
# Configuration
# -----------------------------
START_URLS = [
    ["Staten Island MLS", "https://www.siborrealtors.com/search"],
    ["Brooklyn MLS (Sales)", "https://www.brooklynmls.com/buy/"],
    ["Street Easy (Sales)", "https://streeteasy.com/for-sale/nyc"],
    ["Street Easy (Rentals)", "https://streeteasy.com/for-rent/nyc"],
    ["One Key MLS (Sales)", "https://www.onekeymls.com/homes"],
    ["One Key MLS (Rentals)", "https://www.onekeymls.com/homes/for-rent"],
    ["One Key MLS (Commercial Sales)", "https://www.onekeymls.com/homes/commercial/buy"],
    ["One Key MLS (Commercial Rentals)", "https://www.onekeymls.com/homes/commercial/rent"]
]
OUTPUT_FOLDER = os.path.join(os.getcwd(), "output")
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "realestate.csv")

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# -----------------------------
# Process each portal
# ----------------------------- Helper to process each portal
def process_portal(start_url: str, output_path: str):
    """
    Processes a single real estate portal:
    1. Fetch all pages
    2. Parse supporter data
    3. Clean data
    4. Export to CSV
    """

    print(f"[INFO] Processing portal: {start_url}")

    # # 1. Fetch all pages
    # print("[INFO] Fetching pages...")
    # pages_html = fetcher.get_all_pages(start_url)
    # print(f"[INFO] Fetched {len(pages_html)} pages...")

    # # 2. Parse supporter data
    # print("[INFO] Parsing supporter data...")
    # raw_data = parser.parse_multiple_pages(pages_html)
    # print(f"[INFO] Found {len(raw_data)} supporter entries...")

    # # 3. Clean data
    # print("[INFO] Cleaning data...")
    # cleaned_data = cleaner.clean_data(raw_data)

    # # 4. Export to CSV
    # print("[INFO] Exporting data to CSV...")
    # exporter.export_to_csv(cleaned_data, output_path)


# -----------------------------
# Main workflow
# -----------------------------
def run_scraper(start_urls: str, output_path: str):
    """
    Orchestrates the scraping workflow:
    1. Fetch page(s)
    2. Parse supporter data
    3. Clean data
    4. Export to CSV
    """

    print("[INFO] Starting scraper...")

    # Loop through major URLs
    for name, url in start_urls:
        print(f"[INFO] Processing portal: {name} - {url}")
        process_portal(url, output_path)

    print(f"[INFO] Scraper finished successfully.")


# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    run_scraper(START_URLS, OUTPUT_FILE)
