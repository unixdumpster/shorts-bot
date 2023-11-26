import praw
import random as r
from playwright.sync_api import sync_playwright

class RedditClient:
    def __init__(self, client_id, client_secret, user_agent):
        self._backingClient = praw.Reddit(client_id= client_id, 
                                            client_secret=client_secret, 
                                            user_agent=user_agent)
        
        self._subreddit_names = ['AITAH', 'AmITheAsshole', 'TIFU', 'Confessions']
        self._subreddit_used = None

    def get_posts_and_screenshots(self, num_posts):
        self._subreddit_used = self._subreddit_names[r.randint(0, 3)]
        sub = self._backingClient.subreddit(self._subreddit_used)

        ps_map = {}
        posts = list(sub.top(time_filter='day', limit=num_posts))
        for post in posts:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(post.url)
                page.wait_for_selector('shreddit-post')
                ps_map[post.url] = page.locator('shreddit-post').screenshot()
        return ps_map

    def get_subreddit(self):
        return self._subreddit_used