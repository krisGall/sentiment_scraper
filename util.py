'''
Functions for the scraper
'''
import requests


def get_bluesky_posts(query):
    """
    Returns latest 100 bluesky posts for a given query.
    Arguments:
        query - query to find posts for.
    Returns:
        list of posts in JSON format
    """
    url = "https://api.bsky.app/xrpc/app.bsky.feed.searchPosts"
    params = {
        "q": query,
        "sort": "latest",
        "limit": 1
        }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url= url, params= params, headers= headers)
    return response.json()['posts']

