# -*- coding: utf-8 -*-
import os
import random
import string
import hashlib

from flask import render_template, flash, redirect, url_for, request, abort, send_from_directory
from werkzeug.urls import url_parse
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename
from app import app
from flask_login import login_user, logout_user
from app.models import *
from app.forms import *
from flask_login import login_required, current_user
from app import db, nominatim
import json


# @app.errorhandler(Exception)
# def handle_error(e):
#     description = 'Я чайник'
#     code = 418
#     if isinstance(e, HTTPException):
#         code = e.code
#         description = e.description
#     return render_template('404.html', code=code, description=description), code


def gen_file_name(filename):
    char_set = string.ascii_uppercase + string.digits
    path = str(''.join(random.sample(char_set * 2, 2))) + '/' + str(''.join(random.sample(char_set * 2, 2)))
    if not os.path.exists(app.config['UPLOAD_FOLDER'] + path):
        os.makedirs(app.config['UPLOAD_FOLDER'] + path)
    img_path = os.path.join(path, filename + ".jpg")
    return img_path


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/uploads/<first>/<second>/<img>')
def uploaded_file(first, second, img):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'] + first + "/" + second), img)


@app.route('/my/', methods=["POST", "GET"])
@login_required
def my():
    user = current_user
    records = db.session.query(Record).filter(Record.user_id == user.id).all()
    if user.first_name and user.middle_name and user.last_name and user.position and user.unit_id:
        return render_template("user_profile.html", title=f'Профіль', user=user, records=records)
    else:
        return redirect(url_for('edit_user', user_id=current_user.id))


@app.route('/')
@app.route('/index/')
@login_required
def index():
    if current_user.is_authenticated:
        return redirect(url_for('my'))
    else:
        return redirect(url_for('login'))


@app.route('/location', methods=['POST'])
@login_required
def location():
    region = request.form["addressStr"]
    request_location = nominatim.geocode(region, timeout=10)
    return json.dumps(
        {
            'status': 'OK',
            'location': request_location.address,
            'latitude': request_location.latitude,
            'longitude': request_location.longitude
        }
    )


@app.route('/record<number>/', methods=["POST", "GET"])
@login_required
def record(number):
    opened_record = Record.query.filter(Record.id == number).first()
    if opened_record:
        if int(opened_record.user_id) == int(current_user.get_id()) or opened_record.permission == False:
            person = opened_record.persons[0]
            return render_template("person.html",
                                   title=f'Досьє на особу {person.last_name}',
                                   person=person,
                                   number=number,
                                   record=opened_record
                                   )
        else:
            abort(403, description='Вибачте, але це приватний запис')
    else:
        abort(404, description='Вибачте, але сторінка за запитом не знайдена')


@app.route('/record<number>/edit/person', methods=["POST", "GET"])
@login_required
def person_edit(number):
    edited_record = db.session.query(Record).filter(Record.id == number).first()
    if record:
        person = edited_record.persons[0]
        form = PersonForm()
        if form.is_submitted():
            if form.last_name.data:
                person.last_name = form.last_name.data
            if form.middle_name.data:
                person.middle_name = form.middle_name.data
            if form.first_name.data:
                person.first_name = form.first_name.data
            if form.date.data:
                person.date_birthday = form.date.data
            if form.place_latitude.data:
                person.place_birthday_latitude = form.place_latitude.data
            if form.place_longitude.data:
                person.place_birthday_longitude = form.place_longitude.data,
            if form.place_address.data:
                person.place_birthday_address = form.place_address.data,
            if form.code.data:
                person.code = form.code.data,
            db.session.commit()
            return redirect(url_for('record', number=number))
        return render_template("edit_person.html",
                               title=f'Досьє на особу {person.last_name}',
                               person=person,
                               form=form,
                               number=number
                               )
    else:
        abort(404, description='Вибачте, але сторінка за запитом не знайдена')


