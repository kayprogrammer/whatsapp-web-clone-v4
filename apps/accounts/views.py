from flask import Blueprint, render_template, request, redirect, url_for
from . forms import RegisterForm, LoginForm
from . models import User, Timezone
from flask_login import current_user, login_required, login_user, logout_user
from setup.extensions import login_manager
from . senders import Token, Util

accounts_router = Blueprint('accounts_router', __name__, template_folder='templates')

@accounts_router.route('/register', methods=['GET', 'POST'])
def register():
    # print(vars(request))
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
        Util.send_verification_email(request, user)
        return redirect(url_for("accounts_router.login"))
    else:
        print(form.errors)
    return render_template('accounts/register.html', form=form)

@accounts_router.route('/activate-user/<token>/<email>/', methods=['GET'])
def activate_user(token, email):
    user_obj = User.query.filter_by(email=email).first()
    if not user_obj:
        return render_template('accounts/email-broken-link.html')
    user = Token.verify_activation_token(user_obj, token)
    if user:
        return redirect(url_for("accounts.login"))
    return render_template('accounts/email-activation-failed.html', email=email)

@accounts_router.route('/resend-activation-email/<email>/', methods=['GET'])
def resend_activation_email(email):
    user_obj = User.query.filter_by(email=email).first()
    if not user_obj:
        print('error')
        return
    if user_obj.is_email_verified:
        print('error')
        return

    Util.send_verification_email(request, user_obj)
    return redirect(url_for("accounts_router.login"))


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