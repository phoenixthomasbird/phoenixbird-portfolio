import tweepy

def post_tweet(message):
    api_key = "your_api_key"
    api_secret = "your_api_secreat"
    access_token = "your_access_token"
    access_token_secret = "your_access_token_secret"

    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(message)

post_tweet("Hello, world! #PythonAutomation")