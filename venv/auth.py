from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User
from __init__ import db
from zipcodeCityState import get_citystate_data


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    emailAddress = request.form.get('emailAddress')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(emailAddress=emailAddress).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        # if user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():

    emailAddress = request.form.get('emailAddress')
    name = request.form.get('name')
    password = request.form.get('password')
    zipcode = request.form.get('zipcode')
    userImage = request.form.get('userImage')
    hikingValue = request.form.get('hiking')
    mountainBikingValue = request.form.get('mountainBiking')
    campingValue = request.form.get('camping')

    cityStateData = get_citystate_data(zipcode)
    city = cityStateData[0]
    state = cityStateData[1]
    userRadius = 20

    if hikingValue:
        hiking = True
    else:
        hiking = False

    if mountainBikingValue:
        mountainBiking = True
    else:
        mountainBiking = False

    if campingValue:
        camping = True
    else:
        camping = False

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(emailAddress=emailAddress).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(emailAddress=emailAddress,
                    name=name,
                    password=generate_password_hash(password, method='sha256'),
                    zipcode=zipcode,
                    city=city,
                    state=state,
                    userRadius=userRadius,
                    userImage=userImage,
                    hiking=hiking,
                    mountainBiking=mountainBiking,
                    camping=camping
                    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    user = User.query.filter_by(emailAddress=emailAddress).first()
    login_user(user)

    return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
