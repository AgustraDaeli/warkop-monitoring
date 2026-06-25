from flask import Flask, render_template, request, redirect, session
import mysql.connector
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, session, jsonify
import pandas as pd
from flask import send_file
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
app = Flask(__name__)
app.secret_key = 'secret123'

def db():
    return mysql.connector.connect(
        host="thomas.proxy.rlwy.net",
        user="root",
        password="frpIBiZLhGBHruhEBhzbhdsvkYSOJsJr",
        database="railway",
        port=38324
    )
# ================= INIT =================
def init_db():
    conn = db()
    c = conn.cursor()

    # ================= ISI DATA AWAL =================
    c.execute("SELECT COUNT(*) FROM bahan")
    if c.fetchone()[0] == 0:

        bahan_list = [
            ("mie", 100),
            ("telor", 50),
            ("keju", 40),
            ("kornet", 40),
            ("bakso", 40),
            ("pisang", 50),
            ("sosis", 40),
            ("kapal api", 30),
            ("liong", 30),
            ("kentang", 50),
            ("otak otak", 50),
            ("cireng", 50),
            ("nugget", 50),
            ("dimsum", 50),
            ("roti", 50),
            ("mix plate", 40),

            ("susu", 100),
            ("coklat", 100),
            ("jahe", 50),
            ("teh tarik", 50),
            ("beng beng", 50),
            ("milo", 50),
            ("ovaltine", 50),
            ("energen", 50),

            ("extrajoss", 50),
            ("kukubima", 50),

            ("chocolatos coklat", 50),
            ("chocolatos matcha", 50),

            ("kopi tubruk", 50),
            ("abc susu", 50),
            ("luwak white coffee", 50),
            ("indocafe milk", 50),
            ("good day", 50),

            ("jeruk nipis", 50),
            ("jeruk peras", 50),
            ("leci", 50),
            ("leci tea", 50),
            ("milky orange", 50),
            ("semangka", 50),
            ("sirsak", 50),
            ("strawberry", 50),
            ("sweet mango", 50),
            ("sweet orange", 50)
        ]

        for b in bahan_list:
            c.execute(
                "INSERT INTO bahan (nama, stok) VALUES (%s, %s)",
                b
            )

        def get_bahan(nama):
            c.execute(
                "SELECT id FROM bahan WHERE nama=%s",
                (nama,)
            )
            return c.fetchone()[0]

        produk_data = [
            ("Indomie", "INDOMIE"), ("Indomie Double", "INDOMIE"), ("Indomie Telor", "INDOMIE"), ("Indomie Bakso", "INDOMIE"), 
            ("Indomie Double Telor", "INDOMIE"), ("Indomie Keju", "INDOMIE"), ("Indomie Kornet", "INDOMIE"), ("Indomie Keju Kornet", "INDOMIE"), 
            ("Indomie Telor Keju", "INDOMIE"), ("Indomie Telor Kornet", "INDOMIE"),("Indomie (Keju, Telor, Kornet)", "INDOMIE"),

            ("Kentang Goreng", "SNACK"), ("Sosis Goreng", "SNACK"), ("Kentang Sosis", "SNACK"), ("Otak-Otak", "SNACK"), 
            ("Rujak Cireng", "SNACK"), ("Cireng Isi", "SNACK"), ("Nugget", "SNACK"), ("Pisang Coklat", "SNACK"), 
            ("Pisang Goreng 3 Rasa (Coklat, Keju, Susu)", "SNACK"), ("Dimsum 4 PCS", "SNACK"),
            ("Mix Plate (Sosis, Kentang, Otak-Otak)", "SNACK"), ("Roti Bakar", "SNACK"), ("Omelet Mie", "SNACK"),

            ("Susu Jahe", "MILK"), ("Susu Putih", "MILK"), ("Susu Coklat", "MILK"), ("Teh Tarik", "MILK"), ("Beng-Beng", "MILK"), 
            ("Milo", "MILK"),("Ovaltine", "MILK"), ("Energen", "MILK"), ("Extrajoss", "MILK"), ("Kukubima", "MILK"), 
            ("Extrajoss Susu", "MILK"),("Kukubima Susu", "MILK"), ("Chocolatos Coklat", "MILK"), ("Chocolatos Matcha", "MILK"),

            ("Kapal Api", "COFFEE"), ("Kopi Tubruk", "COFFEE"), ("Kopi Liong", "COFFEE"), ("ABC Susu", "COFFEE"), 
            ("Luwak White Coffee", "COFFEE"), ("Indocafe Milk", "COFFEE"), ("Good Day", "COFFEE"),

            ("Jeruk Nipis", "NUTRISARI"), ("Jeruk Peras", "NUTRISARI"), ("Leci", "NUTRISARI"), ("Leci Tea", "NUTRISARI"), ("Milky Orange", "NUTRISARI"),
            ("Semangka", "NUTRISARI"), ("Sirsak", "NUTRISARI"), ("Strawberry", "NUTRISARI"), ("Sweet Mango", "NUTRISARI"),("Sweet Orange", "NUTRISARI"),
        ]

        produk_map = {}

        for nama, kat in produk_data:
            c.execute(
                "INSERT INTO produk (nama, kategori) VALUES (%s, %s)",
                (nama, kat)
            )
            produk_map[nama] = c.lastrowid

        def resep(c, nama_menu, bahan_dict):

            c.execute(
                "SELECT id FROM produk WHERE nama=%s",
                (nama_menu,)
            )

            data = c.fetchone()

            if not data:
                print(f"Produk {nama_menu} tidak ditemukan")
                return

            produk_id = data[0]

            for bahan, qty in bahan_dict.items():

                c.execute(
                    "SELECT id FROM bahan WHERE nama=%s",
                    (bahan,)
                )

                data_bahan = c.fetchone()

                if not data_bahan:
                    print(f"Bahan {bahan} tidak ditemukan")
                    continue

                bahan_id = data_bahan[0]

                c.execute(
                    """
                    INSERT INTO resep (produk_id, bahan_id, qty)
                    VALUES (%s, %s, %s)
                    """,
                    (produk_id, bahan_id, qty)
                )
        # contoh resep
        resep(c, "Indomie", {"mie": 1})
        resep(c, "Indomie Double", {"mie": 2})
        resep(c, "Indomie Telor", {"mie": 1, "telor": 1})
        resep(c, "Indomie Bakso", {"mie": 1, "bakso": 1})
        resep(c, "Indomie Double Telor", {"mie": 2, "telor": 1})
        resep(c, "Indomie Keju", {"mie": 1, "keju": 1})
        resep(c, "Indomie Kornet", {"mie": 1, "kornet": 1})
        resep(c, "Indomie Keju Kornet", {"mie": 1, "keju": 1, "kornet": 1})
        resep(c, "Indomie Telor Keju", {"mie": 1, "telor": 1, "keju": 1})
        resep(c, "Indomie Telor Kornet", {"mie": 1, "telor": 1, "kornet" : 1})
        resep(c, "Indomie (Keju, Telor, Kornet)", {"mie": 1, "keju": 1, "telor": 1, "kornet": 1})        

        resep(c, "Sosis Goreng", {"sosis": 1})
        resep(c, "Kentang Goreng", {"kentang": 1})
        resep(c, "Otak-Otak", {"otak otak": 1})
        resep(c, "Rujak Cireng", {"cireng": 1})
        resep(c, "Cireng Isi", {"cireng": 1})
        resep(c, "Nugget", {"nugget": 1})
        resep(c, "Dimsum 4 PCS", {"dimsum": 1})
        resep(c, "Mix Plate (Sosis, Kentang, Otak-Otak)", {"mix plate": 1,})
        resep(c, "Roti Bakar", {"roti": 1})
        resep(c, "Omelet Mie", {"mie": 1})
        resep(c, "Kentang Sosis", {"kentang": 1, "sosis": 1})
        resep(c, "Pisang Coklat", { "pisang": 1, "coklat": 1})
        resep(c, "Pisang Goreng 3 Rasa (Coklat, Keju, Susu)", {"pisang": 1, "coklat": 1, "keju": 1, "susu": 1})
        resep(c, "Susu Jahe", {"susu": 1, "jahe": 1})
        resep(c, "Susu Putih", {"susu": 1})
        resep(c, "Susu Coklat", {"susu": 1, "coklat": 1})

        resep(c, "Teh Tarik", {"teh tarik": 1})
        resep(c, "Beng-Beng", {"beng beng": 1})
        resep(c, "Milo", {"milo": 1})
        resep(c, "Ovaltine", {"ovaltine": 1})
        resep(c, "Energen", {"energen": 1})
        resep(c, "Extrajoss", {"extrajoss": 1})
        resep(c, "Kukubima", {"kukubima": 1})
        resep(c, "Extrajoss Susu", { "extrajoss": 1, "susu": 1})
        resep(c, "Kukubima Susu", {"kukubima": 1, "susu": 1})
        resep(c, "Chocolatos Coklat", {"chocolatos coklat": 1})
        resep(c, "Chocolatos Matcha", {"chocolatos matcha": 1})

        resep(c, "Kapal Api", {"kapal api": 1})
        resep(c, "Kopi Liong", {"liong": 1})
        resep(c, "Kopi Tubruk", {"kopi tubruk": 1})
        resep(c, "ABC Susu", {"abc susu": 1})
        resep(c, "Luwak White Coffee", {"luwak white coffee": 1})
        resep(c, "Indocafe Milk", {"indocafe milk": 1})
        resep(c, "Good Day", {"good day": 1 })

        resep(c, "Jeruk Nipis", {"jeruk nipis": 1})
        resep(c, "Jeruk Peras", {"jeruk peras": 1})
        resep(c, "Leci", {"leci": 1})
        resep(c, "Leci Tea", {"leci tea": 1})
        resep(c, "Milky Orange", {"milky orange": 1})
        resep(c, "Semangka", {"semangka": 1})
        resep(c, "Sirsak", {"sirsak": 1})
        resep(c, "Strawberry", {"strawberry": 1})
        resep(c, "Sweet Mango", {"sweet mango": 1})
        resep(c, "Sweet Orange", {"sweet orange": 1})

    conn.commit()
    conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'ageto99':

            session['login'] = True
            return redirect('/')

        else:

            return render_template(
                'login.html',
                error='Username atau Password salah!'
            )

    return render_template('login.html')

