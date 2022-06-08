from papi import db
from datetime import datetime
 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    second_name = db.Column(db.String(20), nullable=False)
    user_name = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(20), unique=True)
    user_img = db.Column(db.String(20), default='user.jpg')
    password = db.Column(db.String(60), nullable=False)
    tasks = db.relationship('Task', backref='author', lazy=True)

    def __repr__(self) -> str:
        return f'User({self.user_name}, {self.email}, {self.user_img})'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(20), nullable=False)
    complete = db.Column(db.Boolean, nullable=False, default=False)
    data_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return f'Task({self.task_name}, {self.data_created}, {self.complete})'

class News(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20), nullable=False)
    subtitle = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    discription = db.Column(db.String(20), nullable=False)
    source = db.Column(db.String(20), nullable=False)
    link = db.Column(db.String(20), nullable=False)
    story_img = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return f'News({self.title}, {self.category})'
