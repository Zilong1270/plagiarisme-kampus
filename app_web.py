import streamlit as st
import os
import requests
from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import PyPDF2

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Fazrul Plagiat-Check T-Pro", 
    layout="wide", 
    page_icon="🛡️"
)

# --- CSS CUSTOM UNTUK TAMPILAN PROFESIONAL ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e3440,#2e3440); color: white; }
    a { text-decoration: none; color: #58a6ff; }
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
    except:
        return ""

def ambil_teks_web(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        paragraphs = soup.find_all('p')
        teks_web = " ".join([p.get_text() for p in paragraphs])
        return teks_web
    except:
        return "Error: Gagal mengambil data dari URL."

def hitung_kemiripan(teks1, teks2):
    set1 = set(teks1.split())
    set2 = set(teks2.split())
    if not set1 or not set2: return 0
    irisan = set1.intersection(set2)
    return (len(irisan) / len(set1.union(set2))) * 100

# --- SIDEBAR (PROFIL & KONTROL) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=80)
    st.title("Pusat Kendali")
    
    opsi = st.selectbox("Metode Uji:", ["Upload PDF", "Paste Teks AI", "Link Artikel Web"])
    
    st.divider()
    st.write("👤 **Profil Pengembang**")
    st.write("**Fazrul**")
    st.write("🎓 *AI Content Auditor*")
    
    # Ganti username_kamu dengan username IG aslimu
    st.link_button("📸 Ikuti Instagram Saya", "https://www.instagram.com/fazzrul__")
    
    st.divider()
    st.write("📊 **Status Database:**")
    folder_db = "database_lokal"
    if not os.path.exists(folder_db): os.makedirs(folder_db)
    files_in_db = [f for f in os.listdir(folder_db) if f.endswith('.pdf')]
    st.success(f"{len(files_in_db)} Dokumen Tersedia")

# --- KONTEN UTAMA ---
st.title("🛡️ FAZRUL PLAGIAT-CHECK PRO V3.1")
st.subheader("Sistem Verifikasi Orisinalitas Teks (T-Edition)")
st.markdown("---")

teks_uji = ""

if opsi == "Upload PDF":
    file = st.file_uploader("Unggah PDF", type="pdf")
    if file: teks_uji = baca_pdf(file)
elif opsi == "Paste Teks AI":
    teks_uji = st.text_area("Tempel teks di sini:", height=250)
elif opsi == "Link Artikel Web":
    url = st.text_input("Tempel URL Artikel:")
    if url:
        with st.spinner("Membaca konten web..."):
            teks_uji = ambil_teks_web(url)

# Tombol Eksekusi
if st.button("🚀 MULAI ANALISIS"):
    if teks_uji:
        with st.spinner("Sedang memproses..."):
            teks_uji_bersih = bersihkan_teks(teks_uji)
            hasil = []
            
            for f_name in files_in_db:
                with open(os.path.join(folder_db, f_name), "rb") as f:
                    t_db_bersih = bersihkan_teks(baca_pdf(f))
                    skor = hitung_kemiripan(teks_uji_bersih, t_db_bersih)
                    hasil.append((f_name, skor))
            
            if hasil:
                hasil.sort(key=lambda x: x[1], reverse=True)
                top_file, top_skor = hasil[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Skor Kemiripan Tertinggi", f"{top_skor:.2f}%")
                with col2:
                    status = "⚠️ TERINDIKASI PLAGIAT" if top_skor > 30 else "✅ AMAN"
                    st.write(f"**Status Dokumen:** \n### {status}")
                
                st.write("### Detail Database:")
                for nama, skor in hasil:
                    st.write(f"**{nama}**")
                    st.progress(skor/100)
            else:
                st.warning("Database lokal kosong.")
    else:
        st.error("Masukkan data terlebih dahulu!")

st.divider()
st.caption("© 2026 Fazrul Technology | Versi 3.1 Final Update")