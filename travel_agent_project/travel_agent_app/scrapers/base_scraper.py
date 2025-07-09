from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class BaseScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def get_page(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            return None
    
    def get_page_with_selenium(self, url):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(url)
            time.sleep(5)  # Wait for JavaScript to load
            page_source = driver.page_source
            driver.quit()
            return page_source
        except Exception as e:
            print(f"Error with Selenium: {e}")
            return None
    
    def scrape(self, destination, duration_days, max_price=None):
        raise NotImplementedError("Subclasses must implement this method")
    
    def convert_to_rupees(self, price, currency):
        # Simple conversion rates (in a real app, use an API for current rates)
        conversion_rates = {
            'USD': 83.0,
            'EUR': 89.0,
            'GBP': 105.0,
            'INR': 1.0
        }
        
        if currency.upper() in conversion_rates:
            return round(float(price) * conversion_rates[currency.upper()], 2)
        return price
