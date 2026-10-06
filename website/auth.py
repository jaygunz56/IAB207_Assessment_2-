from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import RegisterForm, LoginForm
from .models import User
from . import db

authbp = Blueprint('auth', __name__)


@authbp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()

        if User.query.filter_by(email=email).first():
            flash('An account with that email already exists, try logging in', 'danger')
            return render_template('register.html', form=form)

        user = User(first_name=form.first_name.data.strip(),
                    last_name=form.last_name.data.strip(),
                    email=email,
                    mobile=form.mobile.data.strip(),
                    password_hash=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f'Welcome aboard {user.first_name}!', 'success')
        return redirect(url_for('main.index'))

    return render_template('register.html', form=form)


@authbp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()

        # same message either way so people can't fish for which emails exist
        if user is None or not check_password_hash(user.password_hash, form.password.data):
            flash('Incorrect email or password', 'danger')
            return render_template('login.html', form=form)

        login_user(user)
        flash(f'Welcome back {user.first_name}', 'success')

        # only follow next if it's a page on our own site
        next_page = request.args.get('next')
        if next_page and next_page.startswith('/') and not next_page.startswith('//'):
            return redirect(next_page)
        return redirect(url_for('main.index'))

    return render_template('login.html', form=form)


@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))
