from os import getenv
import tweepy
from .models import DB, Tweet, User
import spacy

# Get API keys from .env file

# Connect to the Twitter API

# Add a new user to the database if they do not already exist
# If the user already exists in the DB, grab their most recent tweets

def add_or_update_user(username):
    '''Takes username (twitter handle) and pulls user 
    and tweet data from twitter API'''

    # Get the user data

    # Create a db_user from db model (check to see if db user already exists)

    # Add the user to the database

    # Check to see if the newest tweet in the DB is equal to the newest tweet
    # from the API

    # Get the user's tweets

    # Pull out only the tweet information that we care about from the list of tweets

    # Save the user and all of the tweets that were added to the DB.session

nlp = spacy.load('my_model/')

def vectorize_tweet(tweet_text):
    '''return the word embedding for a given string of text'''
    return nlp(tweet_text).vector