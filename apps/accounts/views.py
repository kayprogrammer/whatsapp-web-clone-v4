from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . forms import RegisterForm, LoginForm, OtpVerificationForm, PasswordResetRequestForm, PasswordResetForm
from . models import User, Timezone
from flask_login import login_user, logout_user
from . decorators import login_required, logout_required
from setup.extensions import login_manager, db
from . senders import Util
from . tokens import Token

accounts_router = Blueprint('accounts_router', __name__, template_folder="templates")

@accounts_router.route('/register', methods=['GET', 'POST'])
@logout_required
def register():
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
        return render_template('accounts/email-activation-request.html', detail='sent', email=user.email)
    return render_template('accounts/register.html', form=form)

@accounts_router.route('/activate-user/<token>/<user_id>/', methods=['GET'])
@logout_required
def activate_user(token, user_id):
    user_obj = User.query.filter_by(id=user_id).first()
    if not user_obj:
        flash("You entered an invalid link!", {"heading": "Invalid", "tag": "error"})
        return redirect(url_for("accounts_router.login"))
    user = Token.verify_activation_token(token)
    if not user:
        return render_template('accounts/email-activation-failed.html', email=user_obj.email)
    if user.id != user_obj.id:
        flash("You entered an invalid link!", {"heading": "Invalid", "tag": "error"})
        return redirect(url_for("accounts_router.login"))

    user.current_activation_jwt['used'] = True
    user.is_email_verified = True
    db.session.commit()

    if not user.is_phone_verified:
        Util.send_sms_otp(user)
        session['verification_phone'] = user.phone
        flash("Activation successful!. Verify your phone now!", {"heading": "Done", "tag": "success"})
        return redirect(url_for('accounts_router.verify_otp'))

    flash("Activation successful!.", {"heading": "Done", "tag": "success"})
    Util.send_welcome_email(request, user)
    return redirect(url_for("accounts_router.login"))

@accounts_router.route('/resend-activation-email/', methods=['GET'])
@logout_required
def resend_activation_email():
    email = request.cookies.get('activation_email')
    user_obj = User.query.filter_by(email=email).first()
    if not user_obj:
        flash("Something went wrong!.", {"heading": "error", "tag": "error"})
        return redirect(url_for("accounts_router.login"))
    if user_obj.is_email_verified:
        flash("Your email address has already been verified!.", {"heading": "Verified", "tag": "info"})
        return redirect(url_for("accounts_router.login"))

    Util.send_verification_email(request, user_obj)
    return render_template('accounts/email-activation-request.html', detail='resent', email=email)

@accounts_router.route('/verify-otp', methods=['GET', 'POST'])
@logout_required
def verify_otp():
    phone = session.get('verification_phone')
    if not phone:
        flash("Back to login!.", {"heading": "Error!", "tag": "error"})
        return redirect(url_for('accounts_router.login'))
    form = OtpVerificationForm(request.form)
    if form.validate_on_submit():
        flash("You can login now.", {"heading": "Verification complete!", "tag": "success"})
        return redirect(url_for('accounts_router.login'))
    return render_template('accounts/otp-verification.html', form=form)

@accounts_router.route('/resend-otp', methods=['GET'])
@logout_required
def resend_otp():
    phone = session.get('verification_phone')
    if not phone:
        flash("Something went wrong.", {"heading": "Error!", "tag": "info"})
        return redirect(url_for('accounts_router.login'))
    user = User.query.filter_by(phone=phone).first()
    if not user:
        flash("Invalid user.", {"heading": "Error!", "tag": "error"})
        return redirect(url_for('accounts_router.login'))
    if user.is_phone_verified:
        flash("Your phone number has already been verified.", {"heading": "Already verified!", "tag": "info"})
        return redirect(url_for('accounts_router.login'))
    
    Util.send_sms_otp(user)
    flash("A new otp has been sent to your phone number.", {"heading": "Sent!", "tag": "success"})
    return redirect(url_for('accounts_router.verify_otp'))


@accounts_router.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    session['password_reset_email'] = None
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email_or_phone.data).first() or User.query.filter_by(phone=form.email_or_phone.data).first()
        if not user:
            flash("Invalid credentials.", {"heading": "Error!", "tag": "error"})
            return redirect(url_for('accounts_router.login'))
        password_check = user.check_password(form.password.data)
        if password_check == False:
            flash("Invalid credentials.", {"heading": "Error!", "tag": "error"})
            return redirect(url_for('accounts_router.login')) 

        if not user.is_email_verified:
            Util.send_verification_email(request, user)
            return render_template('accounts/email-activation-request.html', detail='request', email=user.email)

        if not user.is_phone_verified:
            Util.send_sms_otp(user)
            session['verification_phone'] = user.phone
            return redirect(url_for('accounts_router.verify_otp'))
        login_user(user)
        return redirect(url_for("chat_router.home"))
    return render_template('accounts/login.html', form=form)

@accounts_router.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('accounts_router.login'))

@accounts_router.route('/request-password-reset', methods=['GET', 'POST'])
@logout_required
def password_reset_request():
    detail = 'first_view'
    form = PasswordResetRequestForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            Util.send_password_reset_email(request, user)
            session['password_reset_email'] = user.email
            detail = 'second_view'
    return render_template('accounts/password-reset-request.html', detail=detail, form=form)

@accounts_router.route('/verify-password-reset-token/<token>/<user_id>', methods=['GET', 'POST'])
@logout_required
def verify_password_reset_token(token, user_id):
    detail = 'invalid_token'
    form = None
    try:
        user_obj = User.query.filter_by(id=user_id).first()
    except:
        flash("You entered an invalid link.", {"heading": "Error!", "tag": "error"})
        return redirect(url_for("accounts_router.login"))
    user = Token.verify_reset_token(token)
    
    if user and user.id != user_obj.id:
        flash("You entered an invalid link.", {"heading": "Error!", "tag": "error"})
        return redirect(url_for("accounts_router.login"))
    elif user and user.id == user_obj.id:
        session['password_reset_email'] = user_obj.email
        return redirect(url_for('accounts_router.reset_password'))
    return render_template('accounts/password-reset.html', detail=detail, form=form, email=user_obj.email)

@accounts_router.route('/reset-password', methods=['GET', 'POST'])
@logout_required
def reset_password():
    email=session.get('password_reset_email')
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Not allowed.", {"heading": "Error!", "tag": "error"})
        return redirect(url_for('accounts_router.login'))
    detail = 'valid_token'
    form = PasswordResetForm(request.form)
    if form.validate_on_submit():
        if user:
            user.password = form.newpassword.data
            db.session.commit()
            flash("Your password has been reset.", {"heading": "Success!", "tag": "success"})
            session['password_reset_email'] = None
            return redirect(url_for("accounts_router.login"))
    return render_template('accounts/password-reset.html', detail=detail, form=form, email=email)

@accounts_router.route('/resend-password-token/<email>', methods=['GET'])
@logout_required
def resend_password_token(email):
    detail = 'third_view'
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("Something went wrong.", {"heading": "Error!", "tag": "error"})
        return redirect(url_for("accounts_router.login"))
    
    Util.send_password_reset_email(request, user)
    return render_template('accounts/password-reset-request.html', detail=detail, form=None)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()