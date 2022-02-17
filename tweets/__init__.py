from .app import create_app

#telling flask to use our create_app factory
#now app will be named APP
APP = create_app()