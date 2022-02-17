from pickle import FALSE
from flask_sqlalchemy import SQLAlchemy

#create a database object
#opening up the db connection
DB = SQLAlchemy()

#create a table in the DB
#using python classes

class User(DB.Model):
    #for the different columns in db,
    #each one will be its own attribute on this class

    #ID column schema
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)

    #username column schema
    username = DB.Column(DB.String, nullable=False)

    #the backref down below automatically adds a list of tweets here
    #tweets = []

class Tweet(DB.Model):
    #ID column schema
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)

    #text column schema
    text = DB.Column(DB.Unicode(300))

    #user column schema
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)

    #set up relationship between tweets and IDs
    #this will automatically add new id to both the tweet and user
    user = DB.relationship('User', backref=DB.backref('tweets'), lazy=True)