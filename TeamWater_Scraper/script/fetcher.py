"""
fetcher.py

Module to fetch HTML content from TeamWater.org.
Supports static and dynamic pages, as well as pagination.
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("excludeSwitches", ["enable-logging"])


print("webdriver-manager is installed and working")



# -----------------------------
# Fetching functions
# -----------------------------
def fetch_static_page(url: str) -> str:
    """Fetch static HTML content using requests."""
    # try:
    #     response = requests.get(url)    # Send HTTP GET request
    #     response.raise_for_status()     # Raise an exception for bad responses (4xx, 5xx)
    #     return response.text            # Get the HTML content
    # except requests.exceptions.RequestException as e:
    #     print(f"Error fetching the page: {e}")


    # try:
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver = webdriver.Chrome(executable_path='E:\\Downloads\\chromedriver.exe')
    # driver.get(url)
    
    # service = Service("C:\\Users\\SurfacePro\\Downloads\\chromedriver.exe")
    # driver = webdriver.Chrome(service=service)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "min-h-160 flex flex-col gap-4"))
    # )
    # html = driver.page_source
    # driver.quit()
    # return html


    print(f"Page Source: {driver.page_source}")
    # Locate the div
    div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "min-h-160 flex flex-col gap-4"))
    )

    # # Store initial content
    initial_text = div.text
    print(f"Initial content: {initial_text}")

    # Wait until content changes
    # initial_text = 'No donations found'
    WebDriverWait(driver, 30).until_not(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "min-h-160 flex flex-col gap-4"), initial_text)
    )

    # Fetch updated content
    updated_html = driver.find_element(By.CLASS_NAME, "min-h-160 flex flex-col gap-4").text
    print(f"Updated content: {updated_html}")
    return updated_html
    # except NoSuchElementException as e:
    #     self.save_screenshot("wait_for_run_process_to_finish")


def fetch_dynamic_page(url: str, driver_path=None) -> str:
    """
    Fetch dynamically loaded HTML using Selenium.
    If driver_path is None, ChromeDriverManager will install it automatically.
    """
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(3)  # Wait for dynamic content to load
    html = driver.page_source
    driver.quit()
    return html


def get_all_pages(start_url: str) -> list:
    """
    Handle multiple pages if pagination exists.
    Returns a list of HTML content strings for all pages.
    """
    # For now, assume single page
    html = fetch_static_page(start_url)
    return [html]
