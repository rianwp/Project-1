from re import X
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, Response
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .models import Indexintegrity, Transaksi, User, Databarang
from . import db
import json
from datetime import datetime
import pytz
views = Blueprint('views', __name__)

ALLOWED_EXTENSION = set(['png','jpg', 'jpeg'])
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@views.route('/')
@login_required
def default():
    return redirect(url_for('views.dashboard'))

@views.route('/dashboard')
@login_required
def dashboard():
    yearnow = datetime.now(pytz.timezone('Asia/Bangkok')).strftime("%Y")
    hargabanding = []
    jumlahbanding = []
    idlist = []
    totalpemasukan = 0
    totaljumlah = 0
    max_harga = 0
    max_jumlah = 0
    jmlm = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    nama_max_harga = "None"
    nama_max_jumlah = "None"
    data = current_user.transaksiuser
    if len(data) > 0:
        for row in data:
            totalpemasukan = totalpemasukan + row.harga_transaksi
            totaljumlah = totaljumlah + row.jumlah
            if row.id_barang not in idlist:
                idlist.append(row.id_barang)
        for x in idlist:
            grabdata = Transaksi.query.filter_by(id_barang=x).all()
            harga = 0
            jumlah = 0
            for y in grabdata:
                harga = harga + y.harga_transaksi
                jumlah = jumlah + y.jumlah
                date = y.date_transaksi.strftime("%m")
                year = y.date_transaksi.strftime("%Y")
                if date == "01" and year == yearnow:
                    jmlm[0] = jumlah
                elif date == "02" and year == yearnow:
                    jmlm[1] = jumlah
                elif date == "03" and year == yearnow:
                    jmlm[2] = jumlah
                elif date == "04" and year == yearnow:
                    jmlm[3] = jumlah
                elif date == "05" and year == yearnow:
                    jmlm[4] = jumlah
                elif date == "06" and year == yearnow:
                    jmlm[5] = jumlah
                elif date == "07" and year == yearnow:
                    jmlm[6] = jumlah
                elif date == "08" and year == yearnow:
                    jmlm[7] = jumlah
                elif date == "09" and year == yearnow:
                    jmlm[8] = jumlah
                elif date == "10" and year == yearnow:
                    jmlm[9] = jumlah
                elif date == "11" and year == yearnow:
                    jmlm[10] = jumlah
                elif date == "12" and year == yearnow:
                    jmlm[11] = jumlah
            hargabanding.append(harga)
            jumlahbanding.append(jumlah)
        max_harga = max(hargabanding)
        max_harga_index = hargabanding.index(max_harga)
        max_jumlah = max(jumlahbanding)
        max_jumlah_index = jumlahbanding.index(max_jumlah)
        nama_max_jumlah = Transaksi.query.filter_by(id_barang=idlist[max_jumlah_index]).first().nama_transaksi
        nama_max_harga = Transaksi.query.filter_by(id_barang=idlist[max_harga_index]).first().nama_transaksi
    return render_template("dashboard.html", user=current_user, withnav=True, max_harga=max_harga, max_jumlah=max_jumlah, nama_max_harga=nama_max_harga, nama_max_jumlah=nama_max_jumlah, totalpemasukan=totalpemasukan, totaljumlah=totaljumlah, jmlm=jmlm, yearnow=yearnow)

@views.route('/barang', methods=['GET', 'POST'])
@login_required
def barang():
    indexin = Indexintegrity.query.all()
    if len(indexin)<1:
        new_indexintegrity = Indexintegrity(id_integrity=1)
        db.session.add(new_indexintegrity)
        db.session.commit()
    idintegrity = Indexintegrity.query.get(1).id_integrity
    if request.method == 'POST':
        nama = request.form.get('nama')
        harga = request.form.get('harga')
        stock = request.form.get('stock')
        if len(nama) < 1:
            flash('Nama barang tidak boleh kosong', category='error')
            return redirect(url_for('views.barang'))
        elif len(str(stock)) < 1:
            flash('Stock tidak boleh kosong', category='error')
            return redirect(url_for('views.barang'))
        elif len(str(harga)) < 1:
            flash('Harga tidak boleh kosong', category='error')
            return redirect(url_for('views.barang'))
        else:
            new_databarang = Databarang(id=idintegrity, nama=nama, harga=harga, stock=stock, user_id=current_user.id)
            db.session.add(new_databarang)
            db.session.commit()
            
            updateid = Indexintegrity.query.get(1)
            updateid.id_integrity = idintegrity + 1
            db.session.commit()
            
            flash('Data berhasil diinput', category='success')
            return redirect(url_for('views.barang'))

    return render_template("barang.html", user=current_user, withnav=True)
    
