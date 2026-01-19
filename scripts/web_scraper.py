"""
Web scraper using Selenium with headless Chrome to scrape CNBC World Markets page.
Could not find solution without using this library
"""

import time
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def scrape_cnbc_markets():
    """Scrape CNBC World Markets page and save rendered HTML."""

    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")


    # Initialize the driver
    service =Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        # Navigate to the CNBC World Markets page
        url = "https://www.cnbc.com/world/?region=world"
        print(f"Navigating to {url}...")
        driver.get(url)

        # Wait for MarketCard-symbol elements to load...simulating real world user interaction
        print("Waiting for MarketCard-symbol elements to load...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "MarketCard-symbol"))
        )

        # Sleep for 3 seconds to let JavaScript finish rendering
        print("Sleeping for 3 seconds to let JavaScript finish...")
        time.sleep(3)

        # Get the fully rendered HTML
        html_content = driver.page_source

        # Parse with BeautifulSoup and prettify
        soup = BeautifulSoup(html_content, "html.parser")
        pretty_html = soup.prettify()

        # Find all market symbols from the market banner
        market_symbols = soup.find_all(class_="MarketCard-symbol")
        print(f"Number of market symbols found: {len(market_symbols)}")

        # Ensure output directory exists
        output_path = Path(__file__).parent.parent / "data" / "raw_data" / "web_data.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save the prettified HTML
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(pretty_html)

        print(f"HTML saved to {output_path}")

    finally:
        # Always quit the driver
        driver.quit()
        print("Driver closed.")


if __name__ == "__main__":
    scrape_cnbc_markets()
