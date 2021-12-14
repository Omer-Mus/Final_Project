from flask import Flask, request, render_template, g, redirect, Response, url_for
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FieldList
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
import os
app = Flask(__name__)

bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'


app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    first = db.Column(db.String(40), nullable=True)
    last = db.Column(db.String(40), nullable=True)


class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "User Name"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=20)], render_kw={"placeholder": "Password"})
    email = StringField(validators=[InputRequired(), Length(
        min=4, max=30)], render_kw={"placeholder": "Email"})
    first = StringField(validators=[InputRequired(), Length(
        min=2, max=30)], render_kw={"placeholder": "First name"})
    last = StringField(validators=[InputRequired(), Length(
        min=1, max=30)], render_kw={"placeholder": "Last name"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError("User name already exist! Please choose a different username")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "User Name"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=5, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")


@app.route('/')
def index():

  # DEBUG: this is debugging code to see what request looks like
    print(request.args)
    form = LoginForm(request.form)
    return render_template("index.html", form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    print(request.args)

    form = LoginForm(request.form)
    print("Validation form: ", form.validate_on_submit())
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("home"))
    error = "Invalid Credential! Please try again."
    return render_template("index.html", form=form, error=error)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/register.html', methods=['GET', 'POST'])
def register():
    print(request.args)
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password, email=form.email.data, first=form.first.data, last=form.last.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("register.html", form=form)


@app.route('/home.html')
def home():
    return render_template("home.html")


app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/home-selected.html')
def home_selected():
    return render_template("home-selected.html")

@app.route('/shopping-cart.html')
def shopping_cart():
    return render_template("shopping-cart.html")

@app.route('/shopping-cart-select.html')
def shopping_cart_select():
    return render_template("shopping-cart-select.html")



if __name__ == "__main__":

    import click
    app.run(debug=True)