@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/login')

@app.route('/')
def index():
    if 'login' not in session:
        return redirect('/login')

    conn = db()
    c = conn.cursor()

    # ================= PRODUK =================
    c.execute("SELECT * FROM produk")
    produk = c.fetchall()

    # ================= RESEP =================
    c.execute("""
    SELECT r.produk_id, b.nama, b.stok
    FROM resep r
    JOIN bahan b ON r.bahan_id = b.id
    """)
    data = c.fetchall()

    resep_map = {}
    for pid, nama, stok in data:
        if pid not in resep_map:
            resep_map[pid] = []
        resep_map[pid].append((nama, stok))

    # ================= RIWAYAT HARI INI =================
    today = datetime.now().strftime("%Y-%m-%d")

    c.execute("""
    SELECT * FROM transaksi
    WHERE waktu LIKE %s
    ORDER BY id DESC
    """, (today + "%",))
    orders = c.fetchall()

    # ================= TOTAL HARI INI =================
    c.execute("""
    SELECT SUM(total_harga), COUNT(*)
    FROM transaksi
    WHERE waktu LIKE %s
    """, (today + "%",))

    hasil = c.fetchone()
    total_hari_ini = hasil[0] if hasil[0] else 0
    jumlah_transaksi = hasil[1] if hasil[1] else 0

    # ================= PRODUK TERLARIS =================
    c.execute("""
    SELECT nama, SUM(qty) as total
    FROM transaksi
    WHERE waktu LIKE %s
    GROUP BY nama
    ORDER BY total DESC
    LIMIT 1
    """, (today + "%",))

    produk_terlaris = c.fetchone()

    conn.close()

    harga_map = {
    "Susu Putih": {"Hot":6000, "Ice":7000}, "Susu Coklat": {"Hot":6000, "Ice":7000}, "Teh Tarik": {"Hot":7000, "Ice":8000}, "Beng-Beng": {"Hot":7000, "Ice":8000},
    "Milo": {"Hot":8000, "Ice":10000}, "Ovaltine": {"Hot":8000, "Ice":10000}, "Energen": {"Hot":9000, "Ice":10000}, "Chocolatos Coklat": {"Hot":7000, "Ice":8000},
    "Chocolatos Matcha": {"Hot":7000, "Ice":8000}, "Kapal Api": {"Hot":5000, "Ice":7000}, "Kopi Tubruk": {"Hot":5000, "Ice":7000}, "Kopi Liong": {"Hot":7000, "Ice":14000},
    "ABC Susu": {"Hot":8000, "Ice":5000}, "Luwak White Coffee": {"Hot":5000, "Ice":7000}, "Indocafe Milk": {"Hot":5000, "Ice":7000}, "Good Day": {"Hot":7000, "Ice":8000}
    }

    harga_satuan = {
        "Indomie": 10000, "Indomie Double": 15000, "Indomie Telor": 12000, "Indomie Bakso": 12000, "Indomie Double Telor": 18000, "Indomie Keju": 11000,
        "Indomie Kornet": 13000, "Indomie Keju Kornet": 15000, "Indomie Telor Keju": 15000, "Indomie Telor Kornet": 18000, "Indomie (Keju, Telor, Kornet)": 20000,
            
        "Kentang Goreng": 15000, "Sosis Goreng": 15000, "Kentang Sosis": 15000, "Otak-Otak": 15000, "Rujak Cireng": 15000, "Cireng Isi": 15000, "Nugget": 15000,
        "Pisang Coklat": 15000, "Pisang Goreng 3 Rasa (Coklat, Keju, Susu)": 15000, "Dimsum 4 PCS": 15000, "Mix Plate (Sosis, Kentang, Otak-Otak)": 20000,
        "Roti Bakar": 15000, "Omelet Mie": 18000,

        "Susu Jahe": 5000, "Extrajoss": 7000, "Kukubima": 7000, "Extrajoss Susu": 8000, "Kukubima Susu": 8000,

        "Anggur": 6000, "Blewah": 6000, "Coco Pandan": 6000, "Jambu": 6000, "Jeruk Nipis": 6000, "Jeruk Peras": 6000, "Leci": 6000, "Leci Tea": 6000, 
        "Milky Orange": 6000, "Semangka": 6000, "Sirsak": 6000, "Strawberry": 6000, "Sweet Mango": 6000, "Sweet Orange": 6000 
    }


    return render_template(
    "index.html",
    produk=produk,
    orders=orders,
    resep_map=resep_map,
    harga_map=harga_map,
    harga_satuan=harga_satuan,
    total_hari_ini=total_hari_ini,
    jumlah_transaksi=jumlah_transaksi,
    produk_terlaris=produk_terlaris
)

