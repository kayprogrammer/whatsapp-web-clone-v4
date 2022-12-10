from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
csrf = CSRFProtect()
bcrypt = Bcrypt()
db = SQLAlchemy()
mail = Mail()