import re
import os
import glob
import PyPDF2
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ==========================================
# 1. INISIALISASI SISTEM & NLP
# ==========================================
print("--- SISTEM DETEKSI PLAGIARISME MULTI-SUMBER ---")
print("Status: Menyiapkan mesin NLP...")

# Memastikan resource NLTK siap
try:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except Exception as e:
    print(f"Peringatan download NLTK: {e}")

# Inisialisasi Sastrawi
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# ==========================================
# 2. FUNGSI PEMBANTU (ENGINE)
# ==========================================
def extract_pdf_text(path):
    """Mengekstrak teks dari PDF secara bersih"""
    text = ""
    try:
        with open(path, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
    except Exception as e:
        print(f"   [!] Gagal membaca {os.path.basename(path)}: {e}")
    return text

def preprocess_text(text):
    """Pembersihan: Lowercase, Hapus Simbol, & Stemming"""
    text = text.lower()
    # Menghapus selain huruf a-z dan spasi
    text = re.sub(r'[^a-z\s]', '', text)
    # Proses Stemming Sastrawi
    return stemmer.stem(text)

# ==========================================
# 3. SCANNING MULTI-FOLDER
# ==========================================
jalur_database = [
    "database_lokal/*.pdf",
    "database_eksternal/*.pdf"
]

print("\n[STEP 1] Mencari Dokumen di Database...")
list_file_ref = []
for jalur in jalur_database:
    files = glob.glob(jalur)
    list_file_ref.extend(files)
    print(f"   > Ditemukan {len(files)} file di jalur: {jalur}")

if not list_file_ref:
    print("\n[STOP] Error: Tidak ada file PDF di folder database!")
    exit()

# ==========================================
# 4. INPUT FILE UJI
# ==========================================
print("\n[STEP 2] Memilih File yang Akan Diuji")
file_uji = input("Masukkan nama file PDF uji (contoh: database_lokal\\fazrul.pdf): ")

if not os.path.exists(file_uji):
    print(f"[STOP] Error: File '{file_uji}' tidak ditemukan.")
    exit()

# ==========================================
# 5. PROSES ANALISIS (OPTIMIZED)
# ==========================================
print("\n[STEP 3] Menganalisis... (Mohon tunggu, sedang membedah kalimat)")

# 5a. Proses File Uji
teks_uji_raw = extract_pdf_text(file_uji)
kalimat_uji = nltk.sent_tokenize(teks_uji_raw)
# Pre-process semua kalimat uji sekali saja (biar cepat)
uji_cleaned = [preprocess_text(s) for s in kalimat_uji]

# 5b. Proses Bank Data Referensi
teks_ref_gabungan = ""
for path in list_file_ref:
    teks_ref_gabungan += extract_pdf_text(path) + " "
kalimat_ref = nltk.sent_tokenize(teks_ref_gabungan)
# Pre-process semua kalimat referensi sekali saja (biar cepat)
ref_cleaned = [preprocess_text(s) for s in kalimat_ref]

hasil_plagiat = []
skor_kalimat = []

# 5c. Perbandingan menggunakan Cosine Similarity
for idx, s_uji_clean in enumerate(uji_cleaned):
    if len(s_uji_clean.split()) < 4: continue
    
    is_mirip = False
    max_sim = 0
    
    for s_ref_clean in ref_cleaned:
        if len(s_ref_clean.split()) < 4: continue
        
        try:
            # Perbandingan TF-IDF
            vectorizer = TfidfVectorizer()
            tfidf = vectorizer.fit_transform([s_uji_clean, s_ref_clean])
            sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
            
            if sim > 0.80:
                is_mirip = True
                max_sim = sim
                break
        except:
            continue
            
    if is_mirip:
        hasil_plagiat.append(kalimat_uji[idx]) # Ambil teks aslinya
        skor_kalimat.append(max_sim * 100)

# ==========================================
# 6. LAPORAN HASIL AKHIR
# ==========================================
skor_total = (len(hasil_plagiat) / len(kalimat_uji)) * 100 if kalimat_uji else 0

print("\n" + "="*50)
print("HASIL ANALISIS PLAGIARISME")
print(f"File Diuji      : {file_uji}")
print(f"Total Dokumen   : {len(list_file_ref)} file referensi")
print(f"SKOR AKHIR      : {skor_total:.2f}%")
print("="*50)

if hasil_plagiat:
    print("\nCONTOH KALIMAT YANG TERDETEKSI MIRIP:")
    for i in range(min(5, len(hasil_plagiat))):
        print(f"[{i+1}] ({skor_kalimat[i]:.1f}%) {hasil_plagiat[i].strip()}")

print("\nSTATUS EVALUASI:")
if skor_total < 20:
    print(">>> AMAN: Dokumen cenderung orisinal.")
elif 20 <= skor_total <= 50:
    print(">>> WASPADA: Kemiripan sedang, perbaiki parafrase.")
else:
    print(">>> PLAGIAT: Kemiripan sangat tinggi, segera revisi.")
print("="*50)