# ================= BELI =================
@app.route('/beli', methods=['POST'])
def beli():
    id_produk = request.form['id']
    qty = int(request.form['qty'])
    kategori = request.form['kategori']
    varian = request.form.get('varian')
    harga = request.form.get('harga')

    # 🔥 WAJIB DI ATAS
    conn = db()
    c = conn.cursor()

    # ambil nama produk dulu
    c.execute("SELECT nama FROM produk WHERE id=%s", (id_produk,))
    nama = c.fetchone()[0]

    # kalau ada harga dari popup
    if harga:
        harga = int(harga)
    else:
        harga_satuan = {
            "Indomie": 10000, "Indomie Double": 15000, "Indomie Telor": 12000, "Indomie Bakso": 12000, "Indomie Double Telor": 18000, "Indomie Keju": 11000,
            "Indomie Kornet": 13000, "Indomie Keju Kornet": 15000, "Indomie Telor Keju": 15000, "Indomie Telor Kornet": 18000, "Indomie (Keju, Telor, Kornet)": 20000,
            
            "Kentang Goreng": 15000, "Sosis Goreng": 15000, "Kentang Sosis": 15000, "Otak-Otak": 15000, "Rujak Cireng": 15000, "Cireng Isi": 15000, "Nugget": 15000,
            "Pisang Coklat": 15000, "Pisang Goreng 3 Rasa (Coklat, Keju, Susu)": 15000, "Dimsum 4 PCS": 15000, "Mix Plate (Sosis, Kentang, Otak-Otak)": 20000,
            "Roti Bakar": 15000, "Omelet Mie": 18000,

            "Susu Jahe": 5000, "Extrajoss": 7000, "Kukubima": 7000, "Extrajoss Susu": 8000, "Kukubima Susu": 8000,

            "Anggur": 6000, "Blewah": 6000, "Coco Pandan": 6000, "Jambu": 6000, "Jeruk Nipis": 6000, "Jeruk Peras": 6000, "Leci": 6000, "Leci Tea": 6000, 
            "Milky Orange": 6000, "Semangka": 6000, "Sirsak": 6000, "Strawberry": 6000, "Sweet Mango": 6000, "Sweet Orange": 6000 }
        harga = harga_satuan.get(nama, 0)

    total = harga * qty

    c.execute("SELECT bahan_id, qty FROM resep WHERE produk_id=%s", (id_produk,))
    resep_list = c.fetchall()

    # 🔥 CEK STOK
    for bahan_id, q in resep_list:

        c.execute(
            "SELECT stok FROM bahan WHERE id=%s",
            (bahan_id,)
        )

        stok_sekarang = c.fetchone()[0]

        if stok_sekarang < q * qty:

            conn.close()

            return jsonify({
                "status": "ERROR",
                "message": f"Stok tidak cukup. Tersedia {stok_sekarang}"
            })

    # 🔥 KURANGI STOK
    for bahan_id, q in resep_list:
        c.execute("UPDATE bahan SET stok = stok - %s WHERE id=%s", (q * qty, bahan_id))

    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 🔥 TRANSAKSI HARIAN
    c.execute("""
        INSERT INTO transaksi (nama, qty, total_harga, waktu)
        VALUES (%s,%s,%s,%s)
    """, (nama, qty, total, waktu))
    trx_id = c.lastrowid

    # 🔥 HISTORY
    c.execute("""
        INSERT INTO history (nama, qty, status, total_harga, waktu)
        VALUES (%s,%s,%s,%s,%s)
    """, (nama, qty, "berhasil", total, waktu))

    conn.commit()

    # ambil stok terbaru
    stok_update = {}

    for bahan_id, q in resep_list:

        c.execute(
            "SELECT nama, stok FROM bahan WHERE id=%s",
            (bahan_id,)
        )

        nama_bahan, stok_baru = c.fetchone()

        stok_update[nama_bahan] = stok_baru

    conn.close()

    return jsonify({
        "status": "OK",
        "id": trx_id,
        "nama": nama,
        "qty": qty,
        "harga": total,
        "stok": stok_update
    })

