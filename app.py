from flask import Flask #import
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand # to createa the db
from flask_script import Manager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'images'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/socialdb' #path for db connection
app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://ntkluxshtjlytg:105e6ce0ab73453e43b9f407ec3abbc46cbe2541ff92e535219126a0a4acf282@ec2-34-193-44-192.compute-1.amazonaws.com:5432/d9veiiu3u5tmuk"
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'ksdlfkdsofidsithnaljnfadksjhfdskjfbnjewrhewuirhfsenfdsjkfhdksjhfdslfjasldkj'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

configure_uploads(app, photos)

#instatiate sqlal and migrate passing the app
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.template_filter('time_since')
def time_since(delta):

    seconds = delta.total_seconds()

    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    if days > 0:
        return '%dd' % (days)
    elif hours > 0:
        return '%dh' % (hours)
    elif minutes > 0:
        return '%dm' % (minutes)
    else:
        return 'Just now'

from views import *

#instantiate the script
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()