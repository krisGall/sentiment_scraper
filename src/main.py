from scrapers.bluesky_scraper import BlueskyScraper
from database.database import Database
from utils.scraper_utils import random_sleep
from utils.terminal_utils import show_header, get_current_time
import configparser
import time

def main():

    # Loading settings
    config = configparser.ConfigParser()
    config.read("src/settings.ini")
    queries = config["queries"]["queries"].split(sep=',')
    
    # Setting up
    show_header()
    db = Database()

    while True:
        
        print(f"[{get_current_time()}] Starting scraping...")

        # Scraping Bluesky based on queries in settings.ini
        for query in queries:
            print(f"[{get_current_time()}] Scraping → {query}")
            posts = BlueskyScraper(query)
            db.add_posts(posts)
            random_sleep(base=60, bounds=(4,15))
        
        print(f"[{get_current_time()}] All queries done → Waiting 1 hour")
        print(f"[{get_current_time()}] Sleeping...")
        time.sleep(3600)

        
    