# 🤖 Tugas Praktikum Kelompok: CM - Loan (AWS SageMaker + Lambda + Amplify)

## 🎯 Tujuan Tugas
Membangun aplikasi **Machine Learning End-to-End** standar LKS Cloud Computing bernama **CM - Loan** menggunakan **Amazon S3** (data storage), **Amazon SageMaker** (training & endpoint AI), **Amazon DynamoDB** (database riwayat), **AWS Lambda** (API backend), dan **AWS Amplify** (frontend web hosting).

> **👥 Pembagian Peran Kelompok (3–4 Orang per Akun AWS):**
> - **Anggota 1 (Storage & Database):** Mengerjakan Langkah 1 (S3 & DynamoDB).
> - **Anggota 2 (AI / SageMaker Engineer):** Mengerjakan Langkah 2 & Langkah 3 (Training & Deploy Endpoint).
> - **Anggota 3 (Backend & Frontend):** Mengerjakan Langkah 4, Langkah 5, & Langkah 6 (Lambda API, Amplify Hosting, & Testing).

---

## 🚀 Langkah 1: Menyiapkan S3 Bucket, Dataset, & DynamoDB

File dataset sudah tersedia di dalam folder `data/` pada repository ini (`train.csv` berisi 250 data latihan dan `validation.csv` berisi 60 data uji).

1. **Buat S3 Bucket:**
   - Buka AWS Console -> cari **S3** -> klik **Create bucket**.
   - **Bucket name:** `cm-loan-ml-namakelompok` (huruf kecil semua, pastikan unik).
   - **AWS Region:** Pilih **Asia Pacific (Singapore) `ap-southeast-1`**.
   - Biarkan pengaturan lain default (Block all public access tetap dicentang) -> klik **Create bucket**.

2. **Upload Dataset ke S3:**
   - Masuk ke bucket `cm-loan-ml-namakelompok` -> klik **Create folder** bernama `train` -> upload file `data/train.csv` ke dalamnya.
   - Kembali ke root bucket -> klik **Create folder** bernama `validation` -> upload file `data/validation.csv` ke dalamnya.

3. **Buat Tabel DynamoDB:**
   - Buka **DynamoDB** -> **Tables** -> **Create table**.
   - **Table name:** `CMLoan-Riwayat-NamaKelompok`
   - **Partition key:** `id_pengajuan` (String).
   - Klik **Create table**.

---

## 🚀 Langkah 2: Melatih Model AI (SageMaker Training Job)

Kita akan menggunakan algoritma bawaan AWS yaitu **XGBoost** untuk melatih model prediksi kelayakan pinjaman.

1. **Buat IAM Role untuk SageMaker:**
   - Buka **IAM** -> **Roles** -> **Create role**.
   - **Trusted entity:** `AWS service` -> pilih **SageMaker** -> **Next**.
   - Pastikan policy **`AmazonSageMakerFullAccess`** terpasang -> **Next**.
   - **Role name:** `CMLoan-SageMakerRole-NamaKelompok` -> klik **Create role**.

2. **Jalankan Training Job:**
   - Buka **Amazon SageMaker** -> menu kiri pilih **Training** -> **Training jobs** -> klik **Create training job**.
   - **Job name:** `cm-loan-xgb-namakelompok`
   - **IAM role:** Pilih `CMLoan-SageMakerRole-NamaKelompok`.
   - **Algorithm options:** Pilih **Amazon SageMaker built-in algorithm** -> pilih **XGBoost** (version `1.7-1`).
   - **Resource configuration:**
     - Instance type: `ml.m5.xlarge` (atau `ml.m5.large` jika tersedia).
     - Instance count: `1`.
   - **Hyperparameters** (ubah bagian penting ini saja):
     - `objective`: `binary:logistic`
     - `num_round`: `50`
   - **Input data configuration:**
     - **Channel 1 (`train`):** S3 location = `s3://cm-loan-ml-namakelompok/train/` | Content type = `text/csv`
     - Klik **Add channel** -> **Channel 2 (`validation`):** S3 location = `s3://cm-loan-ml-namakelompok/validation/` | Content type = `text/csv`
   - **Output data configuration:**
     - S3 output path: `s3://cm-loan-ml-namakelompok/output/`
   - Klik **Create training job** dan tunggu ± 3–5 menit hingga status berubah menjadi **Completed**.

---

## 🚀 Langkah 3: Deploy Model Menjadi Endpoint AI

Agar model yang sudah dilatih bisa dipanggil oleh aplikasi, kita harus mengubahnya menjadi **Real-Time Endpoint**.

1. **Buat Model:**
   - Buka detail Training Job yang sudah **Completed** tadi -> klik tombol **Create model** di pojok kanan atas.
   - **Model name:** `cm-loan-model-namakelompok`
   - **IAM role:** `CMLoan-SageMakerRole-NamaKelompok` -> klik **Create model**.

2. **Buat Endpoint:**
   - Di menu kiri SageMaker, pilih **Inference** -> **Endpoints** -> klik **Create endpoint**.
   - **Endpoint name:** `cm-loan-endpoint-namakelompok`
   - Pada bagian **Endpoint configuration**, klik **Create a new endpoint configuration**:
     - Configuration name: `cm-loan-config-namakelompok`
     - Pada **Production variants**, klik **Add model** -> pilih `cm-loan-model-namakelompok` -> klik **Save**.
     - Klik **Edit** pada variant tersebut -> ubah **Instance type** menjadi **`ml.m5.large`** (atau `ml.t2.medium` jika tersedia) -> **Save**.
     - Klik **Create endpoint configuration**.
   - Kembali ke halaman Create endpoint -> klik **Create endpoint**.
   - Tunggu ± 6–8 menit sampai status Endpoint berubah menjadi **InService** (hijau).

