## Menjalankan Aplikasi

Di repo ini ada dua cara pakai:

1. **CLI (Terminal)** → hilal.py
2. **Web (Flask)** → app.py

> Repo ini hanya bisa dijalankan menggunakan sistem operasi (os) Linux.
> Gunakan wsl jika Anda berjalan pada os Windows.
---

### 1) Persiapan umum

Jalankan dari folder proyek:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
```

---

### 2) Jalankan versi CLI (hilal.py)

```bash
python hilal.py
```

Akan tampil prompt:
- pilih kriteria (MABIMS / Wujudul / Odeh)
- masukkan tanggal (YYYY‑MM‑DD) atau tekan Enter untuk hari ini  
Hasil perhitungan akan ditampilkan di terminal.

---

### 3) Jalankan versi Web (Flask) (app.py)

```bash
python app.py
```

Buka di browser:

- `http://localhost:5000`

Web UI menyediakan input tanggal & lokasi, lalu memanggil API `/api/hilal` untuk menghitung posisi hilal dan menampilkan hasilnya.

User: buat dalam format md

GitHub Copilot: # Menjalankan Aplikasi

Repositori ini berisi dua antarmuka untuk menghitung posisi hilal:

- **CLI (Terminal)** → hilal.py
- **Web (Flask)** → app.py

---

## 1) Persiapan Umum

Jalankan dari folder proyek:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirement.txt
```

---

## 2) Versi CLI (hilal.py)

Jalankan:

```bash
python hilal.py
```

### Alur
- Pilih kriteria:
  - 1 = MABIMS (Nahdatul Ulama)
  - 2 = Wujudul (Muhammadiyah)
  - 3 = Odeh
- Masukkan tanggal (YYYY‑MM‑DD) atau tekan Enter untuk tanggal hari ini.
- Hasil perhitungan akan ditampilkan langsung di terminal.

---

## 3) Versi Web (Flask) (app.py)

Jalankan server Flask:

```bash
python app.py
```

Buka di browser:

- `http://localhost:5000`

### Fitur
- Input tanggal dan lokasi (atau gunakan Geolocation browser)
- Pilih kriteria hilal
- Tekan **Hitung Posisi Hilal**
- Hasil ditampilkan di UI (verdict, nilai astronomi, dan visualisasi langit)

---

### Kelebihan
- Visualisasi simulasi posisi bulan
- Mempermudah pengamatan
- Tidak memerlukan teleskop mahal
- Minim anggaran
- Sidang Isbat cepat

### Kekurangan
- Ga dapet duit perjalanan dinas
- Angaran kecil
- Bid'ah
