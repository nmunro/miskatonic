from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from miskatonic.apps.admin.forms import LoginForm
from .models import Person


admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = Person.select().where(Person.username == form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('admin.login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template(
        'pages/admin/login.tmpl.html',
        title='Log in',
        form=form,
        active=f'home',
    )


@admin.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
