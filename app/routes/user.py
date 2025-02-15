from flask import Blueprint, render_template, redirect, request, flash, current_app,url_for
from ..extensions import db,bcrypt
from ..models.user import User
from ..forms import RegistrationForm, LoginForm
from ..functions import save_picture
from ..config import Config
from flask_login import login_user,logout_user
user = Blueprint('user', __name__)

@user.route('/user/register', methods= ['GET','POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        #current_app.config['SECRET_KEY']
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        filename = save_picture(form.avatar.data)

        user = User(name=form.name.data, login=form.login.data, avatar=filename, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Поздравляем, {form.login.data} вы успешно зарегестрированы!", "success")
            return redirect(url_for("user.login"))
        except Exception as e:
            print(str(e))
            flash(f"При регистрации произошла ошибка, ", "danger")
    return render_template("user/register.html", form=form)

@user.route('/user/login', methods= ['GET','POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Поздравляем, {form.login.data} вы успешно авторизованны!", "success")
            return redirect(next_page) if next_page else redirect(url_for('post.all'))
        else:
            flash("Неверные данные входа", "danger")
    return render_template("user/login.html", form=form)

@user.route('/user/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for("post.all"))