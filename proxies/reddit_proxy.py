import praw
import random as r
from playwright.sync_api import sync_playwright


class RedditClient:
    def __init__(self, client_id, client_secret, user_agent):
        self._backingClient = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)
        self._subreddit_names = ['AITAH', 'AmITheAsshole', 'TIFU', 'Confessions']
        self._subreddit_used = None

    @DeprecationWarning
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
                ps_map[post] = page.locator('shreddit-post').screenshot(path="screenshot.png")
        return ps_map

    def get_post_and_screenshot(self):
        """
        :return: tuple(reddit_post, screenshot)
            reddit_post: praw.submission
        """

        post_final = None
        print("Retrieving Top Post from Subreddits")
        for subreddit_name in self._subreddit_names:
            subreddit = self._backingClient.subreddit(subreddit_name)
            post_id = list(subreddit.top(time_filter='day', limit=1))[0]
            post = self._backingClient.submission(post_id)
            post_final = self.__select_post(post_final, post)
        print("Completed Post Retrieval")

        print("Grabbing Screenshot")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(post_final.url)
            page.wait_for_selector('shreddit-post')
            page.locator('shreddit-post').screenshot(path="screenshot.png")
        print("Saved Screenshot")

        return post_final

    def get_subreddit(self):
        return self._subreddit_used

    @staticmethod
    def __select_post(post_final, post_other):
        if not post_final:
            return post_other

        # by number of upvotes
        if post_final.score != post_other.score:
            return post_final if post_final.score > post_other.score else post_other

        # if they are equal, break the tie with num comments
        return post_final if post_final.num_comments > post_other.num_comments else post_other
