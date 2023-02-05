import os
from flask import Flask, flash, request, redirect, render_template, session, url_for
from flask_sqlalchemy import SQLAlchemy


def create_app(test_config=None):
    from flask_bootstrap import Bootstrap
    app = Flask(__name__, instance_relative_config=True)
    bootstrap = Bootstrap(app)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String, unique=True)
        mobile = db.Column(db.String, nullable=False)
        email = db.Column(db.String)

        def __repr__(self):
            return '<User %r>' % self.name

    with app.app_context():
        db.create_all()


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

    from . import auth
    app.register_blueprint(auth.bp) # Not sure if this is doing anything


    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('auth/login.html')
        else:
            if True: # If user successfully logs in
                # Store user in session['name'] and access via session.get('name')
                flash('Nice')
                return redirect(url_for('index'))
            else:
                flash('Unrecognised details')
                return redirect(url_for('register'))

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