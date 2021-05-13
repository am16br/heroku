import json
from app import app
from flask import render_template,request,url_for,redirect,session
from flask_login import login_required,current_user
from app.login_check.forms import Loginform,Signupform
from app.upload.forms import Uploadfeed
from app.models import Upload,User,Comments


@app.route('/login')
def login():
    form = Loginform()
    return render_template('login.html',form=form)




@app.route('/signup')
def signup():
    form = Signupform()
    return render_template('signup.html',form=form)


@app.route('/uploadata')
@login_required
def upload():
    form = Uploadfeed()
    return render_template('upload.html',form=form)


#extends
@app.route('/extended/<id>')
def postextends(id):
    post = Upload.query.get(int(id))
    return render_template('extended.html',post=post,json=json)



@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')