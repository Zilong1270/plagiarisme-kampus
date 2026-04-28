import streamlit as st
import os, re, time, requests
from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import PyPDF2

# --- KONFIGURASI ---
NAMA_APLIKASI = "Fazrul Plagiat-Check V4.3"
st.set_page_config(page_title=NAMA_APLIKASI, page_icon="🛡️")

# Inisialisasi Stemmer (Cache agar cepat)
@st.cache_resource
def load_stemmer():
    return StemmerFactory().create_stemmer()

stemmer = load_stemmer()

# --- FUNGSI PEMBERSIH TEKS ---
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

def jaccard_similarity(str1, str2):
    a = set(stemmer.stem(clean_text(str1)).split())
    b = set(stemmer.stem(clean_text(str2)).split())
    if not a or not b: return 0.0
    return (len(a.intersection(b)) / len(a.union(b))) * 100

# --- FUNGSI MANDIRI (WEB SEARCH) ---
def cari_global_internet(teks_user):
    # Ambil 10 kata pertama sebagai keyword pencarian
    keywords = " ".join(teks_user.split()[:10])
    url = f"https://www.google.com/search?q={keywords}"
    
    # User-Agent agar dianggap manusia oleh Google
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Mengambil cuplikan hasil pencarian (snippets)
        snippets = []
        for g in soup.find_all('div', class_='VwiC3b'): # Class Google Snippet terbaru
            snippets.append(g.get_text())
        
        return " ".join(snippets) if snippets else None
    except:
        return None

# --- UI UTAMA ---
st.title(f"🚀 {NAMA_APLIKASI}")
st.markdown("---")

uploaded_file = st.file_uploader("Upload Dokumen PDF", type="pdf")

if uploaded_file:
    # Baca PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    teks_uji = ""
    for page in pdf_reader.pages:
        teks_uji += page.extract_text()
    
    st.info(f"Karakter terdeteksi: {len(teks_uji)}")

    if st.button("JALANKAN AUDIT HYBRID"):
        # 1. CEK LOKAL (Folder database_lokal)
        st.write("🔎 Memeriksa database internal...")
        skor_lokal_max = 0
        # (Logika looping file lokal kamu di sini)
        
        time.sleep(1) # Efek loading
        
        # 2. CEK GLOBAL (Jika lokal bersih atau ingin validasi internet)
        st.write("🌐 Mencari referensi di Internet secara mandiri...")
        teks_internet = cari_global_internet(teks_uji)
        
        if teks_internet:
            skor_global = jaccard_similarity(teks_uji, teks_internet)
            
            # TAMPILAN HASIL
            st.subheader("Hasil Analisis Akhir")
            col1, col2 = st.columns(2)
            col1.metric("Skor Lokal", f"{skor_lokal_max:.1f}%")
            col2.metric("Skor Global (Internet)", f"{skor_global:.1f}%")
            
            if skor_global > 30:
                st.error("⚠️ Indikasi Plagiarisme Tinggi ditemukan di Internet!")
            else:
                st.success("✅ Dokumen relatif aman dari sumber publik internet.")
        else:
            st.warning("Gagal terhubung ke database global. Pastikan koneksi internet stabil.")