from flask_login import UserMixin
from app import db,log_in
from datetime import datetime
class User(UserMixin,db.Model):
    __tablename__ = "Userinfo"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40),unique=True,nullable=False)
    password = db.Column(db.String(200), nullable=False)
    liked_post = db.relationship('Likes', backref='liked_by', lazy='dynamic')
    posts = db.relationship('Upload',backref='author',lazy='dynamic')
    comment = db.relationship('Comments',backref='poster',lazy='dynamic')
    def __init__(self,name,email,password):
        self.name = name
        self.email = email
        self.password = password




class Upload(UserMixin,db.Model):
    __tablename__ = "uploadata"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40),nullable=False)
    about = db.Column(db.String(500),nullable=False)
    pic = db.Column(db.String(200),nullable=False)
    time = db.Column(db.DateTime,default=datetime.utcnow())
    likes = db.Column(db.Integer,default=0)
    liked_by = db.relationship('Likes',backref='likedpost',lazy='dynamic')
    user_id = db.Column(db.Integer,db.ForeignKey('Userinfo.id'))
    comments = db.relationship('Comments',backref='post',lazy='dynamic')


class Comments(UserMixin,db.Model):
    __tablename__ = 'commentdata'
    id = db.Column(db.Integer,primary_key=True)
    comment = db.Column(db.String(400),nullable=False)
    time = db.Column(db.DateTime,default=datetime.utcnow())
    userid = db.Column(db.Integer,db.ForeignKey('Userinfo.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('uploadata.id'))

class Likes(UserMixin,db.Model):
    __tablename__ = 'likedata'
    id = db.Column(db.Integer,primary_key=True)
    userid = db.Column(db.Integer,db.ForeignKey('Userinfo.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('uploadata.id'))


@log_in.user_loader
def load_user(id):
    return User.query.get(int(id))