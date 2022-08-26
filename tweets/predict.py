import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import vectorize_tweet

from .models import User

def predict_user(user0_username, user1_username, hypo_tweet_text):

    # query database for the two users
    user0 = User.query.filter(User.username == user0_username).one()
    user1 = User.query.filter(User.username == user1_username).one()

    # get a list of word embeddings for each user's tweets
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # combine the word embeddings into single large np array
    # X matrix for training
    vects = np.vstack([user0_vects, user1_vects])

    # user np.concatenate() to concatenate one-dimensional numpy arrays
    zeros = np.zeros(len(user0.tweets))
    ones = np.ones(len(user1.tweets))
    # y vector for training
    labels = np.concatenate([zeros, ones])

    # train the logistic regression
    # instantiate the class to create a LR object
    log_reg = LogisticRegression()
    # fit the model ot the data
    log_reg.fit(vects, labels)

    # generate prediction for hypothetical tweet text
    # vectorize the hypothetical tweet text
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    # pass the 2-dimensional array to .predict()
    prediction = log_reg.predict([hypo_tweet_vect])

    return prediction[0]
