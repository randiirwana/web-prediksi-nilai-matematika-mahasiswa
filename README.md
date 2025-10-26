# Student Math Performance Prediction Web Application

Aplikasi web untuk prediksi performa matematika mahasiswa menggunakan Machine Learning dengan Flask dan Bootstrap.

## 🚀 Features

- **Single Student Prediction**: Input manual untuk prediksi satu mahasiswa
- **Batch Upload**: Upload file CSV untuk prediksi multiple mahasiswa
- **Real-time Results**: Hasil prediksi dengan probability score
- **Beautiful UI**: Interface modern dengan Bootstrap 5
- **Responsive Design**: Compatible dengan semua device

## 📋 Requirements

- Python 3.8+
- Flask
- Pandas
- NumPy
- Scikit-learn
- Joblib

## 🛠️ Installation

1. **Clone atau download project**
```bash
git clone <repository-url>
cd student-math-performance-prediction
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Prepare dataset**
- Pastikan file `dataset_mahasiswa.csv` ada di root directory
- Dataset harus memiliki kolom: gender, race/ethnicity, parental level of education, lunch, test preparation course, math score, reading score, writing score

## 🎯 Usage

### 1. Training Model
```bash
python train_student_model.py
```

### 2. Run Web Application
```bash
python app_student.py
```

### 3. Access Application
- Buka browser dan kunjungi: `http://localhost:5000`

## 📊 Dataset Format

File CSV harus memiliki kolom berikut:
- `gender`: Gender mahasiswa (female/male)
- `race/ethnicity`: Kelompok etnis (group A, B, C, D, E)
- `parental level of education`: Tingkat pendidikan orang tua
- `lunch`: Tipe makan siang (free/reduced, standard)
- `test preparation course`: Persiapan ujian (completed, none)
- `math score`: Nilai matematika (target untuk analisis)
- `reading score`: Nilai membaca
- `writing score`: Nilai menulis

## 🔧 API Endpoints

### POST /predict
Prediksi single student
```json
{
  "gender": "female",
  "race_ethnicity": "group B",
  "parental_education": "bachelor's degree",
  "lunch": "standard",
  "test_preparation": "completed"
}
```

### POST /upload
Upload file CSV untuk batch prediction
- File: CSV dengan kolom yang sesuai
- Response: Summary hasil prediksi

## 📁 Project Structure

```
├── app_student.py              # Flask application
├── train_student_model.py      # Model training script
├── requirements.txt            # Dependencies
├── dataset_mahasiswa.csv       # Dataset
├── math_performance_model.pkl  # Trained model
├── label_encoders.pkl          # Label encoders
├── demo_student_data.csv       # Demo data
├── templates/                  # HTML templates
│   └── student_index.html
└── static/                     # Static files (CSS, JS)
```

## 🎨 UI Features

- **Hero Section**: Introduction dengan gradient background
- **Single Prediction Form**: Input form dengan dropdown
- **Batch Upload**: File upload dengan progress indicator
- **Results Display**: Card-based results dengan color coding
- **Responsive Design**: Mobile-friendly interface

## 📈 Model Performance

- **Algorithm**: Decision Tree Classifier (Pruned)
- **Features**: 7 features (Gender, Race, Education, Lunch, Test Prep, Reading Score, Writing Score)
- **Accuracy**: 82.5%
- **Target**: Math Performance (High ≥70, Low <70)

## 🔍 Key Insights

- **Gender**: Laki-laki memiliki performa lebih tinggi (47.9% vs 34.4%)
- **Race**: Group E memiliki performa tertinggi (64.3%)
- **Education**: Master's degree memiliki performa tertinggi (55.9%)
- **Lunch**: Standard lunch memiliki performa lebih tinggi (49.9% vs 24.5%)
- **Test Prep**: Completed course memiliki performa lebih tinggi (49.2% vs 36.3%)

## 🐛 Troubleshooting

### Model tidak ditemukan
```bash
python train_student_model.py
```

### Port sudah digunakan
```bash
# Ganti port di app_student.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Dependencies error
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 📞 Support

Jika ada masalah atau pertanyaan, silakan buat issue di repository ini.

## 📄 License

MIT License - bebas digunakan untuk keperluan edukasi dan komersial.
