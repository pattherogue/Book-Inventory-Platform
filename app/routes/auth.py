from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db
from werkzeug.urls import url_parse
import logging

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None or not user.check_password(request.form['password']):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=request.form.get('remember_me'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        logging.info(f"Attempting to register user: {username}")
        
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            logging.info(f"User object created: {user}")
            
            db.session.add(user)
            logging.info("User added to session")
            
            db.session.commit()
            logging.info("Session committed successfully")
            
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error during user registration: {str(e)}")
            logging.error(f"Error type: {type(e).__name__}")
            logging.error(f"Error args: {e.args}")
            flash('An error occurred during registration. Please try again.')
    
    return render_template('auth/register.html')