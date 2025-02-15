from flask import Blueprint,render_template,request, redirect,abort
from flask_login import login_required,current_user
from ..extensions import db
from sqlalchemy import desc
from ..models.post import Post
from ..models.user import User
from ..forms import PostForm, StudentForm, TeacherForm
post = Blueprint('post', __name__)

@post.route('/', methods = ['POST', 'GET'])
def all():
    form = TeacherForm()
    form.teacher.choices = [t.name for t in User.query.filter_by(status='teacher')]
    if form.validate_on_submit():
        teacher = form.teacher.data
        teacher_id = User.query.filter_by(name=teacher).first().id
        posts = Post.query.filter_by(teacher=teacher_id).order_by(Post.date.desc()).all()
    elif "orderby" in request.args:
        posts = Post.query.order_by(request.args["orderby"]).all() 
        #Post.query.order_by(Post.date.desc()).all()
    else:
        posts = Post.query.order_by(desc("date")).limit(20).all()
    return render_template('post/all.html', posts=posts, user=User, form=form)


@post.route('/post/create', methods = ['POST','GET'])
@login_required
def create():
    form = PostForm()
    studentForm = StudentForm()
    studentForm.student.choices = [s.name for s in User.query.filter_by(status='user')]
    if form.validate_on_submit():
        student_id = User.query.filter_by(name=studentForm.student.data).first().id
        post = Post(teacher=current_user.id,
                    subject=form.subject.data,
                    student=student_id)
        
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(str(e))

    return render_template('post/create.html',form=form, studentForm=studentForm)


@post.route('/post/<int:id>/update', methods = ['POST','GET'])
@login_required
def update(id):
    post = Post.query.get(id)
    if post.author.id == current_user.id:
        form = PostForm()
        studentForm = StudentForm()
        
        studentForm.student.choices = [s.name for s in User.query.filter_by(status='user')]
        if form.validate_on_submit():
            post.subject = form.subject.data
            post.likes = 0
            student_id = User.query.filter_by(name=studentForm.student.data).first().id
            post.student = student_id
            try:
                db.session.commit()
                return redirect('/')
            except Exception as e:
                print(str(e))
        else:
            student = User.query.filter_by(id=post.student).first()
            studentForm.student.data = student.name
            form.subject.data = post.subject
            return render_template('post/update.html', post=post, form=form,studentForm=studentForm)
    else:
        abort(403)


@post.route('/post/<int:id>/delete', methods = ['POST','GET'])
@login_required
def delete(id):

    post = Post.query.get(id)
    if post.author.id == current_user.id:
        if request.method == 'POST':
            try:
                db.session.delete(post)
                db.session.commit()
            except Exception as e:
                print(str(e))
                return str(e)
            return redirect('/')
        else:
            return render_template('post/delete.html', post=post)
    else:
        abort(403)
    

@post.route('/post/<int:id>/like', methods = ['GET'])
@login_required
def like(id):
    post = Post.query.get(id)
    if post.likes is None:
        post.likes = 0
    else:
        post.likes += 1
    try:
        db.session.commit()
    except Exception as e:
        print(str(e))
        return str(e)
    return redirect("/")


@post.route('/post/<int:id>/dislike', methods = ['GET'])
@login_required
def dislike(id):
    post = Post.query.get(id)
    if post.likes is None:
        post.likes = 0
    else:
        post.likes -= 1
    try:
        db.session.commit()
    except Exception as e:
        print(str(e))
        return str(e)
    return redirect("/")