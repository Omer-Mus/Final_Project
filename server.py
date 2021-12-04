
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FieldList
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt

# tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
# app = Flask(__name__, template_folder=tmpl_dir)
app = Flask(__name__)

#
#
# DATABASEURI = "postgresql://user:password@34.74.246.148/proj1part2"
#                   # om2349    xxxxx
#
# #
# # This line creates a database engine that knows how to connect to the URI above.
# #
# engine = create_engine(DATABASEURI)
#
#
# @app.before_request
# def before_request():
#   """
#   This function is run at the beginning of every web request
#   (every time you enter an address in the web browser).
#   We use it to setup a database connection that can be used throughout the request.
#
#   The variable g is globally accessible.
#   """
#   try:
#     g.conn = engine.connect()
#   except:
#     print("uh oh, problem connecting to database")
#     import traceback; traceback.print_exc()
#     g.conn = None
#
# @app.teardown_request
# def teardown_request(exception):
#   """
#   At the end of the web request, this makes sure to close the database connection.
#   If you don't, the database could run out of memory!
#   """
#   try:
#     g.conn.close()
#   except Exception as e:
#     pass
#

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    full_name = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    allergies = db.Column(db.ARRAY(Text), nullable=False)


class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "User Name"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=20)], render_kw={"placeholder": "Password"})
    full_name = StringField(validators=[InputRequired(), Length(
        min=5, max=40)], render_kw={"placeholder": "Full name"})
    email = StringField(validators=[InputRequired(), Length(
        min=4, max=30)], render_kw={"placeholder": "Email"})
    age = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Age"})
    zip_code = StringField(validators=[InputRequired(), Length(
        min=5, max=9)], render_kw={"placeholder": "Zip Code"})
    allergies = StringField(render_kw={"placeholder": "allergies"})

    submit = SubmitField("Register")


    def validate_username(self, username):
        existing_user_username = User.quesry.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "User name already exist! Please choose a different username")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "User Name"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")


@app.route('/', methods=['GET', 'POST'])
def index():

  # DEBUG: this is debugging code to see what request looks like
    print(request.args)

    form = LoginForm()
    error = ""
    try:
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.date).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for("home"))
        return render_template("index.html", form=form)

    except Exception as E:
        error = 'Invalid Credentials. Please try again.'
        return render_template("index.html", form=form, error=error)



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/register.html')
def register():
    print(request.args)
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_passowrd_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index.html"))
    return render_template("register.html", form=form)


@app.route('/signup', methods=['POST'])
def signup():
    print(request.args)

    fname = request.form['fname']
    user_name = request.form['user_name']
    email = request.form['email']
    pword = request.form['pword']
    age = request.form['age']
    allergies = request.form['allergies']
    zip_code = request.form['zip_code']
    return render_template("register.html")

# # Example of adding new data to the database
# @app.route('/add', methods=['POST'])
# def add():
#   # name = request.form['name']
#   # g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
#   return redirect('/')


# @app.route('/', methods=['POST'])
# def login():
#     print(request.args)
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             return redirect(url_for('home'))
#
#     return render_template('index.html', error=error)

if __name__ == "__main__":

    import click
    # @click.command()
    # @click.option('--debug', is_flag=True)
    # @click.option('--threaded', is_flag=True)
    # @click.argument('HOST', default='0.0.0.0')
    # @click.argument('PORT', default=8111, type=int)
    #
    # def run(debug, threaded, host, port):
    #   HOST, PORT = host, port
    #   print("running on %s:%d" % (HOST, PORT))
    #   app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
    #
    # run()
    app.run(debug=True)