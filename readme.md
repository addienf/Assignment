# 🛍️ Dashboard Analisis Penjualan & RFM Customer Segmentation

Dashboard interaktif berbasis **Streamlit** untuk menganalisis data penjualan toko online serta mengidentifikasi perilaku pelanggan menggunakan metode **RFM (Recency, Frequency, Monetary)**.

---

## 🚀 **Deskripsi Singkat**

Proyek ini membantu tim bisnis dan analis data untuk memahami:

- Tren penjualan dari waktu ke waktu.
- Negara dengan kontribusi penjualan tertinggi.
- Produk yang paling laku.
- Segmentasi pelanggan menggunakan **Analisis RFM**.

Dashboard ini memiliki dua halaman utama:

1. **Overview Dashboard** → Ringkasan performa penjualan.
2. **Analisis RFM** → Analisis perilaku pelanggan berdasarkan Recency, Frequency, dan Monetary.

---

## 🧩 **Fitur Utama**

### 🔹 1. Overview Dashboard

- Menampilkan **KPI utama**: Total Penjualan, Jumlah Transaksi, Jumlah Pelanggan.
- Visualisasi:
  - Top 10 Negara dengan Penjualan Tertinggi.
  - Top 10 Produk Terlaris.
  - Tren Penjualan Bulanan.
- **Filter interaktif berdasarkan Negara.**
- Tombol **Reset Filter** untuk menampilkan semua data kembali.

### 🔹 2. Analisis RFM

- Distribusi nilai **Recency, Frequency, Monetary**.
- Jumlah pelanggan per **Segment RFM**.
- Rata-rata nilai RFM per segment.
- **Filter interaktif berdasarkan Segment.**
- Tombol **Reset Filter Segment.**

---

### Instalasi

Periksa versi Python Anda:

```bash
python --version
```

Import Repositorinya:

```bash
git clone https://github.com/addienf/Assignment.git
cd main
```

Buat Environtment Untuk Library:

```bash
python -m venv my_env
```

Jalankan Scripts Library:

```bash
my_env\Scripts\activate
```

Install Dependency:

```bash
pip install -r requirements.txt
```

Jalankan Program:

```bash
streamlit run assignment.py
```
