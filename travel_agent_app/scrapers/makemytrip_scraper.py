from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
import re
from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
import re
import logging
logger = logging.getLogger(__name__)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MakeMyTripScraper(BaseScraper):
    def scrape(self, destination, duration_days, max_price=None):
        DESTINATION_CODE = "DEL"  # Hardcoded for Delhi, can be mapped to other destinations as needed
        base_url = f"https://www.makemytrip.com/hotels/hotel-listing/?checkin=01012024&checkout=01022024&city=CT{DESTINATION_CODE}&country=IN&searchText={destination}&roomStayQualifier=2e0e&locusId=CT{DESTINATION_CODE}&locusType=city"
        
        # Note: For MakeMyTrip, we need destination codes. In a real app, you'd need to map destinations to codes.
        # For simplicity, we'll use Delhi's code here
        base_url = base_url.replace("{DESTINATION_CODE}", "DEL")
        
        html = self.get_page_with_selenium(base_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        packages = []
        
        for item in soup.select('.listingRow'):
            try:
                title = item.select_one('.hotelName').text.strip()
                price_element = item.select_one('.actualPrice')
                price_text = price_element.text.strip() if price_element else "0"
                
                # Extract numeric price (already in INR)
                price_match = re.search(r'[\d,]+', price_text.replace(',', ''))
                price = float(price_match.group()) if price_match else 0
                
                url = "https://www.makemytrip.com" + item.select_one('a')['href']
                
                package = {
                    'title': title,
                    'destination': destination,
                    'duration_days': duration_days,
                    'price': price,
                    'description': f"MakeMyTrip package for {destination} for {duration_days} days",
                    'url': url
                }
                
                if max_price is None or price <= max_price:
                    packages.append(package)
                    
            except Exception as e:
                print(f"Error parsing MakeMyTrip item: {e}")
                continue
        
        return packages
