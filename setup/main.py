from flask import Flask
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_admin.contrib.sqla import ModelView

from . settings import *

from apps.accounts.views import accounts_router
from apps.chat.views import chat_router
from apps.status.views import status_router

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DATABASES['USER']}:{DATABASES['PASSWORD']}@{DATABASES['HOST']}:{DATABASES['PORT']}/{DATABASES['DB_NAME']}"
bcrypt = Bcrypt(app)

from apps.common.models import db, TimeStampedUUIDModel 
from apps.accounts.models import User, Timezone, BlockedContact, Otp

db.init_app(app)
migrate = Migrate(app, db)

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='WWC V4', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Timezone, db.session))
# REGISTER BLUEPRINTS
app.register_blueprint(accounts_router, url_prefix="/accounts")
app.register_blueprint(chat_router, url_prefix="/chat")
app.register_blueprint(status_router, url_prefix="/status")

with app.app_context():
    db.create_all()