from flask import jsonify
@app.route('/get_stok')
def get_stok():

    conn = db()
    c = conn.cursor()

    c.execute("""
    SELECT nama, stok
    FROM bahan
    """)

    data = c.fetchall()

    conn.close()

    hasil = {}

    for nama, stok in data:
        hasil[nama] = stok

    return jsonify(hasil)

# ================= CANCEL =================
@app.route('/cancel/<int:id>', methods=['GET'])
def cancel_form(id):
    return render_template('confirm_cancel.html', id=id)

@app.route('/cancel', methods=['POST'])
def cancel():
    id = request.form['id']
    password = request.form['password']

    PASSWORD_LOGIN = "admin123"

    if password != PASSWORD_LOGIN:
        return "Password salah", 403

    conn = db()
    c = conn.cursor()

    c.execute("SELECT nama, qty, total_harga FROM transaksi WHERE id=%s", (id,))
    trx = c.fetchone()

    if trx:
        nama, qty, total = trx
        # cari produk berdasarkan nama
        c.execute(
            "SELECT id FROM produk WHERE nama=%s",
            (nama,)
        )

        produk = c.fetchone()

        if produk:

            produk_id = produk[0]

            c.execute("""
                SELECT bahan_id, qty
                FROM resep
                WHERE produk_id=%s
            """, (produk_id,))

            resep_list = c.fetchall()

            # kembalikan stok
            for bahan_id, qty_resep in resep_list:

                c.execute("""
                    UPDATE bahan
                    SET stok = stok + %s
                    WHERE id=%s
                """, (
                    qty_resep * qty,
                    bahan_id
                ))

            waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            c.execute("""
                INSERT INTO history (nama, qty, status, total_harga, waktu)
                VALUES (%s, %s, %s, %s, %s)
            """, (nama, qty, "cancel", total, waktu))

            c.execute(
                "DELETE FROM transaksi WHERE id=%s",
                (id,)
            )

    conn.commit()
    conn.close()

    return jsonify({
    "status":"OK"
    })

