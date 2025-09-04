"""
fetcher.py

Module to fetch HTML content from TeamWater.org.
Supports static and dynamic pages, as well as pagination.
"""
print("[INFO] --- Installing 'FETCHER' libraries...")

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementNotInteractableException



# -----------------------------
# Configuration
# -----------------------------
driver = None
prev_html = None
next_button = None
html = []


# -----------------------------
# Creating Driver Setup
# -----------------------------
def get_driver():
    options = Options()
    options.add_argument("--headless")  # run without opening a browser window
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Pass Service + Options
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


# -----------------------------
# Custom Expected Conditions
# -----------------------------
def innerHTMLChanged(locator, oldHTML=""):
    """
    Custom Expected Condition:
    Wait until the innerHTML of the given locator is different from `oldHTML`.
    Returns: WebElement if changed, otherwise False.
    """
    global driver

    def _predicate(driver):
        try:
            element_ = driver.find_element(*locator)
            if element_.get_attribute('innerHTML') != oldHTML:
                return element_ # return the element (not just HTML string)
            return False
        except:
            return False
        
    return _predicate


def findNextButton(locator, searchText=""):
    """
    Custom expected condition:
    Waits for an element (or multiple) matching locator to contain the given text.
    Returns the element if found, otherwise False.
    """
    global driver
    
    def _predicate(driver):
        try:
            elements_ = driver.find_elements(*locator) # find multiple
            for element_ in elements_:
                if element_.text.strip() == searchText:
                    return element_ # success: return the matching element
            return False
        except Exception as e:
            print(f"[ERROR] findNextButton failed: {e}")
            return False
        
    return _predicate


# -----------------------------
# Configuration
# -----------------------------
def openNextPage(delay=0):
    """
    Click the 'Next' button if available.
    Returns True if navigation succeeded, False otherwise.
    """
    global driver, next_button
    next_btn = (By.TAG_NAME, "button")
    # time.sleep(delay)

    try:
        # Look for 'Next' button if not already found
        if not next_button:
            next_button = WebDriverWait(driver, 30).until(
                findNextButton(next_btn, "Next")
            )

        # Confirm the 'Next' button is clickable/active
        isClickable = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(next_button)
            # EC.element_to_be_clickable(next_btn)
        )
        if not isClickable:
            return False
        
        # Click the 'Next' button
        try:
            next_button.click()  # Normal click (preferred)
            print("[VERBOSE] --- Redirecting to next page.")
            return True
        except Exception:
            print("[WARN] --- Normal click failed, using JS click instead")
            try:
                driver.execute_script("arguments[0].click();", next_button)
                return True
            except Exception as e:
                print(f"[ERROR] --- JS click also failed")
                return False
    
    # Combined exception handling for clarity
    except:
        return False


# -----------------------------
# Fetching For Static Pages
# -----------------------------
def fetch_static_page(url: str) -> str:
    """Fetch static HTML content using requests."""
    global html

    try:
        print(f"[DEBUG] --- Fetching static page: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        html.append(response.text)
    except Exception as e:
        print(f"[ERROR] Could not fetch static page: {e}")
        html = ""
    finally:
        time.sleep(2)
    
    # return the valued HTML
    print("[DEBUG] --- Finished fetching page")
    return html


# -----------------------------
# Fetching For Dynamic Pages
# -----------------------------
def fetch_dynamic_page(url: str, driver_path=None) -> str:
    """
    Fetch dynamically loaded HTML using Selenium.
    If driver_path is None, ChromeDriverManager will install it automatically.
    Returns the page HTML as a string.
    """
    global driver, prev_html, html

    driver = get_driver()
    driver.get(url)
    container_locator = (By.CSS_SELECTOR, ".min-h-160")

    # Debug logging
    print(f"[INFO] --- Opened URL: {url}")
    print(f"[INFO] --- Page title: {driver.title}")

    while True:
        try:
            if not prev_html:
                # print("[VERBOSE] --- Searching for data/content container")
                element = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located(container_locator)
                )
                # print(f"[VERBOSE] --- Data/content container found: {element}")
                prev_html = element.get_attribute('innerHTML')
            
            # print("[VERBOSE] --- Waiting for new data/content to be loaded")
            element = WebDriverWait(driver, 60).until(
                innerHTMLChanged(container_locator, prev_html)
            )
            html.append(element.get_attribute("innerHTML"))
            prev_html = element.get_attribute("innerHTML")

            # After content has been loaded
            # Check for "next" button and click if exists 
            if not openNextPage():
                print("[INFO] No more pages/data available.")
                break
            
        except Exception as e:
            print(f"[ERROR] Could not find container or load data")
            driver.save_screenshot("../error_png/debug_screenshot.png") # save screenshot for debugging
            break
    
    # return the valued HTML
    driver.quit()
    print("[INFO] --- Finished fetching page(s)")
    return html



# -----------------------------
# Entry point
# -----------------------------
def get_all_pages(start_url: str) -> list:
    """
    Handle multiple pages if pagination exists.
    Returns a list of HTML content strings for all pages.
    """

    # For now, assume single page
    # html = fetch_static_page(start_url)
    # html = fetch_dynamic_page(start_url)
    return fetch_dynamic_page(start_url)
