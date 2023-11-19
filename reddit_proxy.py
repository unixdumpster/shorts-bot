import praw

def get_token_parameters():
    # TODO HIDE ID AND SECRET USING VAULT OR SOMETHING
    return {
    'client_id': '0UDKI9xUjEEYVgYMTpkrYA',
    'client_secret': 'JW4dYD3iA5FBiihStxPaaB0y0npNIw',
    'user_agent': 'useragent',
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

