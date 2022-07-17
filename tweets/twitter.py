from os import getenv
import tweepy
from .models import DB, Tweet, User
import spacy

# Get API keys from .env file
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')

# Connect to the Twitter API
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)

# Add a new user to the database if they do not already exist
# If the user already exists in the DB, grab their most recent tweets

def add_or_update_user(username):
    '''Takes username (twitter handle) and pulls user 
    and tweet data from twitter API'''

    try:
        # Get the user data
        twitter_user = TWITTER.get_user(screen_name=username)

        # Create a db_user from db model (check to see if db user already exists)
        db_user = (User.query.get(twitter_user.id) or User(id=twitter_user.id, username=username))

        # Add the user to the database
        DB.session.add(db_user)

        # Get the user's tweets
        tweets = twitter_user.timeline(count=200, 
                                        exclude_replies=True, 
                                        include_rts=False, 
                                        tweet_mode='extended',
                                        since_id=db_user.newest_tweet_id)

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # Pull out only the tweet information that we care about from the list of tweets
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, 
                            text=tweet.full_text[:300],
                            vect=tweet_vector)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print(f"Error Processing {username}: {e}")
        raise e
    else:
        DB.session.commit()

nlp = spacy.load('my_model/')

def vectorize_tweet(tweet_text):
    '''return the word embedding for a given string of text'''
    return nlp(tweet_text).vector