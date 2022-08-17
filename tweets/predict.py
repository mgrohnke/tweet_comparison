import numpy as np
import spacy
import sklearn.linear_model import LogisticRegression

from .models import User

def predict_user(user1_name, user2_name, tweet_text):

    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()

    user1_embeddings = np.array([tweet.embeddings for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embeddings for tweet in user2.tweets])

    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([np.zeros(len(user1.tweets)),
                              np.ones(len(user2.tweets))])

    log_reg = LogisticRegression().fit(embeddings, labels)

    nlp = spacy.load('/my_model')
    tweet_embedding = nlp(tweet_text).vector

    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))
