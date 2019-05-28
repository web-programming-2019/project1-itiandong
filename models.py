from app import db

from datetime import datetime



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    reviews = db.relationship('Review', backref=db.backref('user', uselist=False))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(10))
    title = db.Column(db.String(200))
    author = db.Column(db.String(50))
    year = db.Column(db.Integer)
    reviews = db.relationship('Review', backref=db.backref('book', uselist=False))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(20))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    body = db.Column(db.String(500))

