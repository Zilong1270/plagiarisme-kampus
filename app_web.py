import streamlit as st
import os
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import PyPDF2
from docx import Document

# Konfigurasi Halaman
st.set_page_config(page_title="Verifikasi-AI Pro", layout="wide")

# CSS untuk tampilan lebih keren
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextArea textarea { background-color: #161b22; color: white; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# Inisialisasi Stemmer Sastrawi
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def bersihkan_teks(teks):
    teks = teks.lower()
    return stemmer.stem(teks)

def baca_pdf(file):
    reader = PyPDF2.PdfReader(file)
    teks = ""
    for page in reader.pages:
        teks += page.extract_text()
    return teks

def hitung_kemiripan(teks1, teks2):
    set1 = set(teks1.split())
    set2 = set(teks2.split())
    if not set1 or not set2: return 0
    irisan = set1.intersection(set2)
    return (len(irisan) / len(set1.union(set2))) * 100

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=100)
    st.title("Audit Sistem")
    mode = st.radio("Pilih Metode Uji:", ["Upload File PDF", "Paste Teks (AI/Internet)"])
    st.divider()
    st.info("Sistem ini membandingkan teks dengan database lokal untuk verifikasi keaslian.")

st.title("🛡️ VERIFIKASI-AI PRO")
st.subheader("Sistem Deteksi Kemiripan & Validasi Dokumen")

teks_uji = ""

# Input Section
if mode == "Upload File PDF":
    file_upload = st.file_uploader("Unggah Dokumen Uji (PDF)", type=["pdf"])
    if file_upload:
        teks_uji = baca_pdf(file_upload)
else:
    teks_uji = st.text_area("Tempel Teks dari Internet/AI di sini:", placeholder="Paste teks ChatGPT atau artikel web di sini...", height=300)

if st.button("Mulai Verifikasi Sekarang"):
    if teks_uji:
        with st.spinner("Sedang menganalisis teks..."):
            teks_uji_bersih = bersihkan_teks(teks_uji)
            
            # Cek ke Database Lokal
            folder_db = "database_lokal"
            hasil_akhir = []
            
            if os.path.exists(folder_db):
                for file_name in os.listdir(folder_db):
                    if file_name.endswith(".pdf"):
                        with open(os.path.join(folder_db, file_name), "rb") as f:
                            teks_db = baca_pdf(f)
                            teks_db_bersih = bersihkan_teks(teks_db)
                            skor = hitung_kemiripan(teks_uji_bersih, teks_db_bersih)
                            hasil_akhir.append((file_name, skor))
            
            # Tampilkan Hasil
            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Kata Diproses", len(teks_uji.split()))
            
            with col2:
                if hasil_akhir:
                    max_skor = max(hasil_akhir, key=lambda x: x[1])
                    st.metric("Tingkat Kemiripan Tertinggi", f"{max_skor[1]:.2f}%")
                else:
                    st.warning("Database kosong.")

            if hasil_akhir:
                st.write("### Detail Analisis Database:")
                for nama, skor in hasil_akhir:
                    progress_color = "red" if skor > 50 else "green"
                    st.write(f"**{nama}**")
                    st.progress(skor/100)
                    st.write(f"Tingkat kemiripan: {skor:.2f}%")
    else:
        st.error("Silakan masukkan teks atau upload file terlebih dahulu!")

st.caption("Developed by Fazrul | Versi 2.0 (Live Update)")