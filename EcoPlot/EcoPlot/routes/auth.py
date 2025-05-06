# EcoPlot/routes/auth.py
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from EcoPlot import db
from EcoPlot.models.user import User
from EcoPlot.forms.auth import LoginForm, RegistrationForm, PasswordChangeForm
from urllib.parse import urlparse

auth_bp = Blueprint('auth', __name__)

# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Try to find a user by either username or email
        user = User.query.filter(
            (User.username == form.login.data) | 
            (User.email == form.login.data)
        ).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username/email or password', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)

# Logout route
@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Registration route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! Please complete your profile.', 'success')
        # Log in the user after registration
        login_user(user)
        # Redirect to profile page with first_visit flag
        return redirect(url_for('main.profile', first_visit=True))
    
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordChangeForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect', 'danger')
            return redirect(url_for('auth.change_password'))
        
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('auth/change_password.html', title='Change Password', form=form)