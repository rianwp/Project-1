from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.default'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Sukses Login', category='success')
                return redirect(url_for('views.default'))
            else:
                flash('Password anda salah', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('Username anda salah!', category='error')
            return redirect(url_for('auth.login'))
        
    return render_template("login.html", user=current_user, withnav=False)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        fullname = request.form.get('fullname')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        null = "Kosong"
        if user:
            flash('Username sudah digunakan', category='error')
            return redirect(url_for('auth.admin'))
        else:
            new_user = User(username=username, fullname=fullname, password=generate_password_hash(password, method='sha256'), password_length=len(password), img=null, imgname=null, mimetype=null)
            db.session.add(new_user)
            db.session.commit()
            flash('Akun Sukses Dibuat', category='success')
            return redirect(url_for('auth.login'))
            
    return render_template("admin.html", user=current_user)     