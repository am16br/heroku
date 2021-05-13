import os
import json
import cloudinary
from cloudinary.uploader import upload
from  cloudinary.utils import  cloudinary_url
from app import app,Upload,db
from flask import request,abort,redirect,url_for,current_app,render_template,session
from flask_login import current_user,login_required
from app.upload import upload
from app.upload.forms import Uploadfeed
from app.models import Likes,User,Upload
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
load_dotenv()

cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET')
)


@upload.route('/', methods = ['POST'])
@login_required
def upload_process():
        form = Uploadfeed()
        if form.validate_on_submit():
            name = request.form['name']
            about = request.form['about']
            pic = request.files['pic']
            filename = secure_filename(pic.filename)
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                    abort(400)
                '''pic.save(os.path.join(current_app.config['UPLOAD_FOLDER'],filename))
            address = '/static/images/{}'.format(filename)
            #saving in db part'''
            jsondata = cloudinary.uploader.upload(pic,public_id='petbook/{}/{}'.format(current_user.id,filename))
            keys_to_extract = ["url", "public_id"]
            subset = {key: jsondata[key] for key in keys_to_extract}
            user = Upload(name=name,about=about,pic=json.dumps(subset),author=current_user)
            db.session.add(user)
            db.session.commit()
        return redirect(url_for('display.show_post'))


@upload.route('/edit/<id>')
@login_required
def edit_post(id):
        post = Upload.query.filter_by(id=id).first()
        if post is not None and post.author.id == current_user.id:
            return render_template('editpost.html',post=post,json=json)
        abort(400)

@upload.route('/editprocess', methods = ['POST'])
@login_required
def edit_process():
    if request.method == 'POST':
            name = request.form['name']
            about = request.form['about']
            id = request.form['id']

             #saving in db part
            post = Upload.query.filter_by(id=id).first()
            if post is not None:
                post.name = name
                post.about = about
                db.session.commit()
                return redirect(url_for('display.show_post'))
            abort(400)



@upload.route('/delete/<id>')
@login_required
def delete_post(id):
        post = Upload.query.filter_by(id=id).first()
        if post is not None and post.author.id == current_user.id:
            session['deletepost'] = post.id
            return render_template('deletepost.html',post=post,json=json)

        abort(400)


@upload.route('/deleteprocess')
@login_required
def delete_process():
    yolo = session['deletepost']
    query = Upload.query.filter_by(id=yolo).first()
    likes = Likes.query.filter_by(post_id=yolo).all()
    #likequery
    if query is not None:
        cloudinary.uploader.destroy(json.loads(query.pic)['public_id'])
        for comment in query.comments:
            db.session.delete(comment)
        for like in likes:
            db.session.delete(like)
        db.session.delete(query)
        db.session.commit()
        session.pop('deletepost',None)
        return redirect(url_for('profile.profile_view',author=query.author.id))
    abort(400)

