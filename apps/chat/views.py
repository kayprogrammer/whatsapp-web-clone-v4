from flask import Blueprint, render_template, request, session
from flask_login import current_user
from apps.accounts.decorators import login_required

chat_router = Blueprint('chat_router', __name__, template_folder="templates")

@chat_router.before_request
@login_required
def before_request():
    """ Execute before all of the chat endpoints. """
    session['current_path'] = request.path
    pass 

@chat_router.route('/home')
def home():
    return render_template('chat/index.html', user=current_user)