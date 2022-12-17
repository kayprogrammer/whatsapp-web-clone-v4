from flask import Blueprint, render_template, request, session, render_template_string, jsonify
from flask_login import current_user
from sqlalchemy import or_, case, literal_column
from apps.accounts.decorators import login_required
from apps.accounts.models import User
from setup.extensions import db
from . models import Message
import json
import pytz

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
    ).distinct(other)
    sorted_inbox_list = sorted(inbox_list, key=lambda x: x.created_at, reverse=True)
    
    all_users = User.query.filter(User.is_email_verified==True, User.is_phone_verified==True, User.is_active==True, User.id != user.id).order_by('name')

    return render_template('chat/index.html', user=current_user, all_users=all_users, inbox_list=sorted_inbox_list, messages=messages)

@chat_router.route('/show-direct-messages', methods=['POST'])
def show_dms():
    phone = request.form.get('phone')
    user = current_user
    friend = User.query.filter_by(phone=phone).first()
    if not friend:
        return jsonify(error= 'User not found') 

    recent_emojis = session.get('recent_emojis')
    messages = Message.query.filter(
        or_(Message.sender_id == user.id, Message.receiver_id == user.id), 
        or_(Message.sender_id == friend.id, Message.receiver_id == friend.id)
    )
    messages.filter_by(sender_id=friend.id).update(dict(is_read=True))
    messages = messages.order_by(Message.created_at)
    response = dict()
    response['success'] = True
    response['html_data'] = render_template('chat/dm-page.html', messages=messages, friend= friend, recent_emojis= recent_emojis, user=user)
    
    return jsonify(response)

@chat_router.route('/send-message', methods=['POST'])
def send_message():
    user = current_user
    data = request.form
    message = data.get('message')
    friend = User.query.filter_by(phone=data.get('phone')).first()
    if not friend:
        return jsonify(error= 'User not found') 
    if len(message) < 1:
        return jsonify(error= "You didn't type anything")

    # Solve recent emojis
    recent_emojis = session.get('recent_emojis')
    em = []
    for i in message:
        # if i in emojis:
        if recent_emojis and i in recent_emojis:
            recent_emojis.remove(i)
        em.append(i)
            

    if len(em) > 0:
        em = list(set(em)) # remove duplicates
        if recent_emojis:
            updated_emojis = em + recent_emojis
            if len(updated_emojis) > 50:
                n = len(updated_emojis) - 50
                del updated_emojis[-n:]
            session['recent_emojis'] = updated_emojis
        else:
            updated_emojis = em
            if len(updated_emojis) > 50:
                n = len(updated_emojis) - 50
                del updated_emojis[-n:]
            session['recent_emojis'] = updated_emojis

    message_object = Message(sender_id=user.id, receiver_id=friend.id, text=message)
    db.session.add(message_object)
    db.session.commit()
    time = message_object.created_at.astimezone(pytz.timezone(user.tzname))
    return jsonify(success=True, message= message, time= time.strftime('%I:%M %p'))
