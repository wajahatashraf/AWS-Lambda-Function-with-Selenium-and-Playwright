import os
from playwright.sync_api import sync_playwright

def lambda_handler(event, context):
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
