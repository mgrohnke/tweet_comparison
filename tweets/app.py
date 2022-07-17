from flask import Flask, render_template, request

from tweets.twitter import add_or_update_user
from tweets.models import DB, User
from tweets.predict import predict_user

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
        # set "users" to empty list if no users in database
        if not User.query.all():
            return render_template('base.html', users=[])

        # query all users if users in database
        return render_template('base.html', users=User.query.all())

    @app.route('/add_user', methods=['POST'])
    def add_user():

        user = request.form.get('user_name')

        try:
            response = get_user_and_tweets(user)

            # response will be value 0 or greater.  If it is 0, no tweets added
            if not response:
                return 'Nothing added' \
                        '<br><br><a href="/" class="button warning">Go Back!</a'

            # if response is 1 or greater, tweets added
            else:
                return f'User: {user} successfully added!' \
                        '<br><br><a href="/" class="button warning">Go Back!</a'

        except Exception as e:
            return str(e)


    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):

        try:
            tweets = User.query.filter(User.name == name).one().tweets

        except Exception as e:
            message = f'Error adding @{name}: {e}'
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def predict():
        user0 = request.form.get('user0')
        user1 = request.form.get('user1')
        tweet_text = request.form.get('tweet_text')

        prediction = predict_user(user0, user1, tweet_text)

        message = '"{}" is more likely to be said by @{} than @{}'.format(
            tweet_text, user0 if predection else user1,
            user1 if prediction else user0
        )

        return message + '<br><br><a href="/" class="button warning">Go Back!</a>'

    # make the route for adding user
    @app.route('/reset')
    def reset():
              
        #remove everything from database
        DB.drop_all()

        #create a new DB with indicated tables
        DB.create_all()

        return 'Database Reset'

    return app