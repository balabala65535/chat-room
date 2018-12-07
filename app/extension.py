from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_oauthlib.client import OAuth


login_manager = LoginManager()
bcrypt = Bcrypt()
socketio = SocketIO()
oauth = OAuth()
