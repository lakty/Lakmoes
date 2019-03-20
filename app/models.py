from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)
    records = db.relationship('Record', backref='author', lazy='dynamic')
    users = db.relationship('User', backref='author', lazy='dynamic')


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    persons = db.relationship('Person', backref='author', lazy='dynamic')
    permission = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self, type, user_id, permission, category):
        self.category_id = Category.query.filter(Category.category == category).first().id,
        self.permission = True if permission == 'private' else False
        self.user_id = user_id
        self.type_id = Type.query.filter(Type.type == type).first().id

    def get_category(self):
        return Category.query.filter(Category.id == self.category_id).first().category


class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule = db.Column(db.String)
    description = db.Column(db.String)
    users = db.relationship('User', backref='owner', lazy='dynamic')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    records = db.relationship('Record', backref='owner')
    rule_id = db.Column(db.Integer, db.ForeignKey('rule.id'))
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    unit_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    position = db.Column(db.String(50))
    images = db.relationship('Image', backref='User', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_count_records(self):
        return len(self.records)

    def get_category(self):
        return Category.query.filter(Category.id == self.unit_id).first().category

    def get_image(self):
        if len(list(self.images)) > 0:
            return ['/uploads/' + image.image_url for image in self.images]
        else:
            return ['http://ssl.gstatic.com/accounts/ui/avatar_2x.png']


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    record_id = db.Column(db.Integer, db.ForeignKey('record.id'))
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    date_birthday = db.Column(db.DateTime(50))
    place_birthday_address = db.Column(db.String, nullable=True)
    place_birthday_latitude = db.Column(db.String, nullable=True)
    place_birthday_longitude = db.Column(db.String, nullable=True)
    code = db.Column(db.String, nullable=True)
    dates = db.relationship('Date', backref='author', lazy='dynamic')
    contacts = db.relationship('Contact', backref='Person', lazy='dynamic')
    places = db.relationship('Place', backref='Person', lazy='dynamic')
    sources = db.relationship('Source', backref='author', lazy='dynamic')
    estates = db.relationship('Estate', backref='author', lazy='dynamic')
    images = db.relationship('Image', backref='Person', lazy='dynamic')

    def get_image(self):
        if len(list(self.images)) > 0:
            return ['/uploads/' + image.image_url for image in self.images]
        else:
            return ['http://ssl.gstatic.com/accounts/ui/avatar_2x.png']


class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    sources = db.relationship('Source', backref='date', lazy='dynamic')
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(50))
    longitude = db.Column(db.String(50))
    address = db.Column(db.String(300))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    sources = db.relationship('Source', backref='place', lazy='dynamic')

    def get_type(self):
        return Type.query.filter(Type.id == self.type_id).first().type


class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    sources = db.relationship('Source', backref='code', lazy='dynamic')


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(50))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    sources = db.relationship('Source', backref='contact', lazy='dynamic')

    def get_type(self):
        return Type.query.filter(Type.id == self.type_id).first().type


class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(120))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    code_id = db.Column(db.Integer, db.ForeignKey('code.id'))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    date_id = db.Column(db.Integer, db.ForeignKey('date.id'))
    estate_id = db.Column(db.Integer, db.ForeignKey('estate.id'))


class Estate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sources = db.relationship('Source', backref='Estate')
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))

    def get_type(self):
        return Type.query.filter(Type.id == self.type_id).first().type

    def get_place(self):
        return Place.query.filter(Place.id == self.place_id).first()


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(200))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    dates = db.relationship('Date', backref='Image')
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def get_type(self):
        return Type.query.filter(Type.id == self.type_id).first().type
