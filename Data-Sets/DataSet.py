from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Configure Selenium WebDriver
options = Options()
options.add_argument("--headless")  # Run in headless mode (no browser UI)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

BASE_URL = "https://www.olx.in/mobiles_c1453?page="

def scrape_page(page_number):
    url = BASE_URL + str(page_number)
    driver.get(url)
    time.sleep(3)  # Allow the page to load
    data = []

    # Find all listings
    listings = driver.find_elements(By.CLASS_NAME, "EIR5N")  # Update class if necessary
    for listing in listings:
        try:
            title = listing.find_element(By.CLASS_NAME, "_2tW1I").text
            price = listing.find_element(By.CLASS_NAME, "_89yzn").text
            location = listing.find_element(By.CLASS_NAME, "tjgMj").text
            data.append({"Title": title, "Price": price, "Location": location})
        except Exception:
            continue
    return data

def scrape_data(total_pages):
    all_data = []
    for page in range(1, total_pages + 1):
        print(f"Scraping page {page}...")
        data = scrape_page(page)
        if data:
            all_data.extend(data)
        else:
            print(f"No data found on page {page}")
    return all_data

try:
    # Scrape data from 5 pages as a test
    total_pages = 5
    data = scrape_data(total_pages)
    
    # Save data to a CSV file
    if data:
        df = pd.DataFrame(data)
        df.to_csv("used_mobile_prices_selenium.csv", index=False)
        print("Dataset saved as 'used_mobile_prices_selenium.csv'")
    else:
        print("No data scraped.")
finally:
    driver.quit()
