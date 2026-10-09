from src.scrapers.bluesky_scraper import BlueskyScraper
from src.database.database import Database
from datetime import datetime
import time
import random

queries = [
    "Toronto",
    "Montreal",
    "Calgary",
    "Ottawa",
    "Edmonton",
    "Winnipeg",
    "Mississauga",
    "Vancouver",
    "Brampton",
    "Hamilton",
    "Surrey",
    "Quebec City",
    "Halifax",
    "Laval",
    "London",
    "Markham",
    "Vaughan",
    "Gatineau",
    "Saskatoon",
    "Kitchener",
    "Longueuil",
    "Burnaby",
    "Windsor",
    "Regina",
    "Oakville"
]
db = Database()


print(
    """
    \n
    +==========================================+
    =              Bluesky Scraper             =
    +==========================================+
    \n
    """
)
while True:

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] Starting scraping...")

    for query in queries:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Scraping → {query}")
        posts = BlueskyScraper(query)
        db.add_posts(posts)
        time.sleep(60 + random.randint(4,15))

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] All queries done → Waiting 1 hour")
    print(f"\n")
    time.sleep(3600)


