from flask import Flask, flash, request, redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from os import path, environ as env
from dotenv import load_dotenv
from config import config

# TODO - Make dotenv_path accessible by flask app and not hard coded
dotenv_path = '/Users/LJPurcell/Code/Sharks/.env'
load_dotenv(dotenv_path=dotenv_path)


bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()


def create_app(config_type):
    app = Flask(__name__)

    app.config.from_object(config[config_type])
    config[config_type].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(mail)
    db.init_app(app)
        

    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String, unique=True)
        password = db.Column(db.String, nullable=False)
        mobile = db.Column(db.String, nullable=False)
        email = db.Column(db.String)

        def __repr__(self):
            return '<User %r>' % self.name

    with app.app_context():
        db.create_all()

    
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


    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            # TODO
            # name = form.data['name']
            # password = form.data['password']
            # db.session.add(User(name, password))
            db.session.commit()
        else:
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