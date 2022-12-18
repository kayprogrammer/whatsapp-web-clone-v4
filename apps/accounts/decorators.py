from functools import wraps
from flask import request, redirect, url_for, flash, session
from flask_login import current_user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('accounts_router.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You must logout first!", {"heading": "Not allowed", "tag": "info"})
            return redirect(session.get('current_path'))
        return f(*args, **kwargs)
    return decorated_function