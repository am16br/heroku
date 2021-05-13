from flask import render_template,url_for,request,redirect
from flask_login import current_user,login_user,logout_user,login_required
from werkzeug.security import generate_password_hash,check_password_hash
from app.login_check import login
from app.login_check.forms import Loginform,Signupform
from app import db,User

@login.route('/login', methods=['POST'])
def login_process():
    if current_user.is_authenticated:
        return redirect(url_for('findjobs'))
    form = Loginform()
    if form.validate_on_submit() and request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            remember_me =request.form['remember_me']
        except:
            remember_me = False
        user = User.query.filter_by(email=email).first()
        if user is not None and check_password_hash(user.password,password):
            login_user(user,remember=remember_me)
            return redirect(url_for('display.show_post'))
        else:
            return redirect(url_for('login'))




@login.route('/signup', methods=['POST'])
def signup_process():
    if current_user.is_authenticated:
        return redirect(url_for('findjobs'))
    form = Signupform()
    if form.validate_on_submit() and request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        user = User(name=name,email=email,password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        login_user(user,remember=True)
        return redirect(url_for('display.show_post'))

    return redirect(url_for('signup'))



@login.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('display.show_post'))