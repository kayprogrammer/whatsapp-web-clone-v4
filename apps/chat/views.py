from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

chat_router = Blueprint('chat_router', __name__, template_folder='templates')

@chat_router.route('/', defaults={'page': 'index'})
@chat_router.route('/<page>')
def show(page):
    try:
        return render_template(f'pages/{page}.html')
    except TemplateNotFound:
        abort(404)