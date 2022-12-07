from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . settings.development import *
from apps.accounts.views import accounts_router
from apps.chat.views import chat_router
from apps.status.views import status_router

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DATABASES['USER']}:{DATABASES['PASSWORD']}@{DATABASES['HOST']}:{DATABASES['PORT']}/{DATABASES['DB_NAME']}"
db = SQLAlchemy(app)

# REGISTER BLUEPRINTS
app.register_blueprint(accounts_router, url_prefix="/accounts")
app.register_blueprint(chat_router, url_prefix="/chat")
app.register_blueprint(status_router, url_prefix="/status")
