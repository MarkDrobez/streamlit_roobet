import streamlit as st
from playwright.sync_api import sync_playwright
import pandas as pd
import time

def scrape_roobet_odds():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to Roobet Sportsbook
        url = "https://roobet.com/sports"
        page.goto(url)
        time.sleep(5)  # Allow page to load

        # Extract Odds Data
        events = page.query_selector_all(".bt480")  # Event container
        odds_data = []
        
        for event in events:
            try:
                teams = event.query_selector(".bt366").inner_text()  # Team names
                odds_elements = event.query_selector_all(".bt1941.bt1935.bt1943")  # Odds values
                
                # Extract odds as a list
                odds = [odd.inner_text() for odd in odds_elements if odd.inner_text()]
                
                if len(odds) >= 2:  # Ensure there are enough odds extracted
                    odds_data.append({"Event": teams, "Odds": odds})
            except Exception as e:
                print(f"Error extracting data: {e}")
                continue
        
        browser.close()
        
    # Convert to DataFrame
    df = pd.DataFrame(odds_data)
    return df

# Streamlit UI
st.title("Roobet Odds Scraper")

if st.button("Scrape Odds"):
    st.write("Fetching latest odds...")
    odds_df = scrape_roobet_odds()
    st.write("## Latest Odds")
    st.dataframe(odds_df)
