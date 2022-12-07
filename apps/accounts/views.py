from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

accounts_router = Blueprint('accounts_router', __name__, template_folder='templates')

@accounts_router.route('/', defaults={'page': 'index'})
@accounts_router.route('/<page>')
def show(page):
    try:
        return render_template(f'pages/{page}.html')
    except TemplateNotFound:
        abort(404)