from flask import Flask, render_template, request, redirect
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)

# Fungsi koneksi ke PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        os.environ['DATABASE_URL'],
        cursor_factory=psycopg2.extras.RealDictCursor
    )

# Buat tabel otomatis jika belum ada
def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pengguna (
                id SERIAL PRIMARY KEY,
                nama VARCHAR(100),
                email VARCHAR(100) UNIQUE,
                password VARCHAR(100)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS layanan (
                id SERIAL PRIMARY KEY,
                nama VARCHAR(100),
                deskripsi TEXT,
                harga INTEGER
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("✔️ Inisialisasi DB berhasil")
    except Exception as e:
        print(f"❌ Error saat inisialisasi DB: {e}")

# Halaman utama
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/layanan')
def layanan():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM layanan;")
    data_layanan = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('layanan/index.html', layanan=data_layanan)
@app.route('/isi_layanan')
def isi_layanan():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO layanan (nama, deskripsi, harga) VALUES
        ('Farmasi', 'Layanan obat dan resep dokter', 25000),
        ('Pemeriksaan Umum', 'Cek kondisi kesehatan dasar', 50000),
        ('Vaksinasi', 'Pemberian vaksin berbagai jenis', 75000)
    """)
    conn.commit()
    cur.close()
    conn.close()
    return "Data layanan berhasil ditambahkan!"
@app.route('/layanan/<int:layanan_id>')
def detail_layanan(layanan_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM layanan WHERE id = %s;", (layanan_id,))
    layanan = cur.fetchone()
    cur.close()
    conn.close()

    if layanan is None:
        return "Layanan tidak ditemukan", 404

    return render_template('layanan/detail.html', layanan=layanan)



# Halaman register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO pengguna (nama, email, password) VALUES (%s, %s, %s);", (nama, email, password))
            conn.commit()
            cur.close()
            conn.close()
            return redirect('/')
        except Exception as e:
            return f"Terjadi kesalahan: {e}"

    return render_template('register.html')

@app.route('/init')
def init_route():
    try:
        init_db()
        return "✅ Database berhasil diinisialisasi!"
    except Exception as e:
        return f"❌ Gagal inisialisasi DB: {e}"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

