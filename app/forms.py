from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms.fields.html5 import DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, StopValidation
from app.models import User
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField
from app import models


class RequiredIf(object):

    def __init__(self, message=None, **kwargs):
        self.message = message

    def __call__(self, form, field):
        current_value = form.data.get(str(field.name)[:-7])
        source_value = form.data.get(field.name)
        message = self.message
        if current_value and not source_value:
            if message is None:
                message = field.gettext('Поле джерела інформації має бути заповнене')
            raise StopValidation(message)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Запам\'ятати мене')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class RecordForm(FlaskForm):
    permission = SelectField(
        'Доступ: ',
        choices=[
            ('private', 'Приватний'),
            ('public', 'Публічний'),
        ]
    )
    category = SelectField(
        'Лінія роботи: ',
        choices=[(cat.category, cat.category) for cat in models.Category.query.all()]
    )
    record_type = SelectField(
        'Тип нового досьє: ',
        choices=[
            ('Особа', 'Особа'),
            ('Об\'єкт', 'Об\'єкт'),
            ('Юридична особа', 'Юридична особа'),
            ('Група осіб', 'Група осіб'),
            ('Місце', 'Місце'),
            ('Подія', 'Подія'),
        ]
    )
    submit = SubmitField('Додати')


class PersonForm(FlaskForm):
    first_name = StringField('Ім\'я')
    first_name_source = StringField('Джерело імені', validators=[RequiredIf()])
    middle_name = StringField('По батькові')
    middle_name_source = StringField('Джерело імені по батькові', validators=[RequiredIf()])
    last_name = StringField('Прізвище')
    last_name_source = StringField('Джерело прізвища', validators=[RequiredIf()])
    date = DateField('Дата народження')
    date_source = StringField('Джерело дати народження', validators=[RequiredIf()])
    place_latitude = HiddenField(validators=[])
    place_longitude = HiddenField(validators=[])
    place_address = StringField('Місце народження')
    place_address_source = StringField('Джерело місця народження', validators=[RequiredIf()])
    code = StringField('РНОКПП')
    code_source = StringField('Джерело РНОКПП', validators=[RequiredIf()])
    submit = SubmitField('Додати')


class PlaceForm(FlaskForm):
    latitude = HiddenField(validators=[])
    longitude = HiddenField(validators=[])
    address = StringField('Адреса')
    type = SelectField(
        'Тип адреси: ',
        choices=[
            ('Місце проживання', 'Місце проживання'),
            ('Місце реєстрації', 'Місце реєстрації'),
            ('Місце роботи', 'Місце роботи'),
            ('Місце навчання', 'Місце навчання'),
        ]
    )
    address_source = StringField('Джерело місця народження', validators=[RequiredIf()])
    submit = SubmitField('Редагувати')


class ContactForm(FlaskForm):
    contact = StringField('Контактна Інформація', validators=[RequiredIf()])
    type = SelectField(
        'Тип адреси: ',
        choices=[
            ('Абонентський номер', 'Абонентський номер'),
            ('Електронна поштова скринька', 'Електронна поштова скринька'),
            ('Сторінка у соціальній мережі', 'Сторінка у соціальній мережі'),
        ]
    )
    contact_source = StringField('Джерело місця народження', validators=[RequiredIf()])
    submit = SubmitField('Редагувати')


class ConnectForm(FlaskForm):
    contact = StringField('Контактна Інформація', validators=[RequiredIf()])
    type = SelectField(
        'Тип адреси: ',
        choices=[
            ('Абонентський номер', 'Абонентський номер'),
            ('Електронна поштова скринька', 'Електронна поштова скринька'),
            ('Сторінка у соціальній мережі', 'Сторінка у соціальній мережі'),
        ]
    )
    contact_source = StringField('Джерело місця народження', validators=[RequiredIf()])
    submit = SubmitField('Редагувати')


class EstateForm(PlaceForm):
    type = SelectField(
        'Тип майна: ',
        choices=[
            ('Квартира', 'Квартира'),
            ('Будинок', 'Будинок'),
            ('Земельна ділянка', 'Земельна ділянка'),
        ]
    )


class UserInfo(FlaskForm):
    first_name = StringField('Ім\'я', validators=[DataRequired()])
    middle_name = StringField('По батькові', validators=[DataRequired()])
    last_name = StringField('Прізвище', validators=[DataRequired()])
    position = StringField('Посада', validators=[DataRequired()])
    unit = SelectField(
        'Підрозділ: ',
        choices=[(cat.category, cat.category) for cat in models.Category.query.all()]
    )
    submit = SubmitField('Додати')


class UserImageForm(FlaskForm):
    image = FileField('Зображення', validators=[FileRequired()])
    submit = SubmitField('Додати')


class RecordImageForm(UserImageForm):
    type = SelectField(
        'Тип фото',
        choices=[
            ('Фото особи', 'Фото особи'),
            ('Фоторобот', 'Фоторобот'),
        ]
    )
    image_date = DateField('Дата розміщення')


class OtherForm(FlaskForm):
    other = StringField('Додаткова інформація', validators=[RequiredIf()])
    other_source = StringField('Джерело додаткової інформації', validators=[RequiredIf()])
    submit = SubmitField('Додати')