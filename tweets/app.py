from flask import Flask, render_template, request
from os import getenv
from .twitter import get_or_update_user
from .models import DB, User, Tweet
from .predict import predict_user

# create a factory for serving up the app when launched
def create_app():
        
    # initialize the flask app
    app = Flask(__name__)

    # configuration
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URI')

    # connect the databse to our app object
    DB.init_app(app)

    # make the "home" or "root" route
    @app.route('/')
    def root():
    # do this when somebody hits the home page
        return render_template('base.html', title='Home', users=User.query.all())

    # update users with their latest tweets
    @app.route('/update')
    def update():
        users = User.query.all()
        usernames = [user.username for user in users]
        for username in usernames:
            get_or_update_user(username)
        return render_template('base.html', title='All users have been updated to include their latest tweets')

    # test another route
    @app.route('/reset')
    def test():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Database Reset')

    # this route is NOT displaying information
    # this route changes our database
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        # grab the username that the user has put into the input box
        name = name or request.values['user_name']

        try:
            if request.method == 'POST':
                get_or_update_user(name)
                message = f'User "{name}" was successfully added.'
            tweets = User.query.filter(User.username == name).one().tweets
        except Exception as e:
            message = f'Error adding {name}: {e}'
            tweets = []
        else:
            return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted([request.values['user0'], request.values['user1']])

        if user0 == user1:
            message = 'Cannot compare a user to themselves!'
        else:
            tweet_text = request.values['tweet_text']
            prediction = predict_user(user0, user1, tweet_text)
            message = '''"{}" is more likely to be said
                        by {} than {}.'''.format(tweet_text,
                                                user1 if prediction else user0,
                                                user0 if prediction else user1)
        return render_template('prediction.html', title='Prediction', message=message)

    return app