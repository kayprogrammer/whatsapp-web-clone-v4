from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

status_router = Blueprint('status_router', __name__, template_folder='templates')

@status_router.route('/', defaults={'page': 'index'})
@status_router.route('/<page>')
def show(page):
    try:
        return render_template(f'pages/{page}.html')
    except TemplateNotFound:
        abort(404)