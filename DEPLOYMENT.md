# 🚀 Panduan Deployment ke Railway

## 📋 Persiapan

### 1. Buat Account Railway
- Kunjungi [railway.app](https://railway.app)
- Sign up dengan GitHub/GitHub
- Verifikasi email Anda

### 2. Install Railway CLI (Opsional)
```bash
npm i -g @railway/cli
railway login
```

## 🔧 Konfigurasi Project

### File-file yang Dibutuhkan:
- ✅ `Procfile` - Menentukan perintah untuk menjalankan aplikasi
- ✅ `requirements.txt` - Dependencies Python
- ✅ `runtime.txt` - Versi Python
- ✅ `railway.json` - Konfigurasi Railway
- ✅ `app.py` - Aplikasi Flask

### Struktur Project:
```
TA-05/
├── app.py
├── templates/
│   ├── index.html
│   └── graphs.html
├── static/
│   ├── feature_importance.png
│   ├── class_distribution.png
│   ├── performance_by_features.png
│   └── score_distribution.png
├── math_performance_model.pkl
├── label_encoders.pkl
├── Procfile
├── requirements.txt
├── runtime.txt
└── railway.json
```

## 📤 Deploy ke Railway

### Cara 1: Via Dashboard Railway

1. **Buka Railway Dashboard**
   - Login ke railway.app
   - Klik "New Project"

2. **Connect Repository**
   - Pilih "Deploy from GitHub repo"
   - Pilih repository Anda
   - Railway akan otomatis detect project

3. **Configure Variables**
   - Railway akan otomatis setup build
   - Tidak perlu variables tambahan untuk project ini

4. **Deploy**
   - Railway akan otomatis build dan deploy
   - Tunggu sampai status menjadi "Deployed"

### Cara 2: Via Railway CLI

1. **Login**
   ```bash
   railway login
   ```

2. **Initialize Project**
   ```bash
   railway init
   ```

3. **Deploy**
   ```bash
   railway up
   ```

## 🎯 Setelah Deploy

1. **URL Aplikasi**
   - Railway akan generate URL otomatis
   - Format: `https://your-app-name.up.railway.app`

2. **Custom Domain (Opsional)**
   - Settings > Domains
   - Tambahkan domain Anda

3. **Environment Variables (Jika diperlukan)**
   - Settings > Variables
   - Tambahkan variables jika ada

## 🔍 Troubleshooting

### Error: "Model file not found"
- Pastikan file `.pkl` ada di repository
- Check `.gitignore` tidak mengabaikan file tersebut

### Error: "Port already in use"
- Railway akan otomatis handle port
- Pastikan `gunicorn` terinstall

### Error: "Static files not loading"
- Pastikan folder `static/` ada di repository
- Check path ke gambar di template

### Error: "Memory limit exceeded"
- Railway free tier: 512MB RAM
- Upgrade ke Pro jika perlu lebih banyak memory

## 📝 Catatan Penting

1. **File .pkl harus ada**
   - Pastikan `math_performance_model.pkl` dan `label_encoders.pkl` ada
   - Size file: ~1-2MB

2. **Static Images**
   - Pastikan semua gambar PNG ada di folder `static/`
   - Generate ulang jika perlu: `python plot_charts.py`

3. **Build Time**
   - Build pertama: ~3-5 menit
   - Build berikutnya: ~1-2 menit

## 🎉 Selesai!

Setelah deploy sukses, aplikasi Anda akan tersedia di:
`https://your-app-name.up.railway.app`

**Fitur yang Tersedia:**
- ✅ Prediksi Performa Matematika
- ✅ Grafik Analisis Model
- ✅ Interface Bahasa Indonesia

