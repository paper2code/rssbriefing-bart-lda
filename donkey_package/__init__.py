import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the WSGI application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'donkey.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # use route() decorator to tell Flask what URL should trigger our function
    # URL --> function
    # to go function --> URL, use url_for(function_string)
    # By default, a route only answers to GET requests
    @app.route('/')
    # The function is given a name which is also used to generate URLs for that particular function,
    # and returns the message we want to display in the user’s browser
    def hello_world():
        # The return value from a view function is automatically converted into a response object
        # for you.
        return 'Hello wurd!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import rss_reader
    app.register_blueprint(rss_reader.bp)
    app.add_url_rule('/', endpoint='index')

    return app