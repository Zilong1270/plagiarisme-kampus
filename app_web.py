import streamlit as st
import os
import requests
import time
import re
from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import PyPDF2

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Fazrul Plagiat-Check V3.8", layout="wide", page_icon="🛡️")

# --- CSS CUSTOM PREMIUM ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .hasil-box { padding: 25px; border-radius: 15px; margin-bottom: 25px; border: 1px solid #30363d; }
    .word-pill { display: inline-block; padding: 5px 12px; margin: 4px; border-radius: 20px; background: #238636; color: white; font-size: 0.85rem; font-weight: bold; }
    .suggestion-box { background-color: #1e2327; border-left: 5px solid #58a6ff; padding: 15px; border-radius: 8px; margin-top: 10px; }
    .dev-card { background: linear-gradient(135deg, #238636 0%, #2ea043 100%); padding: 15px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI INTI ---
@st.cache_resource
def get_stemmer():
    return StemmerFactory().create_stemmer()

stemmer = get_stemmer()

def bersihkan_teks(teks):
    teks_bersih = re.sub(r'[^a-zA-Z\s]', '', teks)
    return stemmer.stem(teks_bersih.lower())

def baca_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        return " ".join([page.extract_text() for page in reader.pages])
    except: return ""

# --- LOGIKA SARAN PERBAIKAN ---
def beri_saran_perbaikan(kata_plagiat):
    kamus_sinonim = {
        "adalah": "merupakan / ialah",
        "menggunakan": "memanfaatkan / mengimplementasikan",
        "penelitian": "studi / riset akademik",
        "sangat": "amat / luar biasa",
        "penting": "kritikal / krusial",
        "hasil": "output / temuan",
        "melakukan": "menjalankan / melaksanakan",
        "untuk": "guna / demi",
        "metode": "teknik / prosedur"
    }
    saran = []
    for kata in kata_plagiat:
        if kata in kamus_sinonim:
            saran.append(f"Ganti kata **'{kata}'** menjadi **'{kamus_sinonim[kata]}'**")
    return saran

# --- SIDEBAR (IDENTITAS PEMBUAT) ---
with st.sidebar:
    st.markdown('<div class="dev-card"><b>PENGEMBANG UTAMA</b><br>FAZRUL</div>', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=80)
    st.title("Pusat Kendali")
    mode = st.selectbox("Metode Input:", ["Upload PDF", "Paste Teks AI", "Link Artikel Web"])
    
    st.divider()
    st.write("🔗 **Hubungi Saya:**")
    st.link_button("📸 Instagram: @fazzrul__", "https://www.instagram.com/fazzrul__")
    st.write("📧 Email: fazrul@example.com")
    
    st.divider()
    folder_db = "database_lokal"
    if not os.path.exists(folder_db): os.makedirs(folder_db)
    jml_file = len([f for f in os.listdir(folder_db) if f.endswith('.pdf')])
    st.success(f"🗄️ {jml_file} Database Aktif")

# --- KONTEN UTAMA ---
st.title("🛡️ FAZRUL PLAGIAT-CHECK V3.8")
st.subheader("Audit Orisinalitas & Asisten Perbaikan Teks")
st.markdown("---")

teks_uji = ""
if mode == "Upload PDF":
    file = st.file_uploader("Pilih Dokumen PDF", type="pdf")
    if file: teks_uji = baca_pdf(file)
elif mode == "Paste Teks AI":
    teks_uji = st.text_area("Input Teks Disini:", height=200)
elif mode == "Link Artikel Web":
    url = st.text_input("Link URL Website:")
    if url: teks_uji = requests.get(url).text # Simple scrape

# --- TOMBOL ANALISIS ---
if st.button("🚀 MULAI AUDIT & CARI SOLUSI"):
    if teks_uji and len(teks_uji.strip()) > 10:
        with st.status("🔍 Menganalisis Dokumen...", expanded=True) as status:
            time.sleep(1)
            teks_uji_bersih = bersihkan_teks(teks_uji)
            set_uji = set(teks_uji_bersih.split())
            
            hasil = []
            files_in_db = [f for f in os.listdir(folder_db) if f.endswith('.pdf')]
            for f_name in files_in_db:
                with open(os.path.join(folder_db, f_name), "rb") as f:
                    t_db_bersih = bersihkan_teks(baca_pdf(f))
                    set_db = set(t_db_bersih.split())
                    kata_sama = set_uji.intersection(set_db)
                    skor = (len(kata_sama) / len(set_uji.union(set_db))) * 100
                    hasil.append({"skor": skor, "kata": list(kata_sama)})
            status.update(label="Analisis Selesai!", state="complete")

        if hasil:
            hasil.sort(key=lambda x: x['skor'], reverse=True)
            top_skor = hasil[0]['skor']
            kata_plagiat = hasil[0]['kata']
            
            # Box Hasil
            warna = "#ff4b4b" if top_skor > 30 else "#09ab3b"
            st.markdown(f'<div class="hasil-box" style="border-left: 10px solid {warna};"><h1>SKOR: {top_skor:.1f}%</h1></div>', unsafe_allow_html=True)

            # --- FITUR SARAN PERBAIKAN ---
            st.subheader("💡 Saran AI untuk Mengurangi Plagiat")
            daftar_saran = beri_saran_perbaikan(kata_plagiat)
            if daftar_saran:
                for s in daftar_saran[:5]: # Tampilkan 5 saran teratas
                    st.markdown(f'<div class="suggestion-box">✅ {s}</div>', unsafe_allow_html=True)
            else:
                st.write("Tidak ada saran khusus, coba ubah struktur kalimat secara manual.")

            st.divider()
            st.write("### 📊 Perbandingan Detail")
            for i, res in enumerate(hasil):
                st.write(f"Arsip ID-0{i+1} | Kemiripan: {res['skor']:.2f}%")
                st.progress(res['skor']/100)
    else:
        st.error("Masukkan teks yang valid!")

st.caption("Aplikasi ini dikembangkan secara resmi oleh **Fazrul** © 2026")