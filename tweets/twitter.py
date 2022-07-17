import requests
import ast

from .models import DB, Tweet, User

import spacy

# Add a new user to the database if they do not already exist
# If the user already exists in the DB, grab their most recent tweets

def get_user_and_tweets(username):
    '''Takes username (twitter handle) and pulls user 
    and tweet data from twitter API'''

    HEROKU_URL = 'https://lambda-ds-twit-assist.herokuapp.com/user/'

    user = ast.literal_eval(requests.get(HEROKU_URL + username).text)

    nlp = spacy.load('/my_model')

    try:

        if User.query.get(user['twitter_handle']['id']):
            db_user = User.query.get(user['twitter_handle']['id'])
        else:
            db_user = User(id=user['twitter_handle']['id'],
                            name=user['twitter_handle']['username'])
            DB.session.add(db_user)

        tweets_added = 0

        for tweet in user['tweets']:

            if Tweet.query.get(tweet['id']):
                break
            else:
                tweet_text = tweet['full_text']

                db_tweet = Tweet(id=tweet['id'], tweet=tweet_text, embeddings=nlp(tweet_text).vector)

                db_user.tweets.append(db_tweet)

                DB.session.add(db_tweet)

                tweets_added += 1
        
    except Exception as e:
        raise e

    DB.session.commit()

    return tweets_added
