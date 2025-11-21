from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def run_driverless_test():
    chrome_path = "/usr/bin/chromium"

    options = Options()
    options.binary_location = chrome_path
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com")
    title = driver.title
    driver.quit()

    return title
