from app import app
from flask_sqlalchemy import SQLAlchemy

app.config.from_object('config')

if __name__ == "__main__":
    app.run()
