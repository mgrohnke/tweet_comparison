from flask import Flask, render_template
from .models import DB, User, Tweet

#create a factory for serving up the app when launched
def create_app():
        
    #initialized the flask app
    app = Flask(__name__)


    #configuration stuff
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'

    #connect the databse to our app object
    DB.init_app(app)


    #make our "home" or "root" route
    @app.route('/')
    def root():
    #do this when somebody hits the home page
        users = User.query.all()
        return render_template('base.html', users=users)

    #test another route
    @app.route('/test')
    def test():
        #remove everything from database
        DB.drop_all()

        #create a new DB with indicated tables
        DB.create_all()

        #create user object from our .models class
        ryan = User(id=1, username='ryanallred')
        julian = User(id=2, username='julian')

        #add the user to the database
        DB.session.add(ryan)
        DB.session.add(julian)

        #make some tweets
        tweet1 = Tweet(id=1, text='this is some tweet text', user=ryan)
        tweet2 = Tweet(id=2, text='this is some other tweet text', user=julian)

        #add the tweets to the DB session
        DB.session.add(tweet1)
        DB.session.add(tweet2)

        #save the database
        DB.session.commit()

        #display new user on page
        #query to get all users
        users = User.query.all()
        return render_template('base.html', users=users, title='test')

    return app