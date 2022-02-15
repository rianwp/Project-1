from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
import pytz

class Transaksi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_barang = db.Column(db.Integer)
    nama_transaksi = db.Column(db.String(10000))
    harga_transaksi = db.Column(db.Integer)
    jumlah = db.Column(db.Integer)
    date_transaksi = db.Column(db.DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Bangkok')))
    user_id_transaksi = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Databarang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(10000))
    harga = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Bangkok')))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    fullname = db.Column(db.String(150))
    password_length = db.Column(db.Integer)
    img = db.Column(db.LargeBinary)
    imgname = db.Column(db.Text)
    mimetype = db.Column(db.Text)
    datauser = db.relationship('Databarang')
    transaksiuser= db.relationship('Transaksi')

class Indexintegrity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_integrity = db.Column(db.Integer)