# ================= HISTORY =================
@app.route('/history', methods=['GET', 'POST'])
def history():
    if 'login' not in session:
        return redirect('/login')

    conn = db()
    c = conn.cursor()

    if request.method == 'POST':
        tanggal = request.form['tanggal']

        c.execute("""
        SELECT * FROM history
        WHERE DATE(waktu)=%s
        ORDER BY waktu DESC
        """, (tanggal,))
    else:
        batas = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")

        c.execute("""
        SELECT * FROM history
        WHERE waktu >= %s
        ORDER BY waktu DESC
        """, (batas,))

    data = c.fetchall()
    conn.close()

    return render_template("history.html", data=data)

@app.route('/stok', methods=['GET', 'POST'])
def stok():
    if 'login' not in session:
        return redirect('/login')

    conn = db()
    c = conn.cursor()
    if request.method == 'POST':

        bahan_id = request.form['bahan_id']
        qty = int(request.form['qty'])
        aksi = request.form['aksi']

        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if aksi == "tambah":

            c.execute(
                "UPDATE bahan SET stok = stok + %s WHERE id=%s",
                (qty, bahan_id)
            )

            status = "tambah_stok"

        elif aksi == "kurang":

            c.execute(
                "SELECT stok FROM bahan WHERE id=%s",
                (bahan_id,)
            )

            stok_sekarang = c.fetchone()[0]

            if stok_sekarang < qty:
                conn.close()
                return redirect('/stok')

            c.execute(
                "UPDATE bahan SET stok = stok - %s WHERE id=%s",
                (qty, bahan_id)
            )

            status = "kurang_stok"

        # ambil nama bahan
        c.execute(
            "SELECT nama FROM bahan WHERE id=%s",
            (bahan_id,)
        )

        data_bahan = c.fetchone()

        if data_bahan:
            nama = data_bahan[0]

            c.execute("""
            INSERT INTO history
            (nama, qty, status, total_harga, waktu)
            VALUES (%s,%s,%s,NULL,%s)
            """, (nama, qty, status, waktu))

        conn.commit()
        conn.close()

        return redirect('/stok')

    # tampilkan bahan
    c.execute("SELECT * FROM bahan")
    bahan = c.fetchall()

    conn.close()
    return render_template("stok.html", bahan=bahan)

