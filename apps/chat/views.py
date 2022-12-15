from flask import Blueprint, render_template, request, session
from flask_login import current_user
from sqlalchemy import or_, case, desc
from apps.accounts.decorators import login_required
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
    messages = Message.query.filter(or_(Message.sender_id == user.id, Message.receiver_id == user.id))
    other = case([(Message.sender_id==user.id, 'receiver_id'),], else_='sender_id')
    print(other)
    messages = messages.order_by(other, desc(Message.created_at)).distinct(other)
    messages = sorted(messages, key=lambda x: x.created_at, reverse=True)
    
    # inbox_list = messages.annotate(other=Case(When(sender=user, then=F('receiver')), default=F('sender'), output_field=CharField())).order_by('other', '-created_at').distinct('other')
    # sorted_inbox_list = sorted(inbox_list, key=lambda_stmt x: x.created_at, reverse=True)
    # all_users = User.objects.filter(is_email_verified=True, is_phone_verified=True, is_active=True).exclude(id=user.id).order_by('name')
    # print(messages)
    print(messages)
    for m in messages:
        print(m.text)
    return render_template('chat/index.html', user=current_user)
