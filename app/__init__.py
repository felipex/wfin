from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_script import Manager
#from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/wfin'

db = SQLAlchemy(app)

#migrate = Migrate(app, db)

#manager = Manager(app)
#manager.add_command('db', MigrateCommand)

from app.controler import index