import os
from flask import Flask, render_template


def create_app(test_config=None):
    from flask_bootstrap import Bootstrap
    app = Flask(__name__, instance_relative_config=True)
    bootstrap = Bootstrap(app)

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

 
    from . import db, auth
    db.init_app(app)
    app.register_blueprint(auth.bp)

    

    # next game details
    @app.route('/next-game', methods=['GET'])
    def next_game():
        from .next_game import NextGame
        return render_template('next.html', next_game=NextGame)

    @app.errorhandler(404) 
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    return app