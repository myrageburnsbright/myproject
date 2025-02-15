from ..extensions import db
from datetime import datetime
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"))
    student = db.Column(db.Integer)
    subject = db.Column(db.String(250))
    body = db.Column(db.String(500))
    date = db.Column(db.DateTime, default=datetime.now)
    likes = db.Column(db.Integer, default=0)