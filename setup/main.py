from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView
from . settings import *
from . extensions import db, bcrypt, csrf, login_manager, mail

from apps.accounts.views import accounts_router
from apps.chat.views import chat_router
from apps.status.views import status_router

from apps.common.models import TimeStampedUUIDModel 
from apps.accounts.models import User, Timezone, BlockedContact, Otp

def register_extensions(app):
    db.init_app(app) 
    Migrate(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = MAIL_PORT
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
    app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
    mail.init_app(app)


def create_app(config):
    app = Flask(__name__, root_path=ROOT_PATH)
    app.config.from_object(config)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DATABASES['USER']}:{DATABASES['PASSWORD']}@{DATABASES['HOST']}:{DATABASES['PORT']}/{DATABASES['DB_NAME']}"
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    # app.wsgi_app = middleware(app.wsgi_app)
    
    # REGISTER ADMIN
    admin = Admin(app, name='WWC V4', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Timezone, db.session))
    admin.add_view(ModelView(BlockedContact, db.session))
    admin.add_view(ModelView(Otp, db.session))

    # REGISTER BLUEPRINTS
    app.register_blueprint(accounts_router, url_prefix="/accounts")
    app.register_blueprint(chat_router, url_prefix="/chat")
    app.register_blueprint(status_router, url_prefix="/status")
    register_extensions(app)

    return app

app = create_app(config)
app.app_context().push()