@views.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        databarang = Databarang.query.get(request.form.get('id'))
        databarang.nama = request.form['nama']
        databarang.harga = request.form['harga']
        databarang.stock = request.form['stock']
        db.session.commit()
        flash('Data berhasil diedit', category='success')
        return redirect(url_for('views.barang'))
    
@views.route('/delete', methods=['POST'])
@login_required
def delete():
    databarang = json.loads(request.data)
    databarangId = databarang['databarangId']
    databarang = Databarang.query.get(databarangId)
    if databarang:
        if databarang.user_id == current_user.id:
            db.session.delete(databarang)
            db.session.commit()
    flash('Data berhasil dihapus', category='success')
    return jsonify({})

@views.route('/transaksi')
@login_required
def transaksi():
    return render_template("transaksi.html", user=current_user, withnav=True)

@views.route('/updatetransaksi', methods=['POST'])
@login_required
def updatetransaksi():
    datatransaksi = json.loads(request.data)
    jumlahdatatransaksi = len(datatransaksi)
    for x in range (jumlahdatatransaksi):
        id_barang = datatransaksi[x]['id']
        jumlah = datatransaksi[x]['jumlah']
        databarang = Databarang.query.get(id_barang)
        nama_transaksi = databarang.nama
        harga_transaksi = databarang.harga*jumlah
        
        new_transaksi = Transaksi(id_barang=id_barang, nama_transaksi=nama_transaksi, harga_transaksi=harga_transaksi, jumlah=jumlah, user_id_transaksi=current_user.id)
        db.session.add(new_transaksi)
        db.session.commit()
        
        stocknew = databarang.stock - jumlah
        databarang.stock = stocknew
        db.session.commit()
        flash('Transaksi Berhasil', category='success')
        
    return jsonify({})

@views.route('/riwayat')
@login_required
def riwayat():
    return render_template("riwayat.html", user=current_user, withnav=True)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    passwordlen = current_user.password_length * ("*")
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file:
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    mimetype = file.mimetype
                    current_user.img = file.read()
                    current_user.mimetype = mimetype
                    current_user.imgname = filename
                    
                    db.session.commit()
                    
                    flash('Foto berhasil diperbarui', category='success')
                    return redirect(url_for('views.profile'))
                else:
                    flash('File harus dalam format jpg, jpeg, atau png', category='error')
                    return redirect(url_for('views.profile'))
                    
        if 'passwordconfirm' in request.form:
            confirmation = request.form['passwordconfirm']
            fullname = request.form['fullname']
            username = request.form['username']
            newpass = request.form['password']
            if check_password_hash(current_user.password, confirmation):
                if fullname:
                    current_user.fullname = fullname   
                if username:
                    current_user.username = username
                if newpass:
                    current_user.password = generate_password_hash(newpass, method='sha256')
                    current_user.password_length = len(newpass)
                    
                db.session.commit()
                
                flash('Data berhasil diperbarui', category='success')
                return redirect(url_for('views.profile'))
        
            else:
                flash('Password anda salah', category='error')
                return redirect(url_for('views.profile'))
        
        
    return render_template("profile.html", user=current_user, withnav=True, passwordlen=passwordlen)

@views.route('/img')
@login_required
def img():
    return Response(current_user.img, mimetype=current_user.mimetype)

@views.errorhandler(413)
def request_entity_too_large(error):
    flash('Ukuran File Maksimal 1 MB', category='error')
    return redirect(url_for('views.profile'))