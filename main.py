from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask_migrate import Migrate

import os
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@db:5432/main'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/main')
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=False)
	title = db.Column(db.String(255))
	image = db.Column(db.String(255))

class ProductUser(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer)
	product_id = db.Column(db.Integer)

	UniqueConstraint('user_id', 'product_id', name="user_product_unique")

@app.route('/')
def index():
	return 'Hello'


if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")