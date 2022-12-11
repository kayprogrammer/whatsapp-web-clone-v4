from flask import Blueprint, render_template
from flask_login import current_user

chat_router = Blueprint('chat_router', __name__, template_folder="templates")

@chat_router.route('/home')
def home():
    return render_template('chat/index.html', user=current_user)