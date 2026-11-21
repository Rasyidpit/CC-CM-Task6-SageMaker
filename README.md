# 🤖 Sesi Materi: AI & Machine Learning Inference (AWS SageMaker & Amplify - 21 November 2026)

Selamat datang di sesi materi Cloud Computing tanggal 21 November 2026. Minggu ini, kita akan membangun aplikasi **Full-Stack Machine Learning** standar lomba **LKS Cloud Computing** bernama **CM - Loan**.

## 🎯 Fokus Materi
Kita akan membangun sistem **CM - Loan (Loan Risk Prediction)** dengan arsitektur terpisah antara Frontend dan Backend:
- **Frontend (AWS Amplify):** Halaman web antarmuka pengguna untuk memasukkan profil pengajuan pinjaman.
- **Backend & AI (AWS Lambda + Amazon SageMaker):** Memproses data pengajuan, melakukan prediksi kelayakan menggunakan model **XGBoost**, dan menyimpan riwayat ke database.

## 📂 Struktur Repository
- `data/train.csv` — Dataset latihan (250 baris data nasabah).
- `data/validation.csv` — Dataset validasi (60 baris data uji akurasi).
- `lambda/lambda_function.py` — Kode backend API Lambda (Python 3.12).
- `frontend/index.html` — Kode tampilan web untuk di-deploy ke **AWS Amplify**.
- `stepbystep.md` — Panduan praktikum lengkap langkah demi langkah.

## 🛠️ Services yang Digunakan
- **Amazon S3**: Menyimpan dataset latihan (*Training & Validation Data*) serta hasil model AI.
- **Amazon SageMaker**: Melatih model Machine Learning (algoritma **XGBoost**) dan men-deploy-nya menjadi **Real-Time Endpoint**.
- **AWS Lambda**: API Backend yang menghubungkan Frontend dengan SageMaker Endpoint dan DynamoDB.
- **Amazon DynamoDB**: Menyimpan log riwayat pengajuan pinjaman nasabah.
- **AWS Amplify**: Hosting aplikasi web statis (`index.html`) dengan HTTPS otomatis.

## 📋 Materi Tugas
Semua instruksi langkah-demi-langkah dan panduan kerja kelompok dapat ditemukan di file berikut:

👉 **Buka Tugas Praktikum:** [stepbystep.md](./stepbystep.md)

🔗 **Cloud Computing Eskul:** [Hubungi Pengajar untuk bantuan]
