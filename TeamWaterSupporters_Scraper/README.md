# TeamWater Scraper

---

## All Functions Defined

All functions are defined in their respective modules:

### 0. `scraper.py` – Main Orchestration Script

- `run_scraper(start_url: str, output_path: str)`  
  Orchestrates the scraping workflow:
  1. Fetch page(s) using `fetcher.get_all_pages()`
  2. Parse supporter data using `parser.parse_multiple_pages()`
  3. Clean data using `cleaner.clean_data()`
  4. Export to CSV using `exporter.export_to_csv()`

---

### 1. `fetcher.py` – Functions to Fetch HTML Content (Static and Dynamic)

- `get_all_pages(start_url: str) -> list`  
  Entry point for fetching all pages, handles pagination and dynamic content.
- `fetch_static_page(url: str) -> str`  
  Fetches static HTML content using `requests`.
- `fetch_dynamic_page(url: str, driver_path=None) -> str`  
  Fetches dynamically loaded HTML using Selenium, waits for content to load, handles pagination.
- `get_driver() -> webdriver.Chrome`  
  Sets up and returns a configured Selenium Chrome driver.
- `innerHTMLChanged(locator, oldHTML="") -> callable`  
  Custom Expected Condition: waits until the innerHTML of an element changes.
- `findNextButton(locator, search)
