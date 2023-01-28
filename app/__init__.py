import os
from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'sharks.sqlite'),
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

 
    from . import db
    db.init_app(app)

    """PAGES"""
    # entry point
    @app.route('/prove-yourself')
    def prove_yourself():
        return "Coming soon" # render_template('prove.html')

    # add user
    @app.route('/register')
    def login():
        return "Coming soon" # render_template('register.html')

    # next game details
    @app.route('/next-game')
    def next_game():
        return "Coming soon" # render_template('next.html')

    return app