---

## 🚀 Langkah 4: Membuat API Backend (AWS Lambda)

Sambil menunggu Endpoint *InService*, buat fungsi Lambda sebagai API penghubung antara frontend Amplify dengan SageMaker dan DynamoDB.

1. **Buat Fungsi Lambda:**
   - Buka **Lambda** -> **Create function** -> **Author from scratch**.
   - **Function name:** `FunctionCMLoan-NamaKelompok`
   - **Runtime:** `Python 3.12` -> klik **Create function**.

2. **Berikan Izin IAM ke Lambda (SageMaker & DynamoDB):**
   - Masuk ke tab **Configuration** -> **Permissions** -> klik **Role name** (warna biru).
   - Klik **Add permissions** -> **Attach policies**.
   - Cari dan centang 2 policy berikut:
     1. `AmazonSageMakerFullAccess`
     2. `AmazonDynamoDBFullAccess`
   - Klik **Add permissions**.

3. **Masukkan Kode Program:**
   - Buka file `lambda/lambda_function.py` dari repository ini dan salin seluruh isinya.
   - Kembali ke Lambda -> tab **Code** -> ganti seluruh isi `lambda_function.py` dengan kode tersebut.
   - **PENTING:** Sesuaikan `ENDPOINT_NAME` dan `TABLE_NAME` milik kelompok kalian!
   - Klik **Deploy**.

4. **Aktifkan Function URL & CORS (PENTING!):**
   - Tab **Configuration** -> **Function URL** -> **Create function URL**.
   - **Auth type:** `NONE`.
   - Centang **Configure cross-origin resource sharing (CORS)**:
     - **Allow origin:** `*`
     - **Allow headers:** `content-type`
     - **Allow methods:** `POST`
   - Klik **Save**, lalu **salin Function URL** yang muncul!

---

## 🚀 Langkah 5: Deploy Frontend Web ke AWS Amplify

Sekarang kita akan men-deploy tampilan web (`frontend/index.html`) menggunakan **AWS Amplify**.

1. **Hubungkan Frontend dengan API Lambda:**
   - Buka file `frontend/index.html` di editor teks (Notepad / VS Code).
   - Cari baris: `const LAMBDA_API_URL = 'ISI_FUNCTION_URL_LAMBDA_KALIAN_DISINI';`
   - Ganti teks di dalam tanda kutip dengan **Function URL Lambda** yang sudah disalin di Langkah 4, lalu **Save**.
   - Masukkan file `index.html` tersebut ke dalam file ZIP (misalnya nama filenya: `web-cmloan.zip`).

2. **Deploy ke AWS Amplify:**
   - Buka AWS Console -> cari **AWS Amplify** -> klik **Create new app** (atau **New app** -> **Host web app**).
   - Pilih **Deploy without Git provider** -> klik **Next**.
   - **App name:** `cm-loan-ui-namakelompok`
   - **Environment name:** `prod`
   - Pilih **Drag and drop** -> tarik/upload file `web-cmloan.zip` yang berisi `index.html`.
   - Klik **Save and deploy** -> tunggu beberapa detik hingga muncul domain `https://prod.xxxx.amplifyapp.com`.

---

## 🚀 Langkah 6: Pengujian (Testing)

Pastikan status **SageMaker Endpoint** di Langkah 3 sudah **InService** sebelum melakukan pengujian.

1. Buka link **AWS Amplify** (`https://prod.xxxx.amplifyapp.com`) di browser HP atau laptop kalian.
2. **Uji Kasus 1 (Profil Aman / Reliable):**
   - Nama: `Andi Wijaya` | Umur: `35` | Pekerjaan: `PNS / BUMN` | Gaji: `15` | Lama Kerja: `6` | Pinjaman: `10`
   - Klik **Analisis Kelayakan dengan AI**.
   - **Hasil yang diharapkan:** Kotak hijau bertuliskan **LOW RISK (DISETUJUI)**.
3. **Uji Kasus 2 (Profil Berisiko Tinggi):**
   - Nama: `Rizky Pratama` | Umur: `21` | Pekerjaan: `Pekerja Lepas` | Gaji: `3` | Lama Kerja: `0` | Pinjaman: `25`
   - Klik **Analisis Kelayakan dengan AI**.
   - **Hasil yang diharapkan:** Kotak merah bertuliskan **HIGH RISK (DITOLAK)**.
4. **Cek Database:** Buka tabel **DynamoDB** -> klik **Explore table items** untuk memastikan kedua data pengujian tersimpan.

---

## ⚠️ PENTING: Pembersihan (Wajib Dilakukan Sebelum Pulang!)

Instance SageMaker Endpoint dikenakan biaya per jam jika dibiarkan menyala. Lakukan pembersihan ini bersama pengajar:

1. **SageMaker Endpoint:** Buka **SageMaker** -> **Inference** -> **Endpoints** -> pilih endpoint kalian -> **Actions** -> **Delete**.
2. **SageMaker Endpoint Config:** Buka **Endpoint configurations** -> pilih config kalian -> **Actions** -> **Delete**.
3. **Amplify App:** Buka **AWS Amplify** -> pilih app kalian -> **App settings** -> **General settings** -> **Delete app**.
4. **Lambda & DynamoDB:** Hapus fungsi Lambda dan tabel DynamoDB yang dibuat.
5. **S3 Bucket:** Kosongkan (*Empty*) lalu hapus S3 Bucket.
