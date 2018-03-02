from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_script import Manager
#from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:wfin2018@localhost/wfindb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bjhyjijetsjlmt:e9ba8aaffcc1114d9cd4e216b5565813cdd563106d23117299fe7ae501dc541d@ec2-54-204-46-60.compute-1.amazonaws.com:5432/d5t43ksk47kb29'


db = SQLAlchemy(app)

#migrate = Migrate(app, db)

#manager = Manager(app)
#manager.add_command('db', MigrateCommand)

from app.controler import index
