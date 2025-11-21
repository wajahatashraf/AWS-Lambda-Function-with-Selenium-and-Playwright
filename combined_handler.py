from sys import hash_info

import playwright.sync_api as pw
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import tempfile
import os
from playwright.sync_api import sync_playwright



# ================================
# Playwright handler (fixed flags)
# ================================
def run_playwright():
    # Make sure Playwright uses the pre-installed browser
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/var/task/.playwright"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            # Required for running in Lambda container
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--single-process",
                "--no-zygote",
            ]
        )

        page = browser.new_page()
        page.goto("https://example.com")
        content = page.content()
        browser.close()

    return {"html": content}


# ================================
# Selenium handler (your logic unchanged)
# ================================
def run_selenium():
    chrome_path = "/opt/chrome/chrome-linux64/chrome"
    driver_path = "/opt/chrome-driver/chromedriver-linux64/chromedriver"

    tmp1 = tempfile.mkdtemp()
    tmp2 = tempfile.mkdtemp()
    tmp3 = tempfile.mkdtemp()

    options = Options()
    options.binary_location = chrome_path
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--single-process")
    options.add_argument("--no-zygote")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument(f"--user-data-dir={tmp1}")
    options.add_argument(f"--data-path={tmp2}")
    options.add_argument(f"--disk-cache-dir={tmp3}")

    service = Service(executable_path=driver_path, service_log_path="/tmp/chromedriver.log")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.google.com")
    title = driver.title
    driver.quit()

    return title


# ================================
# Combined Lambda handler
# ================================
def lambda_handler(event, context):
    try:
        playwright_html = run_playwright()
    except Exception as e:
        playwright_html = f"Playwright error: {str(e)}"

    try:
        selenium_title = run_selenium()
    except Exception as e:
        selenium_title = f"Selenium error: {str(e)}"

    return {
        "playwright_html": playwright_html,
        "selenium_title": selenium_title
    }