@app.route('/record<number>/edit/image/', methods=["POST", "GET"])
@login_required
def edit_image(number):
    edited_record = db.session.query(Record).filter(Record.id == number).first()
    person = edited_record.persons[0]
    return render_template("edit_image.html", title=f'Досьє на особу {person.last_name}')


@app.route('/record<number>/edit/', methods=["POST", "GET"])
@login_required
def record_edit(number):
    edited_record = db.session.query(Record).filter(Record.id == number).first()
    if record:
        form = RecordForm()
        if form.is_submitted():
            if form.record_type.data:
                edited_record.type_id = Type.query.filter(Type.type == form.record_type.data).first().id
                edited_record.type_id = Type.query.filter(Type.type == form.record_type.data).first().id
            if form.permission.data:
                edited_record.permission = True if form.permission.data == 'private' else False
            if form.category.data:
                edited_record.category_id = Category.query.filter(Category.category == form.category.data).first().id
            db.session.commit()
            return redirect(url_for('record', number=number))
        return render_template("edit_record.html",
                               form=form,
                               number=edited_record.id
                               )
    else:
        abort(404, description='Вибачте, але сторінка за запитом не знайдена')


@app.route('/record<number>/edit/contact<int:contact_id>/', methods=["POST", "GET"])
@login_required
def edit_contact(number, contact_id):
    contact = db.session.query(Contact).filter(Contact.id == contact_id).first()
    edited_record = db.session.query(Record).filter(Record.id == number).first()
    person = edited_record.persons[0]
    form = ContactForm()
    if form.is_submitted():
        if form.type.data:
            contact.type_id = db.session.query(Type).filter(Type.type == form.type.data).first().id
        if form.contact.data:
            contact.contact = form.contact.data
        db.session.commit()
        return redirect(url_for('record', number=number))
    if contact in person.contacts:
        return render_template("edit_contact.html", title=f'Досьє на особу', form=form, number=number, contact=contact)
    else:
        abort(404, description='Вибачте, але сторінка за запитом не знайдена')


@app.route('/record<number>/edit/place<int:place_id>/', methods=["POST", "GET"])
@login_required
def record_place(number, place_id):
    place = db.session.query(Place).filter(Place.id == place_id).first()
    edited_record = db.session.query(Record).filter(Record.id == number).first()
    person = edited_record.persons[0]
    form = PlaceForm()
    if form.is_submitted():
        if form.type.data:
            place.type_id = db.session.query(Type).filter(Type.type == form.type.data).first().id
        if form.address.data:
            place.address = form.address.data
        if form.latitude.data:
            place.latitude = form.latitude.data
        if form.longitude.data:
            place.longitude = form.longitude.data
        db.session.commit()
        return redirect(url_for('record', number=number))
    if place in person.places:
        return render_template("edit_place.html", title=f'Досьє на особу', form=form, place=place, number=number)
    else:
        abort(404, description='Вибачте, але сторінка за запитом не знайдена')


