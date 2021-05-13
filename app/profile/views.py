import json
from flask import redirect,url_for,session,render_template,request
from flask_login import current_user,login_required
from app.login_check.forms import Loginform,Signupform
from app import db
from app.profile import profile
from app.models import Upload,Comments,User,Likes
from werkzeug.security import check_password_hash



@profile.route('/')
@login_required
def display_profile():
    user = current_user
    if user is not None:
        return render_template('userprofile.html',user=user,json=json)

@profile.route('/edit')
@login_required
def edit_account():
    user = current_user
    form = Signupform()
    if user is not None:
        return render_template('editaccount.html',form=form)


@profile.route('/edit_process',methods=['POST'])
@login_required
def edit_account_process():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        current_user.email = email
        current_user.name = name
        db.session.commit()
        return redirect(url_for('profile.display_profile'))
    else:
        return redirect(url_for('profile.display_profile'))

@profile.route('/deleteaccount')
@login_required
def delete_account():

    user = current_user
    if user is not None:
      return render_template('confirm.html')




@profile.route('/confirmdelete',methods=['POST'])
@login_required
def delete():
    if  request.method == 'POST' and check_password_hash(current_user.password, request.form['password_confirm']):

        for post in current_user.posts:
            db.session.delete(post)
        for comment in current_user.comment:
            db.session.delete(comment)
        for like in Likes.query.filter_by(userid=current_user.id).all():
            db.session.delete(like)
        db.session.delete(current_user)
        db.session.commit()
        return redirect(url_for('display.show_post'))
    else:
        return redirect(url_for('profile.delete_account'))
        flash('wrong credentials')




@profile.route('/profile_view/<author>')
@login_required
def profile_view(author):
    user = User.query.filter_by(id=author).first()

    if user is not None and user.id != current_user.id:
        return render_template('userprofile.html',user=user,json=json)
    else:
        return redirect(url_for('profile.display_profile'))
