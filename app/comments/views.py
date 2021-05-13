from flask import redirect,url_for,session,render_template,request
from flask_login import current_user,login_required
from app import db
from app.comments import comments
from app.models import Upload,Comments,User



@comments.route('/',methods=['POST','GET'])
@login_required
def comment_process():
    if request.method == 'POST':
        comment = request.form['comment']
        user = current_user.id
        post_id = request.form['postid']
        post = Upload.query.get(int(post_id))
        brr = Comments(comment=comment,userid=user,post=post)
        db.session.add(brr)
        db.session.commit()
        return redirect(request.referrer)




@comments.route('/delete/<id>')
@login_required
def delete_process(id):
        final = Comments.query.filter_by(id=id).first()
        if final.poster.id == current_user.id:
            db.session.delete(final)
            db.session.commit()
            return redirect(request.referrer)
        else:
            return redirect(request.referrer)