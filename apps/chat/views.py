from flask import Blueprint, render_template, request, session
from flask_login import current_user
from sqlalchemy import or_, case, literal_column
from apps.accounts.decorators import login_required
from apps.accounts.models import User
from . models import Message

chat_router = Blueprint('chat_router', __name__, template_folder="templates")

@chat_router.before_request
@login_required
def before_request():
    """ Execute before all of the chat endpoints. """
    session['current_path'] = request.path
    pass 

@chat_router.route('/home')
def home():
    
    user = current_user
    messages = Message.query.filter(
        or_(Message.sender_id == user.id, Message.receiver_id == user.id)
    )
    other = case(
        [(Message.sender_id == user.id, literal_column("receiver_id") )], 
        else_=literal_column("sender_id")
    )
    inbox_list = messages.order_by(
        other, Message.created_at.desc()
    ).distinct(other).order_by(Message.created_at.desc())
    
    all_users = User.query.filter(User.is_email_verified==True, User.is_phone_verified==True, User.is_active==True, User.id != user.id).order_by('name')

    return render_template('chat/index.html', user=current_user, all_users=all_users, inbox_list=inbox_list, messages=messages)