@app.route('/grafik', methods=['GET', 'POST'])
def grafik():

    if 'login' not in session:
        return redirect('/login')

    conn = db()
    c = conn.cursor()

    tanggal = ""

    query = """
    SELECT
        nama,
        SUM(
            CASE
                WHEN status='berhasil' THEN qty
                WHEN status='cancel' THEN -qty
                ELSE 0
            END
        ) as total
    FROM history
    WHERE status IN ('berhasil','cancel')
    """

    params = []

    if request.method == 'POST':

        tanggal = request.form['tanggal']

        query += " AND DATE(waktu)=%s"
        params.append(tanggal)

    query += """
    GROUP BY nama
    HAVING total > 0
    ORDER BY total DESC
    """

    c.execute(query, params)

    data = c.fetchall()

    label_grafik = [row[0] for row in data]
    jumlah_grafik = [row[1] for row in data]

    produk_terlaris = data[0][0] if data else "-"
    total_terjual = data[0][1] if data else 0

    conn.close()

    return render_template(
        'grafik.html',
        label_grafik=label_grafik,
        jumlah_grafik=jumlah_grafik,
        produk_terlaris=produk_terlaris,
        total_terjual=total_terjual,
        tanggal=tanggal
    )

@app.route('/report', methods=['GET', 'POST'])
def report():

    if 'login' not in session:
        return redirect('/login')

    conn = db()
    c = conn.cursor()

    tanggal = ""

    if request.method == 'POST':

        tanggal = request.form['tanggal']

        c.execute("""
            SELECT nama, qty, total_harga, waktu
            FROM transaksi
            WHERE DATE(waktu)=%s
            ORDER BY id DESC
        """, (tanggal,))

        history = c.fetchall()

        c.execute("""
            SELECT SUM(total_harga)
            FROM transaksi
            WHERE DATE(waktu)=%s
        """, (tanggal,))

    else:
        today = datetime.now().strftime("%Y-%m-%d")

        c.execute("""
            SELECT nama, qty, total_harga, waktu
            FROM transaksi
            WHERE DATE(waktu)=%s
            ORDER BY id DESC
        """, (today,))

        history = c.fetchall()

        c.execute("""
            SELECT SUM(total_harga)
            FROM transaksi
            WHERE DATE(waktu)=%s
        """, (today,))
    total = c.fetchone()[0] or 0

    conn.close()

    return render_template(
        'report.html',
        history=history,
        total=total,
        tanggal=tanggal
    )

