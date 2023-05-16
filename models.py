from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    alternatives = db.relationship('Alternative', backref='thought', lazy=True)

class Alternative(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    selected = db.Column(db.Boolean, default=False)
    thought_id = db.Column(db.Integer, db.ForeignKey('thought.id'), nullable=False)
