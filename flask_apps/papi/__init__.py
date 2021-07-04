from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import schedule

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///papi.db'
db = SQLAlchemy(app)

from papi import urls