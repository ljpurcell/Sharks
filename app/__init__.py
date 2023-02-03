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


    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login():
        return render_template('auth/login.html')

    @app.route('/register')
    def register():
        return render_template('auth/register.html')

    @app.route('/next-game', methods=['GET'])
    def next_game():
        from .next_and_prev_game import NextGame
        return render_template('next.html', next_game=NextGame)

    @app.route('/votes')
    def votes():
        from .next_and_prev_game import PrevGame
        team = ["Lyndon Purcell", "Michael Walter", "Ian Johnson"] # Create get_team()
        return render_template('votes.html', prev_game=PrevGame, team=team, total_votes=0)

    @app.errorhandler(404) 
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    return app