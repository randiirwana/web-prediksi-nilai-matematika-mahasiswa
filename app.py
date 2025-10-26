from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Global variables untuk model dan encoders
model = None
label_encoders = None

def load_model():
    """Load model dan label encoders yang sudah ditraining"""
    global model, label_encoders
    try:
        # Check if files exist
        if not os.path.exists('math_performance_model.pkl'):
            print("❌ File model tidak ditemukan: math_performance_model.pkl")
            return False
        if not os.path.exists('label_encoders.pkl'):
            print("❌ File label encoders tidak ditemukan: label_encoders.pkl")
            return False
            
        model = joblib.load('math_performance_model.pkl')
        label_encoders = joblib.load('label_encoders.pkl')
        print("✅ Model dan label encoders berhasil dimuat")
        return True
    except Exception as e:
        print(f"❌ Gagal memuat model: {e}")
        return False

@app.route('/')
def index():
    """Halaman utama"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'model_loaded': model is not None})

@app.route('/graphs')
def graphs():
    """Halaman grafik"""
    return render_template('graphs.html')

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint untuk prediksi performa matematika"""
    try:
        # Check if model is loaded
        if model is None or label_encoders is None:
            return jsonify({'error': 'Model belum dimuat. Silakan coba lagi dalam beberapa saat.'}), 503
            
        # Ambil data dari form
        data = request.get_json()
        
        # Validasi input
        required_fields = ['gender', 'race_ethnicity', 'parental_education', 'lunch', 'test_preparation']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Field {field} wajib diisi'}), 400
        
        # Buat DataFrame dengan data input (termasuk reading dan writing score)
        input_data = {
            'gender': data['gender'],
            'race/ethnicity': data['race_ethnicity'],
            'parental level of education': data['parental_education'],
            'lunch': data['lunch'],
            'test preparation course': data['test_preparation'],
            'reading score': data.get('reading_score', 75),  # Default value jika tidak ada
            'writing score': data.get('writing_score', 75)   # Default value jika tidak ada
        }
        
        # Konversi ke DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Encode categorical variables menggunakan label encoders yang sudah disimpan
        for col in input_df.columns:
            if col in label_encoders:
                input_df[col] = label_encoders[col].transform(input_df[col])
        
        # Prediksi
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]
        
        # Hasil
        result = {
            'prediction': int(prediction),
            'probability_high': float(probability[1]),
            'probability_low': float(probability[0]),
            'status': 'PERFORMA TINGGI' if prediction == 1 else 'PERFORMA RENDAH',
            'description': 'Mahasiswa diprediksi akan memiliki nilai matematika tinggi (≥70)' if prediction == 1 else 'Mahasiswa diprediksi akan memiliki nilai matematika rendah (<70)'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan: {str(e)}'}), 500


# Load model saat aplikasi dimulai
if not load_model():
    print("❌ Gagal memuat model, aplikasi akan tetap berjalan dengan error handling")

if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)