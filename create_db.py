from app.models import *
from app import db
types = [
    'Місце проживання',
    'Місце реєстрації',
    'Абонентський номер',
    'Електронна поштова скринька',
    'Сторінка у соціальній мережі',
    'Квартира',
    'Будинок',
    'Земельна ділянка',
]
for type in types:
    t = Type(type=type)
    db.session.add(t)
    db.session.commit()
cats = [
    'Департамент стратегічних розслідувань',
    'Департамент карного розшуку',
    'Департамент боротьби зі злочинами, пов’язаними з торгівлею людьми ',
    'Департамент протидії наркозлочинності',
    'Департамент оперативної служби',
    'Департамент оперативно-технічних заходів',
    'Управління кримінального аналізу'
]
for type in cats:
    t = Category(category=type)
    db.session.add(t)
    db.session.commit()

types = [
    'Особа',
    'Об\'єкт',
    'Юридична особа',
    'Група осіб',
    'Місце',
    'Подія',
    'Фото особи',
    'Фоторобот'
]
for type in types:
    t = Type(type=type)
    db.session.add(t)
    db.session.commit()