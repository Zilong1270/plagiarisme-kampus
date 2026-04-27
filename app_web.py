import streamlit as st
import os
import requests
import time
import re
from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import PyPDF2

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Fazrul Plagiat-Check V3.7", layout="wide", page_icon="🛡️")

# --- CSS CUSTOM ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .hasil-box { padding: 25px; border-radius: 15px; margin-bottom: 25px; border: 1px solid #30363d; background-color: #161b22; }
    .ai-rewrite-box { background-color: #1e2327; border: 1px solid #238636; padding: 20px; border-radius: 10px; color: #e1e1e1; margin-top: 15px; }
    .stButton>button { width: 100%; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def get_stemmer():
    return StemmerFactory().create_stemmer()

stemmer = get_stemmer()

def bersihkan_teks(teks):
    teks = re.sub(r'[^a-zA-Z\s]', '', teks)
    return stemmer.stem(teks.lower())

def baca_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        return " ".join([page.extract_text() for page in reader.pages])
    except: return ""

# --- FITUR BARU: AI REWRITE (SIMULASI) ---
def ai_paraphrase(teks):
    # Logika simulasi perbaikan teks untuk mengurangi plagiat
    pengganti = {
        "adalah": "merupakan bentuk dari",
        "menggunakan": "memanfaatkan",
        "sangat": "amat",
        "untuk": "guna",
        "penelitian": "studi akademik",
        "hasil": "output data",
        "penting": "kritikal",
        "dilakukan": "diimplementasikan"
    }
    teks_baru = teks
    for lama, baru in pengganti.items():
        teks_baru = re.sub(rf'\b{lama}\b', baru, teks_baru, flags=re.IGNORECASE)
    return teks_baru

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Auditor Fazrul")
    mode = st.selectbox("Metode Input:", ["Upload PDF", "Paste Teks", "Link Web"])
    st.divider()
    st.write("👤 **Dev:** Fazrul")
    st.link_button("📸 Instagram", "https://www.instagram.com/fazzrul__")
    
    folder_db = "database_lokal"
    if not os.path.exists(folder_db): os.makedirs(folder_db)
    files_in_db = [f for f in os.listdir(folder_db) if f.endswith('.pdf')]
    st.success(f"🗄️ {len(files_in_db)} Dokumen di Server")

# --- KONTEN UTAMA ---
st.title("🛡️ FAZRUL PLAGIAT-CHECK V3.7")
st.subheader("Sistem Audit & Fitur Auto-Rewrite Anti-Plagiat")
st.markdown("---")

teks_uji = ""
if mode == "Upload PDF":
    file = st.file_uploader("Pilih PDF Penguji", type="pdf")
    if file: teks_uji = baca_pdf(file)
elif mode == "Paste Teks":
    teks_uji = st.text_area("Input Teks:", height=200)

if st.button("🚀 ANALISIS DOKUMEN"):
    if teks_uji:
        with st.status("🔍 Melakukan Audit Mendalam...", expanded=True) as status:
            time.sleep(1)
            teks_uji_bersih = bersihkan_teks(teks_uji)
            set_uji = set(teks_uji_bersih.split())
            
            hasil = []
            for f_name in files_in_db:
                with open(os.path.join(folder_db, f_name), "rb") as f:
                    t_db_bersih = bersihkan_teks(baca_pdf(f))
                    set_db = set(t_db_bersih.split())
                    kata_sama = set_uji.intersection(set_db)
                    skor = (len(kata_sama) / len(set_uji.union(set_db))) * 100
                    hasil.append({"skor": skor})
            
            status.update(label="Audit Selesai!", state="complete", expanded=False)

        if hasil:
            hasil.sort(key=lambda x: x['skor'], reverse=True)
            top_skor = hasil[0]['skor']
            warna = "#ff4b4b" if top_skor > 30 else "#09ab3b"
            
            st.markdown(f"""
            <div class="hasil-box" style="border-left: 10px solid {warna};">
                <h3>INDEKS PLAGIAT: {top_skor:.2f}%</h3>
                <p>Status: {"⚠️ PERLU PERBAIKAN" if top_skor > 30 else "✅ AMAN"}</p>
            </div>
            """, unsafe_allow_html=True)

            # --- FITUR UNGGULAN UNTUK PENGUJI ---
            if top_skor > 10:
                st.warning("💡 **Saran AI:** Ditemukan kemiripan. Gunakan fitur perbaikan di bawah untuk menurunkan skor.")
                if st.button("✨ PERBAIKI TEKS OTOMATIS (REDUCE PLAGIARISM)"):
                    with st.spinner("AI sedang menyusun ulang kalimat..."):
                        time.sleep(1.5)
                        teks_diperbaiki = ai_paraphrase(teks_uji)
                        st.success("Teks Berhasil Diperbaiki! Persentase plagiat diprediksi menurun.")
                        st.markdown("### 📝 Hasil Perbaikan AI:")
                        st.markdown(f'<div class="ai-rewrite-box">{teks_diperbaiki}</div>', unsafe_allow_html=True)
                        st.info("Salin teks di atas untuk menggantikan bagian yang plagiat.")
            
            st.divider()
            st.write("### 📊 Detail Server Penguji")
            for i, res in enumerate(hasil):
                st.write(f"Arsip ID-0{i+1} | Kemiripan: {res['skor']:.2f}%")
                st.progress(res['skor']/100)
    else:
        st.error("Data kosong!")

st.caption("© 2026 Fazrul Proyek | V3.7 Anti-Plagiat Engine")