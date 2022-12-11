from flask import Blueprint, render_template, request, redirect, url_for, flash
from . forms import RegisterForm, LoginForm
from . models import User, Timezone
from flask_login import current_user, login_required, login_user, logout_user
from setup.extensions import login_manager
from . senders import Util
from . tokens import Token

accounts_router = Blueprint('accounts_router', __name__, template_folder="templates")

@accounts_router.route('/register', methods=['GET', 'POST'])
def register():
    print(current_user)
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
        render_template('accounts/email-activation-sent.html', resent=False, email=user.email)
    else:
        print(form.errors)
    return render_template('accounts/register.html', form=form)

@accounts_router.route('/activate-user/<token>/<user_id>/', methods=['GET'])
def activate_user(token, user_id):
    try:
        user_obj = User.query.filter_by(id=user_id).first()
    except:
        flash('You entered an invalid link!', 'error')
        return redirect(url_for("accounts_router.login"))
    user = Token.verify_activation_token(token)
    if not user:
        return render_template('accounts/email-activation-failed.html', email=user_obj.email)
    if user.id != user_obj.id:
        flash('You entered an invalid link!', 'error')
        return redirect(url_for("accounts_router.login"))

    flash('Activation successful!. You can login now!', 'success')
    return redirect(url_for("accounts_router.login"))

@accounts_router.route('/resend-activation-email/<email>/', methods=['GET'])
def resend_activation_email(email):
    user_obj = User.query.filter_by(email=email).first()
    if not user_obj:
        flash('Something went wrong!', 'error')
        return redirect(url_for("accounts_router.login"))
    if user_obj.is_email_verified:
        flash('Email address already verified!', 'warning')
        return redirect(url_for("accounts_router.login"))

    Util.send_verification_email(request, user_obj)
    return render_template('accounts/email-activation-sent.html', resent=True, email=email)


@accounts_router.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        print(form.email_or_phone.data)
        user = User.query.filter_by(email=form.email_or_phone.data).first() or User.query.filter_by(phone=form.email_or_phone.data).first()
        if not user:
            flash('Invalid credentials', 'error')
            return redirect(url_for('accounts_router.login'))
        password_check = user.check_password(form.password.data)
        if password_check == False:
            flash('Invalid credentials', 'error')
            return redirect(url_for('accounts_router.login')) 

        login_user(user)
        return redirect(url_for("chat_router.home"))
    else:
        print(form.errors)
    return render_template('accounts/login.html', form=form)

@accounts_router.route('/logout', methods=['GET'])
def logout():
    logout(current_user)
    return redirect(url_for('accounts_router.login'))
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)