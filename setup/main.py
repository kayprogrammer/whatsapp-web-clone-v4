from flask import Flask
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView
from . settings import *
from . extensions import db, bcrypt, csrf, login_manager

from apps.accounts.views import accounts_router
from apps.chat.views import chat_router
from apps.status.views import status_router

from apps.common.models import TimeStampedUUIDModel 
from apps.accounts.models import User, Timezone, BlockedContact, Otp

# with app.app_context():
#     db.create_all()

def register_extensions(app):
    db.init_app(app) 
    Migrate(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

def create_app(config):
    app = Flask(__name__, root_path=ROOT_PATH)
    app.config.from_object(config)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DATABASES['USER']}:{DATABASES['PASSWORD']}@{DATABASES['HOST']}:{DATABASES['PORT']}/{DATABASES['DB_NAME']}"
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    
    # REGISTER ADMIN
    admin = Admin(app, name='WWC V4', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Timezone, db.session))

    # REGISTER BLUEPRINTS
    app.register_blueprint(accounts_router, url_prefix="/accounts")
    app.register_blueprint(chat_router, url_prefix="/chat")
    app.register_blueprint(status_router, url_prefix="/status")
    register_extensions(app)

    return app

app = create_app(config)