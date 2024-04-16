from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    contact_number = db.Column(db.String(80), unique=True, nullable=True, default='+7(XXX)XXX-XX-XX')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    address = db.relationship('Address', backref='Buyer', lazy=True)
    order = db.relationship('Order', backref='Buyer', lazy=True)
    product = db.relationship('Product', backref='Buyer', lazy=True)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80), nullable=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'), nullable=False)


class Typesweets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    sweets = db.relationship('Sweets', backref='Typesweets', lazy=True)


class Sweets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    typesweets_id = db.Column(db.Integer, db.ForeignKey('typesweets.id'), nullable=False)
    product = db.relationship('Product', backref='Sweets', lazy=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    contact_number = db.Column(db.String(80))
    status = db.Column(db.String(80), default='Принят в работу', nullable=False)
    date_add = db.Column(db.DateTime, default=datetime.utcnow)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweets.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.id'), nullable=False)
    count = db.Column(db.Integer)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(80), default='Не подтверждён', nullable=False)
