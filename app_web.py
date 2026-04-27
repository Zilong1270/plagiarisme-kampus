import streamlit as st
import os
import requests
from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import PyPDF2

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Fazrul Plagiat-Check T-Pro", layout="wide", page_icon="🛡️")

# --- CSS CUSTOM ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .hasil-box { padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI INTI ---
@st.cache_resource
def get_stemmer():
    factory = StemmerFactory()
    return factory.create_stemmer()

stemmer = get_stemmer()

def bersihkan_teks(teks):
    teks = teks.lower().replace('\n', ' ')
    return stemmer.stem(teks)

def baca_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        teks = ""
        for page in reader.pages:
            teks += page.extract_text()
        return teks
    except: return ""

def ambil_teks_web(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for s in soup(["script", "style"]): s.decompose()
        return " ".join([p.get_text() for p in soup.find_all('p')])
    except: return "Error: Gagal mengambil data."

def hitung_kemiripan(teks1, teks2):
    set1, set2 = set(teks1.split()), set(teks2.split())
    if not set1 or not set2: return 0
    return (len(set1.intersection(set2)) / len(set1.union(set2))) * 100

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=80)
    st.title("Menu Audit")
    opsi = st.selectbox("Pilih Metode:", ["Upload PDF", "Paste Teks AI", "Link Artikel Web"])
    st.divider()
    st.write("👤 **Pengembang**")
    st.write("**Fazrul**")
    st.link_button("📸 Instagram", "https://www.instagram.com/fazzrul__")
    st.divider()
    folder_db = "database_lokal"
    if not os.path.exists(folder_db): os.makedirs(folder_db)
    jml_file = len([f for f in os.listdir(folder_db) if f.endswith('.pdf')])
    st.info(f"📁 {jml_file} Arsip Terenkripsi")

# --- KONTEN UTAMA ---
st.title("🛡️ FAZRUL PLAGIAT-CHECK PRO V3.3")
st.markdown("---")

teks_uji = ""
if opsi == "Upload PDF":
    file = st.file_uploader("Pilih File PDF", type="pdf")
    if file: teks_uji = baca_pdf(file)
elif opsi == "Paste Teks AI":
    teks_uji = st.text_area("Tempel Teks:", height=200)
elif opsi == "Link Artikel Web":
    url = st.text_input("Link URL:")
    if url: teks_uji = ambil_teks_web(url)

if st.button("🔍 JALANKAN VERIFIKASI"):
    if teks_uji:
        with st.spinner("Sistem sedang memverifikasi..."):
            teks_uji_bersih = bersihkan_teks(teks_uji)
            hasil = []
            files_in_db = [f for f in os.listdir(folder_db) if f.endswith('.pdf')]
            
            for f_name in files_in_db:
                with open(os.path.join(folder_db, f_name), "rb") as f:
                    t_db_bersih = bersihkan_teks(baca_pdf(f))
                    skor = hitung_kemiripan(teks_uji_bersih, t_db_bersih)
                    hasil.append(skor)
            
            if hasil:
                hasil.sort(reverse=True)
                top_skor = hasil[0]
                
                # Kotak Hasil Utama
                warna = "#ff4b4b" if top_skor > 30 else "#09ab3b"
                st.markdown(f"""
                <div class="hasil-box" style="border-left: 10px solid {warna};">
                    <h2 style="color: {warna};">Hasil Analisis: {'⚠️ TERINDIKASI PLAGIAT' if top_skor > 30 else '✅ DOKUMEN AMAN'}</h2>
                    <p>Skor Kemiripan Tertinggi: <b>{top_skor:.2f}%</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("### 📊 Perbandingan Detail Arsip:")
                for i, skor in enumerate(hasil):
                    col1, col2 = st.columns([1, 3])
                    col1.write(f"**Arsip [ID-0{i+1}]**")
                    col2.progress(skor/100)
                    st.caption(f"Tingkat kesamaan data: {skor:.2f}%")
            else:
                st.warning("Database tidak ditemukan.")
    else:
        st.error("Masukkan data uji!")

st.divider()
st.caption("© 2026 Fazrul Technology | Secure & Private Audit System")