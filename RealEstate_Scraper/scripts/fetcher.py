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