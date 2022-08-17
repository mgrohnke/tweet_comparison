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

    def __repr__(self):
        return f'[User: {self.name}]'


class Tweet(DB.Model):
    #ID column schema
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)

    #text column schema
    text = DB.Column(DB.Unicode(300))

    #Word Embeddings (vect) Schema
    embeddings = DB.Column(DB.PickleType, nullable=False)

    #user column schema
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)

    #set up relationship between tweets and IDs
    user = DB.relationship('User', backref=DB.backref('tweets'), lazy=True)

    def __repr__(self):
        return f'[Tweet: {self.text}]'