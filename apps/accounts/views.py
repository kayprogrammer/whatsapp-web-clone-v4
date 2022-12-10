from flask import Blueprint, render_template, request, redirect, url_for
from . forms import RegisterForm, LoginForm
from . models import User, Timezone
from flask_login import current_user, login_required, login_user, logout_user
from setup.extensions import login_manager

accounts_router = Blueprint('accounts_router', __name__, template_folder='templates')

@accounts_router.route('/register', methods=['GET'])
def register():
    print(vars(request))
    form = RegisterForm(request.form)
    timezones = Timezone.query.all()
    timezones_list=[(t.name, t.name) for t in timezones]
    form.tz.choices = timezones_list
    if form.validate_on_submit():
        user = User.create_user(
            name=form.name.data,
            email=form.email.data.lower(),
            phone=form.phone.data,
            tz=form.tz.data,
            password=form.password.data,
            terms_agreement=form.terms_agreement.data,
        )
        return redirect(url_for("accounts_router.login"))
    else:
        print(form)
    return render_template('accounts/register.html', form=form)

@accounts_router.route('/login', methods=['GET'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.create(
            username=form.username.data,
            email=form.email.data.lower(),
            password=form.password.data,
            is_active=True,
        )
        return redirect(url_for("accounts_router.login"))
    else:
        print(form)
    return render_template('accounts/login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)