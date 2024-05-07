from db import db

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    song_data = db.Column(db.Text, nullable=False)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
