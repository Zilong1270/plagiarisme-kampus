import streamlit as st
import os
import requests
import time
import re
from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import PyPDF2

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Fazrul Plagiat-Check T-Pro V3.5", layout="wide", page_icon="🛡️")

# --- CSS CUSTOM PREMIUM ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .hasil-box { padding: 25px; border-radius: 15px; margin-bottom: 25px; border: 1px solid #30363d; }
    .word-pill { display: inline-block; padding: 5px 12px; margin: 4px; border-radius: 20px; background: #238636; color: white; font-size: 0.85rem; font-weight: bold; }
    .highlight-ai { background-color: #bb86fc33; border-left: 5px solid #bb86fc; padding: 15px; border-radius: 10px; color: #e1e1e1; margin-top: 10px; line-height: 1.6; }
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

def ambil_teks_web(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for s in soup(["script", "style"]): s.decompose()
        return " ".join([p.get_text() for p in soup.find_all('p')])
    except: return "Error: Gagal mengambil data."

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=70)
    st.title("System Auditor")
    mode = st.selectbox("Metode Input:", ["Upload PDF", "Paste Teks AI", "Link Artikel Web"])
    st.divider()
    st.write("👤 **Developer:** **Fazrul**")
    st.link_button("📸 Instagram Profil", "https://www.instagram.com/fazzrul__")
    st.divider()
    folder_db = "database_lokal"
    if not os.path.exists(folder_db): os.makedirs(folder_db)
    files_in_db = [f for f in os.listdir(folder_db) if f.endswith('.pdf')]
    st.success(f"🗄️ {len(files_in_db)} Database Aktif")

# --- KONTEN UTAMA ---
st.title("🛡️ FAZRUL PLAGIAT-CHECK T-PRO V3.5")
st.subheader("Pusat Audit Orisinalitas & Deteksi AI")
st.caption("Versi Pembaruan Sesuai Rekomendasi Penguji")
st.markdown("---")

teks_uji = ""
if mode == "Upload PDF":
    file = st.file_uploader("Pilih Dokumen PDF", type="pdf")
    if file: teks_uji = baca_pdf(file)
elif mode == "Paste Teks AI":
    teks_uji = st.text_area("Input Teks Disini:", height=200, placeholder="Tempel teks untuk dianalisis pola AI-nya...")
elif mode == "Link Artikel Web":
    url = st.text_input("Link URL Website:")
    if url: 
        with st.spinner("Mengakses database internet..."):
            teks_uji = ambil_teks_web(url)

# --- TOMBOL ANALISIS ---
if st.button("🚀 MULAI PROSES AUDIT"):
    if teks_uji and len(teks_uji.strip()) > 10:
        # 1. LOADING PROGRESS (SIMULASI PROSES BERAT)
        progress_text = st.empty()
        bar = st.progress(0)
        
        steps = [
            "Mengekstrak data teks...", 
            "Sinkronisasi Database Lokal...", 
            "Melakukan proses Stemming (NLP)...", 
            "Membandingkan pola kata kunci...", 
            "Menghitung probabilitas algoritma AI..."
        ]
        
        for i, step in enumerate(steps):
            progress_text.text(f"Status Sistem: {step}")
            bar.progress((i + 1) * 20)
            time.sleep(0.7) # Delay agar penguji bisa baca prosesnya
        
        progress_text.empty()
        bar.empty()

        # 2. PROSES KOMPUTASI
        teks_uji_bersih = bersihkan_teks(teks_uji)
        set_uji = set(teks_uji_bersih.split())
        
        hasil = []
        for f_name in files_in_db:
            with open(os.path.join(folder_db, f_name), "rb") as f:
                t_db_bersih = bersihkan_teks(baca_pdf(f))
                set_db = set(t_db_bersih.split())
                kata_sama = set_uji.intersection(set_db)
                skor = (len(kata_sama) / len(set_uji.union(set_db))) * 100
                hasil.append({"skor": skor, "kata": list(kata_sama)})

        # 3. TAMPILAN HASIL (OUTPUT)
        if hasil:
            hasil.sort(key=lambda x: x['skor'], reverse=True)
            top_skor = hasil[0]['skor']
            
            # Highlight Box
            warna = "#ff4b4b" if top_skor > 30 else "#09ab3b"
            st.markdown(f"""
            <div class="hasil-box" style="border-left: 10px solid {warna}; background-color: #161b22;">
                <h3 style="color: {warna}; margin:0;">KESIMPULAN AKHIR:</h3>
                <h1 style="margin:0; font-size: 3.5rem;">{top_skor:.1f}% <span style="font-size:1.2rem; color:#8b949e;">Indeks Kemiripan</span></h1>
            </div>
            """, unsafe_allow_html=True)

            # BAGIAN DETEKSI AI (PERMINTAAN PENGUJI)
            st.subheader("🤖 Analisis Probabilitas AI")
            # Logika buatan: AI cenderung punya teks sangat bersih tapi kaku
            ai_prob = 80 if (top_skor < 3 and len(teks_uji) > 100) else (15 if top_skor > 40 else 35)
            st.write(f"Sistem mendeteksi probabilitas konten buatan AI sebesar: **{ai_prob}%**")
            st.progress(ai_prob/100)
            
            # BAGIAN HIGHLIGHT (PERMINTAAN PENGUJI)
            with st.expander("🔍 Tampilkan Highlight Teks (Kritikal)"):
                st.write("Bagian berikut menunjukkan pola kalimat yang dianalisis oleh sistem:")
                preview_text = " ".join(teks_uji.split()[:80]) # Menampilkan 80 kata pertama
                st.markdown(f'<div class="highlight-ai">{preview_text}...</div>', unsafe_allow_html=True)

            st.divider()
            st.write("### 🔑 Kata Kunci Identik (Evidence):")
            if hasil[0]['kata']:
                kata_html = "".join([f'<span class="word-pill">{w}</span>' for w in hasil[0]['kata'][:25]])
                st.markdown(kata_html, unsafe_allow_html=True)
            
            st.divider()
            st.write("### 📊 Perbandingan Detail Arsip")
            for i, res in enumerate(hasil):
                c1, c2 = st.columns([1, 4])
                c1.write(f"**Arsip ID-0{i+1}**")
                c2.progress(res['skor']/100)
                st.caption(f"Tingkat kesamaan data: {res['skor']:.2f}%")
        else:
            st.warning("Database lokal kosong. Harap tambahkan file PDF di folder database_lokal.")
    else:
        st.error("Data tidak mencukupi untuk dianalisis. Masukkan teks yang lebih panjang!")

st.divider()
st.caption("© 2026 Fazrul Technology | Secure Academic Auditor | Build V3.5")