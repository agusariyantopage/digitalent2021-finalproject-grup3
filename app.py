from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_hewan(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM hewan WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

def get_jumlahhewan():
    conn = get_db_connection()
    post = conn.execute('SELECT COUNT(id) as jumlah_hewan FROM hewan').fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post['jumlah_hewan']

def get_jumlahsapi():
    conn = get_db_connection()
    post = conn.execute('SELECT COUNT(id) as jumlah FROM hewan where jenis="Sapi"').fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post['jumlah']

def get_jumlahkambing():
    conn = get_db_connection()
    post = conn.execute('SELECT COUNT(id) as jumlah FROM hewan where jenis="Kambing"').fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post['jumlah']

def get_jumlahhewankilo():
    conn = get_db_connection()
    post = conn.execute('SELECT SUM(berat) as jumlah_hewan FROM hewan').fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post['jumlah_hewan']

def get_jumlahsapikilo():
    conn = get_db_connection()
    post = conn.execute('SELECT SUM(berat) as jumlah FROM hewan where jenis="Sapi"').fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post['jumlah']

def get_jumlahkambingkilo():
    conn = get_db_connection()
    post = conn.execute('SELECT SUM(berat) as jumlah FROM hewan where jenis="Kambing"').fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post['jumlah']

def get_jumlahpenerima():
    conn = get_db_connection()
    post = conn.execute('SELECT COUNT(id) as jumlah FROM penerima').fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post['jumlah']

def get_jumlahlayak():
    conn = get_db_connection()
    post = conn.execute('SELECT COUNT(id) as jumlah FROM penerima where layak=1').fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post['jumlah']

def get_jumlahbelumlayak():
    conn = get_db_connection()
    post = conn.execute('SELECT COUNT(id) as jumlah FROM penerima where layak=0').fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post['jumlah']

def get_penerima(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM penerima WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
@app.context_processor
def inject_global_variables():
    return dict(jumlahHewan=get_jumlahhewan(),sapi=get_jumlahsapi(),kambing=get_jumlahkambing(),jumlahHewankilo=get_jumlahhewankilo(),sapikilo=get_jumlahsapikilo(),kambingkilo=get_jumlahkambingkilo(),sapirata=get_jumlahsapikilo()/get_jumlahlayak(),kambingrata=get_jumlahkambingkilo()/get_jumlahlayak(),dagingrata=get_jumlahhewankilo()/get_jumlahlayak(), jumlahPenerima=get_jumlahpenerima(), layak=get_jumlahlayak(), belumLayak=get_jumlahbelumlayak())

app.config['SECRET_KEY'] = 'KMZWA8AWAA'

@app.route('/')
def index():
    get_jumlahhewan()
    return render_template('index.html')

@app.route('/pembagian')
def pembagian():
    return render_template('pembagian.html')

@app.route('/hewan/<int:post_id>')
def hewan_single(post_id):
    post= get_hewan(post_id)
    return render_template('post.html', post=post)

@app.route('/bagirata', methods=('GET', 'POST'))
def bagirata():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM penerima where layak=1 order by bobot desc').fetchall()
    conn.close()
    return render_template('bagirata.html', posts=posts)

@app.route('/bagibaku', methods=('GET', 'POST'))
def bagibaku():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM penerima where layak=1 order by bobot desc').fetchall()
    conn.close()
    return render_template('bagibaku.html', posts=posts)

@app.route('/hewan', methods=('GET', 'POST'))
def hewan():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM hewan').fetchall()
    conn.close()
    return render_template('hewan.html', posts=posts)

@app.route('/penerima', methods=('GET', 'POST'))
def penerima():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM penerima').fetchall()
    conn.close()
    return render_template('penerima.html', posts=posts)

@app.route('/hewan_new', methods=('GET', 'POST'))
def hewan_new():
    if request.method == 'POST':
        jenis = request.form['jenis']
        keterangan = request.form['keterangan']
        berat = request.form['berat']

        if not jenis:
            flash('jenis is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO hewan (jenis, keterangan, berat) VALUES (?, ?, ?)',
                         (jenis, keterangan, berat))
            conn.commit()
            conn.close()
            return redirect(url_for('hewan'))

    return render_template('hewan_new.html')

@app.route('/penerima_new', methods=('GET', 'POST'))
def penerima_new():
    if request.method == 'POST':
        nama = request.form['nama']
        umur = request.form['umur']
        fakir = request.form['fakir']
        miskin = request.form['miskin']
        fisabilillah = request.form['fisabilillah']
        mualaf = request.form['mualaf']
        gharim = request.form['gharim']
        ibnusabil = request.form['ibnusabil']
        amil = request.form['amil']
        bobot=int(fakir)+int(miskin)+int(fisabilillah)+int(mualaf)+int(gharim)+int(ibnusabil)+int(amil)
        ##bobot=int(bobot)
        if bobot>= 1:
            layak=1
        else:
            layak=0       
        
        if not nama:
            flash('nama is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO penerima (nama, umur, fakir, miskin, fisabilillah, mualaf, gharim, ibnusabil, amil, bobot, layak) VALUES (?, ?,?, ?,?, ?,?, ?,?, ?,?)',
                         (nama, umur, fakir, miskin, fisabilillah, mualaf, gharim, ibnusabil, amil, bobot, layak))
            conn.commit()
            conn.close()
            return redirect(url_for('penerima'))

    return render_template('penerima_new.html')

@app.route('/<int:id>/hewan_edit', methods=('GET', 'POST'))
def hewan_edit(id):
    post = get_hewan(id)
    if request.method == 'POST':
        jenis = request.form['jenis']
        keterangan = request.form['keterangan']
        berat = request.form['berat']

        if not jenis:
            flash('jenis is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE hewan SET jenis = ?, keterangan = ?, berat=?'
                            ' WHERE id = ?',
                            (jenis, keterangan, berat, id))
            conn.commit()
            conn.close()
            return redirect(url_for('hewan'))

    return render_template('hewan_edit.html', post=post)

@app.route('/<int:id>/penerima_edit', methods=('GET', 'POST'))
def penerima_edit(id):
    post = get_penerima(id)
    if request.method == 'POST':
        nama = request.form['nama']
        umur = request.form['umur']
        fakir = request.form['fakir']
        miskin = request.form['miskin']
        fisabilillah = request.form['fisabilillah']
        mualaf = request.form['mualaf']
        gharim = request.form['gharim']
        ibnusabil = request.form['ibnusabil']
        amil = request.form['amil']
        bobot=int(fakir)+int(miskin)+int(fisabilillah)+int(mualaf)+int(gharim)+int(ibnusabil)+int(amil)
       
        if bobot>= 1:
            layak=1
        else:
            layak=0  

        if not nama:
                flash('nama is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE penerima SET nama=?, umur=?, fakir=?, miskin=?, fisabilillah=?, mualaf=?, gharim=?, ibnusabil=?, amil=?, bobot=?, layak=?'
                            ' WHERE id = ?',
                            (nama, umur, fakir, miskin, fisabilillah, mualaf, gharim, ibnusabil, amil, bobot, layak, id))
            conn.commit()
            conn.close()
            return redirect(url_for('penerima'))

    return render_template('penerima_edit.html', post=post)

@app.route('/<int:id>/hewan_delete', methods=('GET','POST'))
def hewan_delete(id):
    post = get_hewan(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM hewan WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['jenis']))
    return redirect(url_for('hewan'))   

@app.route('/<int:id>/penerima_delete', methods=('GET','POST'))
def penerima_delete(id):
    post = get_penerima(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM penerima WHERE id = ?', (id,))
    conn.commit()
    conn.close()    
    return redirect(url_for('penerima'))   



