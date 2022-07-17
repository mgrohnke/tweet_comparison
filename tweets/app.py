from flask import Flask, render_template, request
from tweets.twitter import add_or_update_user

from .models import DB, User, Tweet
#from .twitter import get_user_and_tweets

# create a factory for serving up the app when launched
def create_app():
        
    # initialize the flask app
    app = Flask(__name__)


    # configuration
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'

    # connect the databse to our app object
    DB.init_app(app)

    # make the "home" or "root" route
    @app.route('/')
    def root():
    # do this when somebody hits the home page
        users = User.query.all()
        return render_template('base.html', users=users)

    @app.route('/update')
    def update():
        users = User.query.all()
        usernames = [user.username for user in users]
        for username in usernames:
            add_or_update_user(username)
        return 'updated'

    @app.route('/populate')
    def populate():
    # do this when somebody hits the home page
        return 'created some users'

    # make the route for adding user
    @app.route('/reset')
    def test():
              
        #remove everything from database
        DB.drop_all()

        #create a new DB with indicated tables
        DB.create_all()

        return 'database reset'

    return app