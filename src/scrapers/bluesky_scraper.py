import requests

class BlueskyScraper:
    """
    BlueskyScraper scrapes bluesky for data regarding a given query.
    Arguments:
        query - query phrase to scrape posts for
    Returns:
        posts with the query phrase
    """

    def __new__(self, query):
        self._query = query
        posts = self._get_posts(self, self._query)
        posts = self._clean_posts(self, posts)
        return posts

    def _get_posts(self, query):
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
            "limit": 100
            }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url= url, params= params, headers= headers)
        return response.json()['posts']

    def _clean_posts(self, posts):
        """
        Cleans posts for later use
        Arguments:
            posts - posts to clean
        Returns:
            list of clean posts
        """
        clean_posts = []
        for post in posts:
            post_data = (
                post["uri"],
                self._query,
                post["author"]["handle"],
                post["record"]["text"],
                post["record"]["createdAt"]
            )
            clean_posts.append(post_data)
        return clean_posts