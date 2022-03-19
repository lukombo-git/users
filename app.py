from flask import Flask
from flask.sessions import SecureCookieSessionInterface
from routes import user_blueprint
from flask_migrate import Migrate
from flask_login import LoginManager
import models

app = Flask(__name__)
app.config['SECRET_KEY'] = 'w0Jy2lnh6axA3cjZjazlbA'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///./database/user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
models.init_app(app)

app.register_blueprint(user_blueprint)
login_manager = LoginManager(app)
migrate = Migrate(app, models.db)

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = models.User.query.filter_by(api_key=api_key).first()
        if user:
            return user
    return None

class CustomSessionInterface(SecureCookieSessionInterface):
    def save_session(self, *args, **kwargs):
        if self.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
    