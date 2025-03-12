import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def scrape_roobet_odds():
    # Setup Chrome Options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    # Initialize Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Navigate to Roobet Sportsbook
    url = "https://roobet.com/sports"
    driver.get(url)
    time.sleep(5)  # Allow page to load

    # Extract Odds Data
    events = driver.find_elements(By.CLASS_NAME, "bt480")  # Event container

    odds_data = []
    for event in events:
        try:
            teams = event.find_element(By.CLASS_NAME, "bt366").text  # Team names
            odds_elements = event.find_elements(By.CLASS_NAME, "bt1941.bt1935.bt1943")  # Odds values
            
            # Extract odds as a list
            odds = [odd.text for odd in odds_elements if odd.text]
            
            if len(odds) >= 2:  # Ensure there are enough odds extracted
                odds_data.append({"Event": teams, "Odds": odds})
        except Exception as e:
            print(f"Error extracting data: {e}")
            continue

    # Convert to DataFrame
    df = pd.DataFrame(odds_data)
    driver.quit()
    return df

# Streamlit UI
st.title("Roobet Odds Scraper")

if st.button("Scrape Odds"):
    st.write("Fetching latest odds...")
    odds_df = scrape_roobet_odds()
    st.write("## Latest Odds")
    st.dataframe(odds_df)
