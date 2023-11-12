import os.path

from flask import render_template, redirect, url_for, flash, send_from_directory
from sqlalchemy.orm import backref
from Utils.register import RegisterForm
from Utils.login import LoginForm
from Utils.create_picture import CreatePictureForm
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import *
from werkzeug.utils import secure_filename
from Utils.pictures import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webSite.db'
app.config['SECRET_KEY'] = os.urandom(32)
db = SQLAlchemy(app)

app.config['UPLOAD_FOLDER'] = 'my_pictures'


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(40), nullable=False)
    lastname = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    pictures = db.relationship('Picture', backref='user', cascade='all, delete, delete-orphan')

    def is_active(self):
        return True

    def is_authenticated(self):
        return True if self.is_active() else False

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)


class Picture(db.Model):
    __tablename__ = 'picture'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url_picture = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    owner = db.relationship("User", backref=backref("pictures_list", uselist=False))


@app.route('/')
def home():
    return render_template('Basic.html')


@app.route('/uploads/<filename>')
def upload_img(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/Register_page', methods=['GET', 'POST'])
def Register_page():
    form = RegisterForm()
    db.create_all()
    if form.validate_on_submit():
        my_username = form.userName.data
        my_firstname = form.firstName.data
        my_lastname = form.lastName.data
        my_email = form.email_address.data
        my_password = form.password.data
        if form.password_valid.data != my_password:
            flash('Passwords do not match', 'danger')
            return render_template('Register.html', form=form)
        user = User.query.filter_by(email=my_email).first()
        if user:
            flash('This email already exists')
            return render_template('Register.html', form=form)
        user = User.query.filter_by(username=my_username).first()
        if user:
            flash('This username already exists')
            return render_template('Register.html', form=form)
        new_user = User(username=my_username,
                        firstname=my_firstname,
                        lastname=my_lastname,
                        email=my_email,
                        password=my_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('My_login'))
    return render_template("Register.html", form=form)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/My_login', methods=['GET', 'POST'])
def My_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.userName.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('Gallery_page'))
        else:
            print("Login unsuccessful")
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template("Login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/Gallery_page', methods=['GET'])
@login_required
def Gallery_page():
    print("in gallery")
    id_user = current_user.user_id
    pictures = Picture.query.filter(Picture.user_id == id_user).all()
    print("after filter")
    return render_template("Gallery.html", pictures=pictures)


@app.route('/Create_pictures', methods=['GET', 'POST'])
@login_required
def Create_pictures():
    form = CreatePictureForm()

    if form.validate_on_submit():
        file = form.file.data

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'static', secure_filename(file.filename))

        file.save(file_path)
        file_name = os.path.basename(file_path)
        start_path = r'C:\Python\PhotosWebSiteProject'
        rel_path = os.path.relpath(file_path, start_path)
        img = cv2.imread(rel_path)

        new_picture = Picture(url_picture=file_name, user_id=current_user.user_id)
        db.session.add(new_picture)
        db.session.commit()

        create_picture = form.options.data
        if create_picture == 'color':
            if img is not None:
                new_img = change_color_img(img, cv2.COLOR_BGR2GRAY, current_user.user_id, file.filename)
                pic_new = Picture(url_picture=new_img, user_id=current_user.user_id)
                db.session.add(pic_new)
                db.session.commit()
                return render_template('Create_pictures.html', img_url=file_name, new_img_url=new_img, form=form)
            else:
                print("Error" + file_path)
        elif create_picture == 'border':
            if img is not None:
                new_img = border_img(img, cv2.BORDER_CONSTANT, (98, 45, 255), current_user.user_id, file.filename)
                pic_new = Picture(url_picture=new_img, user_id=current_user.user_id)
                db.session.add(pic_new)
                db.session.commit()
                return render_template('Create_pictures.html', img_url=file_name, new_img_url=new_img, form=form)
        elif create_picture == 'identify':
            if img is not None:
                mask, result = identify_object(img, current_user.user_id, file.filename)
                pic_new = Picture(url_picture=result, user_id=current_user.user_id)
                db.session.add(pic_new)
                pic_new = Picture(url_picture=mask, user_id=current_user.user_id)
                db.session.add(pic_new)
                db.session.commit()
                return render_template('Create_pictures.html', img_url=file_name, new_img_url=result, mask_img=mask, form=form)
        else:
            return render_template('Create_pictures.html', form=form)
    return render_template('Create_pictures.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
