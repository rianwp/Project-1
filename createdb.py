from website import create_app
from website import db

db.create_all(app=create_app())