@app.route('/export/pdf')
def export_pdf():

    tanggal = request.args.get("tanggal")

    conn = db()
    c = conn.cursor()

    if tanggal:
        c.execute("""
            SELECT nama, qty, total_harga, waktu
            FROM transaksi
            WHERE DATE(waktu)=%s
            ORDER BY id DESC
        """, (tanggal,))
    else:
        c.execute("""
            SELECT nama, qty, total_harga, waktu
            FROM transaksi
            ORDER BY id DESC
        """)

    data = c.fetchall()
    total_qty = 0
    total_harga = 0

    for row in data:
        total_qty += row[1]
        total_harga += row[2]
    conn.close()

    file_path = "report.pdf"

    pdf = SimpleDocTemplate(file_path)

    table_data = [["Nama", "Qty", "Total Harga", "Waktu"]]

    for row in data:
        table_data.append(list(row))
    table_data.append(["TOTAL", total_qty, total_harga, "-"])

    table = Table(table_data)
    table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),

    # 🔥 TOTAL ROW STYLE (BARIS PALING BAWAH)
    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
    ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
    ]))

    pdf.build([table])

    return send_file(file_path, as_attachment=True)

@app.route('/export/excel')
def export_excel():

    tanggal = request.args.get("tanggal")

    conn = db()
    c = conn.cursor()

    if tanggal:
        c.execute("""
            SELECT nama, qty, total_harga, waktu
            FROM transaksi
            WHERE DATE(waktu)=%s
            ORDER BY id DESC
        """, (tanggal,))
    else:
        c.execute("""
            SELECT nama, qty, total_harga, waktu
            FROM transaksi
            ORDER BY id DESC
        """)

    data = c.fetchall()

    total_qty = 0
    total_harga = 0

    for row in data:
        total_qty += row[1]
        total_harga += row[2]
    conn.close()

    df = pd.DataFrame(
        data,
        columns=['Nama Produk','Qty','Total Harga','Waktu']
    )

    df.loc[len(df)] = ["TOTAL", total_qty, total_harga, ""]

    file_path = "report.xlsx"
    df.to_excel(file_path, index=False)

    return send_file(file_path, as_attachment=True)

@app.route('/dashboard-data')
def dashboard_data():

    conn = db()
    c = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    # TOTAL HARI INI + JUMLAH TRANSAKSI
    c.execute("""
        SELECT SUM(total_harga), COUNT(*)
        FROM transaksi
        WHERE waktu LIKE %s
    """, (today + "%",))

    total_hari_ini, jumlah_transaksi = c.fetchone()

    # PRODUK TERLARIS
    c.execute("""
        SELECT nama, SUM(qty)
        FROM transaksi
        WHERE waktu LIKE %s
        GROUP BY nama
        ORDER BY SUM(qty) DESC
        LIMIT 1
    """, (today + "%",))

    produk = c.fetchone()

    conn.close()

    return jsonify({
        "total_hari_ini": total_hari_ini or 0,
        "jumlah_transaksi": jumlah_transaksi or 0,
        "produk_terlaris": produk[0] if produk else "-"
    })

# ================= RUN =================
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
