from .base_scraper import BaseScraper
from .booking_scraper import BookingScraper
from .expedia_scraper import ExpediaScraper
from .makemytrip_scraper import MakeMyTripScraper

def get_scraper_for_website(url):
    if 'booking.com' in url:
        return BookingScraper()
    elif 'expedia.com' in url:
        return ExpediaScraper()
    elif 'makemytrip.com' in url:
        return MakeMyTripScraper()
    return None