@app.route('/edit/user<int:user_id>/', methods=["POST", "GET"])
@login_required
def edit_user(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    form = UserInfo()
    if form.is_submitted():
        if form.last_name.data:
            user.last_name = form.last_name.data
        if form.middle_name.data:
            user.middle_name = form.middle_name.data
        if form.first_name.data:
            user.first_name = form.first_name.data
        if form.position.data:
            user.position = form.position.data
        if form.unit.data:
            user.unit_id = Category.query.filter(Category.category == form.unit.data).first().id
        db.session.commit()
        return redirect(url_for('my'))
    return render_template('edit_user_info.html', form=form, user=user)


@app.route('/user<int:user_id>/add_image/', methods=["POST", "GET"])
@login_required
def user_add_image(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    form = UserImageForm()
    if form.is_submitted():
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = hashlib.md5(secure_filename(file.filename).encode()).hexdigest()
            img_path = gen_file_name(filename)
            file.save(app.config['UPLOAD_FOLDER'] + img_path)
            image = Image(image_url=img_path)
            user.images.append(image)
            db.session.commit()
        return redirect(url_for('my'))
    return render_template("user_add_image.html", form=form, user=user)


@app.route('/remove/record<number>/', methods=["POST", "GET"])
@login_required
def remove_record(number):
    removed_record = db.session.query(Record).filter(Record.id == number).first()
    db.session.delete(removed_record)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/remove/user<int:user_id>/image<int:image_id>/', methods=["POST", "GET"])
@login_required
def remove_image(user_id, image_id):
    if current_user.id == user_id:
        removed_image = Image.query.filter(Image.id == image_id).first()
        db.session.delete(removed_image)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/record<number>/remove/place<int:place_id>/', methods=["POST", "GET"])
@login_required
def remove_place(number, place_id):
    place = db.session.query(Place).filter(Place.id == place_id).first()
    db.session.delete(place)
    db.session.commit()
    return redirect(url_for('record', number=number))


@app.route('/record<number>/remove/contact<int:contact_id>/', methods=["POST", "GET"])
@login_required
def remove_contact(number, contact_id):
    contact = db.session.query(Contact).filter(Contact.id == contact_id).first()
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('record', number=number))


@app.route('/record<int:number>/add/estate/', methods=["POST", "GET"])
@login_required
def add_estate(number):
    record_to_add_estate = db.session.query(Record).filter(Record.id == number).first()
    person = record_to_add_estate.persons[0]
    form = EstateForm()
    if form.is_submitted():
        source = Source(source=form.address_source.data)
        place = Place(
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            address=form.address.data
        )
        db.session.add(place)
        estate = Estate(
            type_id=db.session.query(Type).filter(Type.type == form.type.data).first().id,
            place_id=place.id,
            sources=[source]
        )
        person.estates.append(estate)
        db.session.commit()
        return redirect(url_for('record', number=number))
    return render_template("add_estate.html", title=f'Досьє на особу', form=form, number=number)


@app.route('/record<int:number>/edit/estate<int:estate_id>/', methods=["POST", "GET"])
@login_required
def edit_estate(number, estate_id):
    estate = Estate.query.filter(Estate.id == estate_id).first()
    form = EstateForm()
    if form.is_submitted():
        source = Source(source=form.address_source.data)
        place = Place.query.filter(Place.id == estate.id).first()
        place.latitude = form.latitude.data
        place.longitude = form.longitude.data
        place.address = form.address.data
        estate.type_id = db.session.query(Type).filter(Type.type == form.type.data).first().id
        estate.place_id = place.id
        estate.sources = [source]
        db.session.commit()
        return redirect(url_for('record', number=number))
    return render_template("edit_estate.html", title=f'Досьє на особу', form=form, number=number, estate=estate)


@app.route('/record<number>/add/place/', methods=["POST", "GET"])
@login_required
def add_place(number):
    record_to_add_place = db.session.query(Record).filter(Record.id == number).first()
    person = record_to_add_place.persons[0]
    form = PlaceForm()
    if form.is_submitted():
        place = Place(
            address=form.address.data,
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            type_id=db.session.query(Type).filter(Type.type == form.type.data).first().id
        )
        person.places.append(place)
        db.session.commit()
        return redirect(url_for('record', number=record_to_add_place.id))
    return render_template("add_place.html", title=f'Досьє на особу', form=form, number=number)


@app.route('/record<number>/add/contact/', methods=["POST", "GET"])
@login_required
def add_contact(number):
    record_to_add_contact = db.session.query(Record).filter(Record.id == number).first()
    person = record_to_add_contact.persons[0]
    form = ContactForm()
    if form.is_submitted():
        source = Source(source=form.contact_source.data)
        contact = Contact(
            contact=form.contact.data,
            type_id=db.session.query(Type).filter(Type.type == form.type.data).first().id,
            sources=[source]
        )
        person.contacts.append(contact)
        db.session.commit()
        return redirect(url_for('record', number=record_to_add_contact.id))
    return render_template("add_contact.html", title=f'Досьє на особу', form=form, number=number)


@app.route('/new_person<int:record_id>/', methods=["POST", "GET"])
@login_required
def new_person(record_id):
    form = PersonForm()
    if form.is_submitted():
        record_to_add_created_person = Record.query.filter(Record.id == record_id).first()
        created_person = Person(
            first_name=form.first_name.data,
            middle_name=form.middle_name.data,
            last_name=form.last_name.data,
            date_birthday=form.date.data,
            place_birthday_latitude=form.place_latitude.data,
            place_birthday_longitude=form.place_longitude.data,
            place_birthday_address=form.place_address.data,
            code=form.code.data,
        )
        record_to_add_created_person.persons.append(created_person)
        db.session.commit()
        return redirect(url_for('record', number=record_id))
    return render_template("new_person.html", title='Додати нове досьє на особу', form=form, record_id=record_id)


@app.route('/new_record/', methods=["POST", "GET"])
@login_required
def new_record():
    get_type = {
        'Особа': 'person',
        'Об\'єкт': 'item',
        'Юридична особа': 'ur_person',
        'Група осіб': 'group',
        'Місце': 'place',
        'Подія': 'event',
    }
    form = RecordForm()
    if form.is_submitted():
        created_record = Record(
            category=form.category.data,
            permission=form.permission.data,
            user_id=current_user.id,
            type=form.record_type.data
        )
        db.session.add(created_record)
        db.session.commit()
        url = 'new_' + get_type[form.record_type.data]
        return redirect(url_for(url, record_id=created_record.id))
    return render_template("new_record.html", title='Додати нове досьє', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('my'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = request.args.get('next') or url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/record<int:number>/add/image/', methods=["POST", "GET"])
@login_required
def record_add_image(number):
    record_to_add_estate = db.session.query(Record).filter(Record.id == number).first()
    person = record_to_add_estate.persons[0]
    form = UserImageForm()
    if form.is_submitted():
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = hashlib.md5(secure_filename(file.filename).encode()).hexdigest()
            img_path = gen_file_name(filename)
            file.save(app.config['UPLOAD_FOLDER'] + img_path)
            image = Image(image_url=img_path)
            person.images.append(image)
            db.session.commit()
        return redirect(url_for('record', number=number))
    return render_template("person_add_image.html", form=form, number=number)


@app.route('/record<int:number>/remove/image<int:image_id>/', methods=["POST", "GET"])
@login_required
def remove_record_image(number, image_id):
    removed_image = Image.query.filter(Image.id == image_id).first()
    db.session.delete(removed_image)
    db.session.commit()
    return redirect(url_for('record', number=number))


@app.route('/record<int:number>/add/other/', methods=["POST", "GET"])
@login_required
def add_other(number):
    record_to_add_other = db.session.query(Record).filter(Record.id == number).first()
    person = record_to_add_other.persons[0]
    form = OtherForm()
    if form.is_submitted():
        source = Source(source=form.other_source.data)
        db.session.add(source)
        other = Other(text=form.other.data, sources=[source])
        person.others.append(other)
        db.session.commit()
        return redirect(url_for('record', number=number))
    return render_template("add_other.html", title=f'Досьє на особу', form=form, number=number)


@app.route('/record<int:number>/add/connect/', methods=["POST", "GET"])
@login_required
def add_connects(number):
    form = ConnectForm()
    if form.is_submitted():
        source = Source(source=form.connect_source.data)
        db.session.add(source)
        connect = Connects(
            connect_type=form.connect_type.data,
            record_from=number,
            record_to=form.first_record.data,
        )
        db.session.add(connect)
        source.connects.append(connect)
        db.session.commit()
        return redirect(url_for('record', number=number))
    return render_template("add_connects.html", title=f'Досьє на особу', form=form, number=number)