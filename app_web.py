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

# --- CSS CUSTOM UNTUK TAMPILAN MODERN ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .stProgress > div > div > div > div { background-color: #1f6feb; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI INTI (STEMMER & ANALISIS) ---
@st.cache_resource
def get_stemmer():
    factory = StemmerFactory()
    return factory.create_stemmer()

stemmer = get_stemmer()

def bersihkan_teks(teks):
    # Menghapus karakter aneh dan proses Stemming (Akar Kata)
    teks = teks.lower().replace('\n', ' ')
    return stemmer.stem(teks)

def baca_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        teks = ""
        for page in reader.pages:
            teks += page.extract_text()
        return teks
    except Exception as e:
        return ""

def ambil_teks_web(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Hapus bagian script dan style agar tidak terbaca sebagai teks
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
            
        paragraphs = soup.find_all('p')
        teks_web = " ".join([p.get_text() for p in paragraphs])
        return teks_web if teks_web.strip() else "Tidak ada teks paragraf yang bisa diambil."
    except:
        return "Error: Gagal terhubung ke website. Coba link lain."

def hitung_kemiripan(teks1, teks2):
    # Algoritma Jaccard Similarity (Mengecek irisan kata)
    set1 = set(teks1.split())
    set2 = set(teks2.split())
    if not set1 or not set2: return 0
    irisan = set1.intersection(set2)
    return (len(irisan) / len(set1.union(set2))) * 100

# --- TAMPILAN UTAMA ---
st.title("🛡️ FAZRUL PLAGIAT-CHECK PRO V3.0 (T-EDITION)")
st.caption("Sistem Audit Dokumen Akademik & Verifikasi Konten Digital")
st.divider()

# --- SIDEBAR CONTROL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=100)
    st.header("⚙️ Panel Kontrol")
    opsi = st.selectbox("Pilih Sumber Data:", ["Upload PDF", "Paste Teks AI", "Link Artikel Web"])
    
    st.divider()
    st.write("📊 **Info Database Lokal:**")
    folder_db = "database_lokal"
    if not os.path.exists(folder_db):
        os.makedirs(folder_db)
    
    files_in_db = [f for f in os.listdir(folder_db) if f.endswith('.pdf')]
    st.success(f"{len(files_in_db)} Dokumen Terdaftar")
    
    st.info("Sistem akan membandingkan data input dengan semua dokumen di database lokal.")

# --- LOGIKA INPUT DATA ---
teks_uji = ""
if opsi == "Upload PDF":
    file = st.file_uploader("Unggah file PDF uji", type="pdf")
    if file: 
        with st.spinner("Mengekstrak teks PDF..."):
            teks_uji = baca_pdf(file)
            st.success("PDF berhasil dibaca!")

elif opsi == "Paste Teks AI":
    teks_uji = st.text_area("Tempel teks (ChatGPT/Artikel) di sini:", height=250, placeholder="Masukkan teks minimal 10 kata...")

elif opsi == "Link Artikel Web":
    url_input = st.text_input("Masukkan URL Website (Contoh: https://news.detik.com/artikel-berita)")
    if url_input:
        with st.spinner("Sedang 'Scraping' konten web..."):
            teks_uji = ambil_teks_web(url_input)
            if "Error" in teks_uji:
                st.error(teks_uji)
                teks_uji = ""
            else:
                st.success("Teks website berhasil ditarik!")
                with st.expander("Lihat teks yang diambil"):
                    st.write(teks_uji[:500] + "...")

# --- PROSES ANALISIS ---
if st.button("🚀 JALANKAN ANALISIS SEKARANG"):
    if teks_uji and len(teks_uji.strip()) > 5:
        with st.spinner("Membersihkan kata & membandingkan dengan database..."):
            teks_uji_bersih = bersihkan_teks(teks_uji)
            hasil_analisis = []

            for f_name in files_in_db:
                with open(os.path.join(folder_db, f_name), "rb") as f:
                    teks_db_asli = baca_pdf(f)
                    teks_db_bersih = bersihkan_teks(teks_db_asli)
                    skor = hitung_kemiripan(teks_uji_bersih, teks_db_bersih)
                    hasil_analisis.append((f_name, skor))

            # Tampilkan Hasil
            st.subheader("📋 Ringkasan Analisis")
            if hasil_analisis:
                hasil_analisis.sort(key=lambda x: x[1], reverse=True)
                top_file, top_skor = hasil_analisis[0]

                c1, c2, c3 = st.columns(3)
                c1.metric("Skor Tertinggi", f"{top_skor:.1f}%")
                c2.metric("Sumber Terkait", top_file[:15] + "...")
                
                status = "⚠️ TERINDIKASI PLAGIAT" if top_skor > 30 else "✅ AMAN / ORISINAL"
                c3.write(f"**Status:** \n### {status}")

                st.divider()
                st.write("### Detail Perbandingan Database:")
                for nama, skor in hasil_analisis:
                    col_nama, col_prog = st.columns([1, 2])
                    col_nama.write(f"**{nama}**")
                    col_prog.progress(skor/100)
                    st.caption(f"Tingkat Kemiripan: {skor:.2f}%")
            else:
                st.warning("Database kosong. Silakan tambah file PDF ke folder 'database_lokal' di GitHub kamu.")
    else:
        st.error("Masukkan data (Upload/Paste/Link) yang valid terlebih dahulu!")

st.markdown("---")
st.caption("Developed by Fazrul | Versi 3.0-T (Deployment Active)")