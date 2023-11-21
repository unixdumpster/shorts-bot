import praw
import os 
from dotenv import load_dotenv

def get_token_parameters():
    load_dotenv()

    return {
    'client_id': os.getenv("REDDIT_CLIENT_ID"),
    'client_secret': os.getenv("REDDIT_CLIENT_SECRET"),
    'user_agent': os.getenv("REDDIT_USERAGENT")
    }

def get_reddit_client(token_params):
    return praw.Reddit(
        client_id=token_params["client_id"],
        client_secret=token_params["client_secret"],
        user_agent=token_params["user_agent"]
    )

def get_posts(subreddit_name, client, num_posts):
    subreddit = client.subreddit(subreddit_name)
    hottest_posts = subreddit.top(time_filter='week', limit=num_posts)
    return hottest_posts

