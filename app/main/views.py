from flask import render_template, flash, url_for, redirect, request
from . import main, RegistrationForm, LoginForm


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm
    if request.method == 'GET':
        return render_template('auth/login.html', form=form)
    else:
        if True: # If user successfully logs in
            # Store user in session['name'] and access via session.get('name')
            flash('Nice')
            return redirect(url_for('index.html'))
        else:
            flash('Unrecognised details')
            return redirect(url_for('auth/register.html'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm
    # if request.method == 'POST':
    #     TODO
    #     name = form.data['name']
    #     password = form.data['password']
    #     db.session.add(User(name, password))
    #     db.session.commit()
    # else:
    return render_template('auth/register.html', form=form)
    


@main.route('/next-game', methods=['GET'])
def next_game():
    from ..next_and_prev_game import NextGame
    return render_template('next.html', next_game=NextGame)

@main.route('/votes')
def votes():
    from ..next_and_prev_game import PrevGame
    team = ["Lyndon Purcell", "Michael Walter", "Ian Johnson"] # Create get_team()
    return render_template('votes.html', prev_game=PrevGame, team=team, total_votes=0)

