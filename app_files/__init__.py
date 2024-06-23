import os
import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

internal_var = "postgresql://users_db_n95m_user:k1utNV6zjMigFYGYoIWlifWinDZ66G3K@dpg-cprcsljv2p9s73a4kl8g-a/users_db_n95m"
external_var = "postgresql://users_db_n95m_user:k1utNV6zjMigFYGYoIWlifWinDZ66G3K@dpg-cprcsljv2p9s73a4kl8g-a.oregon-postgres.render.com/users_db_n95m"
app = flask.Flask(__name__)

os.environ["DATABASE_URL"] = external_var
app.config['SECRET_KEY'] = "super_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
# postgresql://users_db_n95m_user:k1utNV6zjMigFYGYoIWlifWinDZ66G3K@dpg-cprcsljv2p9s73a4kl8g-a.oregon-postgres.render.com/users_db_n95m
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from app_files import routes