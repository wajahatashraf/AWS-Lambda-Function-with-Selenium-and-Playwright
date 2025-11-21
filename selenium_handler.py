import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def lambda_handler(event, context):

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

    service = Service(
        executable_path=driver_path,
        service_log_path="/tmp/chromedriver.log"
    )

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.google.com")
    title = driver.title
    driver.quit()

    return {"statusCode": 200, "body": title}
