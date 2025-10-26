"""
Script untuk membuat grafik hasil model dan menyimpannya
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
import joblib
import os
from sklearn.preprocessing import LabelEncoder

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_data_and_model():
    """Load dataset dan model"""
    print("📊 Memuat dataset dan model...")
    
    # Check if dataset exists
    if not os.path.exists('dataset_mahasiswa.csv'):
        print("⚠️ Dataset tidak ditemukan, menggunakan data dummy...")
        return create_dummy_data()
    
    # Load dataset
    df = pd.read_csv('dataset_mahasiswa.csv')
    
    # Load model dan encoders
    model = joblib.load('math_performance_model.pkl')
    label_encoders = joblib.load('label_encoders.pkl')
    
    # Prepare data
    df['math_performance'] = df['math score'].apply(lambda x: 1 if x >= 70 else 0)
    
    return df, model, label_encoders

def create_dummy_data():
    """Create dummy data for chart generation when dataset is not available"""
    print("🔧 Membuat data dummy untuk grafik...")
    
    # Create dummy dataframe with same structure
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'gender': np.random.choice(['male', 'female'], n_samples),
        'race/ethnicity': np.random.choice(['group A', 'group B', 'group C', 'group D', 'group E'], n_samples),
        'parental level of education': np.random.choice(['some high school', 'high school', 'some college', 'associate\'s degree', 'bachelor\'s degree', 'master\'s degree'], n_samples),
        'lunch': np.random.choice(['standard', 'free/reduced'], n_samples),
        'test preparation course': np.random.choice(['none', 'completed'], n_samples),
        'reading score': np.random.normal(70, 15, n_samples),
        'writing score': np.random.normal(70, 15, n_samples),
        'math score': np.random.normal(70, 15, n_samples)
    }
    
    df = pd.DataFrame(data)
    df['math_performance'] = df['math score'].apply(lambda x: 1 if x >= 70 else 0)
    
    # Create dummy model
    X = df.drop(['math score', 'math_performance'], axis=1)
    y = df['math_performance']
    
    # Encode categorical variables
    X_encoded = X.copy()
    le_dict = {}
    for col in X_encoded.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        X_encoded[col] = le.fit_transform(X_encoded[col])
        le_dict[col] = le
    
    # Train simple model
    model = DecisionTreeClassifier(max_depth=5, random_state=42)
    model.fit(X_encoded, y)
    
    return df, model, le_dict

def plot_feature_importance(model):
    """Plot feature importance"""
    print("📈 Membuat grafik feature importance...")
    
    # Feature importance
    importance = model.feature_importances_
    feature_names = ['Jenis Kelamin', 'Kelompok Etnis', 'Pendidikan Orang Tua', 
                    'Status Ekonomi', 'Kursus Persiapan', 'Nilai Membaca', 'Nilai Menulis']
    
    # Sort by importance
    indices = np.argsort(importance)[::-1]
    
    plt.figure(figsize=(10, 6))
    bars = plt.barh(range(len(indices)), importance[indices], color='#2c3e50')
    plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
    plt.xlabel('Tingkat Kepentingan', fontsize=12, fontweight='bold')
    plt.title('Tingkat Kepentingan Fitur dalam Model', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    
    # Add value labels
    for i, (idx, bar) in enumerate(zip(indices, bars)):
        width = bar.get_width()
        plt.text(width + 0.01, bar.get_y() + bar.get_height()/2, 
                f'{width:.3f}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('static/feature_importance.png', dpi=300, bbox_inches='tight')
    print("✅ Grafik feature importance disimpan: static/feature_importance.png")
    plt.close()

def plot_class_distribution(df):
    """Plot distribusi kelas"""
    print("📊 Membuat grafik distribusi kelas...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Pie chart
    performance_counts = df['math_performance'].value_counts()
    labels = ['Performansi Tinggi (≥70)', 'Performansi Rendah (<70)']
    colors = ['#27ae60', '#e74c3c']
    
    axes[0].pie(performance_counts.values, labels=labels, autopct='%1.1f%%', 
                startangle=90, colors=colors, textprops={'fontsize': 11, 'fontweight': 'bold'})
    axes[0].set_title('Distribusi Performansi Matematika', fontsize=13, fontweight='bold')
    
    # Bar chart
    bars = axes[1].bar(labels, performance_counts.values, color=colors, alpha=0.8)
    axes[1].set_ylabel('Jumlah Mahasiswa', fontsize=11, fontweight='bold')
    axes[1].set_title('Jumlah Mahasiswa per Kategori', fontsize=13, fontweight='bold')
    axes[1].grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height,
                     f'{int(height)}', ha='center', va='bottom', 
                     fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('static/class_distribution.png', dpi=300, bbox_inches='tight')
    print("✅ Grafik distribusi kelas disimpan: static/class_distribution.png")
    plt.close()

def plot_performance_by_features(df):
    """Plot performansi berdasarkan fitur"""
    print("📊 Membuat grafik performansi berdasarkan fitur...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Gender
    gender_perf = df.groupby('gender')['math_performance'].mean() * 100
    axes[0, 0].bar(gender_perf.index, gender_perf.values, color=['#e74c3c', '#3498db'], alpha=0.8)
    axes[0, 0].set_title('Performansi berdasarkan Jenis Kelamin', fontsize=12, fontweight='bold')
    axes[0, 0].set_ylabel('Persentase Performansi Tinggi (%)', fontsize=10)
    axes[0, 0].grid(axis='y', alpha=0.3)
    axes[0, 0].set_xticklabels(['Perempuan', 'Laki-laki'])
    
    # Race/Ethnicity
    race_perf = df.groupby('race/ethnicity')['math_performance'].mean() * 100
    x_pos = range(len(race_perf))
    axes[0, 1].bar(x_pos, race_perf.values, color='#9b59b6', alpha=0.8)
    axes[0, 1].set_title('Performansi berdasarkan Kelompok Etnis', fontsize=12, fontweight='bold')
    axes[0, 1].set_ylabel('Persentase Performansi Tinggi (%)', fontsize=10)
    axes[0, 1].set_xticks(x_pos)
    axes[0, 1].set_xticklabels(['A', 'B', 'C', 'D', 'E'], rotation=0)
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # Education
    edu_perf = df.groupby('parental level of education')['math_performance'].mean() * 100
    y_pos = range(len(edu_perf))
    axes[1, 0].barh(y_pos, edu_perf.values, color='#16a085', alpha=0.8)
    axes[1, 0].set_title('Performansi berdasarkan Pendidikan Orang Tua', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('Persentase Performansi Tinggi (%)', fontsize=10)
    axes[1, 0].set_yticks(y_pos)
    axes[1, 0].set_yticklabels(edu_perf.index, fontsize=9)
    axes[1, 0].grid(axis='x', alpha=0.3)
    
    # Test Prep
    prep_perf = df.groupby('test preparation course')['math_performance'].mean() * 100
    x_pos = range(len(prep_perf))
    axes[1, 1].bar(x_pos, prep_perf.values, color=['#f39c12', '#e67e22'], alpha=0.8)
    axes[1, 1].set_title('Performansi berdasarkan Persiapan Ujian', fontsize=12, fontweight='bold')
    axes[1, 1].set_ylabel('Persentase Performansi Tinggi (%)', fontsize=10)
    axes[1, 1].set_xticks(x_pos)
    axes[1, 1].set_xticklabels(['None', 'Completed'], rotation=0)
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('static/performance_by_features.png', dpi=300, bbox_inches='tight')
    print("✅ Grafik performansi berdasarkan fitur disimpan: static/performance_by_features.png")
    plt.close()

def plot_score_distribution(df):
    """Plot distribusi nilai"""
    print("📊 Membuat grafik distribusi nilai...")
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    # Math Score
    axes[0].hist(df['math score'], bins=20, color='#e74c3c', alpha=0.7, edgecolor='black')
    axes[0].axvline(df['math score'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["math score"].mean():.1f}')
    axes[0].set_title('Distribusi Nilai Matematika', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Nilai', fontsize=10)
    axes[0].set_ylabel('Frekuensi', fontsize=10)
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # Reading Score
    axes[1].hist(df['reading score'], bins=20, color='#3498db', alpha=0.7, edgecolor='black')
    axes[1].axvline(df['reading score'].mean(), color='blue', linestyle='--', linewidth=2, label=f'Mean: {df["reading score"].mean():.1f}')
    axes[1].set_title('Distribusi Nilai Membaca', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Nilai', fontsize=10)
    axes[1].set_ylabel('Frekuensi', fontsize=10)
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    # Writing Score
    axes[2].hist(df['writing score'], bins=20, color='#27ae60', alpha=0.7, edgecolor='black')
    axes[2].axvline(df['writing score'].mean(), color='green', linestyle='--', linewidth=2, label=f'Mean: {df["writing score"].mean():.1f}')
    axes[2].set_title('Distribusi Nilai Menulis', fontsize=12, fontweight='bold')
    axes[2].set_xlabel('Nilai', fontsize=10)
    axes[2].set_ylabel('Frekuensi', fontsize=10)
    axes[2].legend()
    axes[2].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('static/score_distribution.png', dpi=300, bbox_inches='tight')
    print("✅ Grafik distribusi nilai disimpan: static/score_distribution.png")
    plt.close()

def main():
    """Main function"""
    print("🚀 Membuat grafik untuk aplikasi web")
    print("=" * 60)
    
    # Create static directory
    os.makedirs('static', exist_ok=True)
    
    # Load data and model
    df, model, label_encoders = load_data_and_model()
    
    # Create plots
    plot_feature_importance(model)
    plot_class_distribution(df)
    plot_performance_by_features(df)
    plot_score_distribution(df)
    
    print("\n🎉 Semua grafik berhasil dibuat!")
    print("=" * 60)
    print("📁 Grafik tersimpan di folder 'static/':")
    print("   - feature_importance.png")
    print("   - class_distribution.png")
    print("   - performance_by_features.png")
    print("   - score_distribution.png")

if __name__ == "__main__":
    main()

