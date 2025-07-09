from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
import re

class ExpediaScraper(BaseScraper):
    def scrape(self, destination, duration_days, max_price=None):
        base_url = f"https://www.expedia.com/Hotel-Search?destination={destination}"
        html = self.get_page_with_selenium(base_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        packages = []
        
        for item in soup.select('[data-stid="property-listing-results"] li'):
            try:
                title = item.select_one('[data-test-id="hotel-name"]').text.strip()
                price_element = item.select_one('[data-test-id="price-summary"]')
                price_text = price_element.text.strip() if price_element else "0"
                
                # Extract numeric price
                price_match = re.search(r'[\d,]+', price_text.replace(',', ''))
                price = float(price_match.group()) if price_match else 0
                
                # Convert to rupees if needed
                if '₹' not in price_text:
                    currency = re.search(r'[^\d\s,\.]+', price_text).group() if re.search(r'[^\d\s,\.]+', price_text) else 'USD'
                    price = self.convert_to_rupees(price, currency)
                
                url = "https://www.expedia.com" + item.select_one('a')['href']
                
                package = {
                    'title': title,
                    'destination': destination,
                    'duration_days': duration_days,
                    'price': price,
                    'description': f"Expedia package for {destination} for {duration_days} days",
                    'url': url
                }
                
                if max_price is None or price <= max_price:
                    packages.append(package)
                    
            except Exception as e:
                print(f"Error parsing Expedia item: {e}")
                continue
        
        return packages
