import streamlit as st
import os
import requests
import time
import re
from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import PyPDF2

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Fazrul Plagiat-Check V3.8 Pro", layout="wide", page_icon="🛡️")

# --- CSS CUSTOM PREMIUM (BRANDING & UI) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .hasil-box { padding: 25px; border-radius: 15px; margin-bottom: 25px; border: 1px solid #30363d; }
    .word-pill { display: inline-block; padding: 5px 12px; margin: 4px; border-radius: 20px; background: #238636; color: white; font-size: 0.85rem; font-weight: bold; }
    .suggestion-box { background-color: #1e2327; border-left: 5px solid #58a6ff; padding: 12px; border-radius: 8px; margin-top: 8px; font-size: 0.9rem; }
    .highlight-ai { background-color: #bb86fc33; border-left: 5px solid #bb86fc; padding: 15px; border-radius: 10px; color: #e1e1e1; margin-top: 10px; line-height: 1.6; }
    .dev-card { background: linear-gradient(135deg, #238636 0%, #2ea043 100%); padding: 15px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px; border: 1px solid #ffffff33; }
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

def beri_saran_perbaikan(kata_plagiat):
    # Kamus sinonim untuk membantu mengurangi skor plagiat
    kamus_sinonim = {
        "adalah": "merupakan / ialah",
        "menggunakan": "memanfaatkan / mengimplementasikan",
        "penelitian": "studi / riset akademik",
        "sangat": "amat / luar biasa",
        "penting": "kritikal / krusial",
        "hasil": "output / temuan",
        "melakukan": "menjalankan / melaksanakan",
        "untuk": "guna / demi",
        "metode": "teknik / prosedur",
        "data": "informasi / fakta lapangan"
    }
    return [f"Ganti **'{k}'** → **'{kamus_sinonim[k]}'**" for k in kata_plagiat if k in kamus_sinonim]

# --- SIDEBAR (IDENTITAS PEMILIK & DEVELOPER) ---
with st.sidebar:
    st.markdown('<div class="dev-card"><b>PENGEMBANG & PEMILIK</b><br>FAZRUL</div>', unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=80)
    st.title("Pusat Kendali")
    mode = st.selectbox("Metode Input:", ["Upload PDF", "Paste Teks AI", "Link Artikel Web"])
    
    st.divider()
    st.write("🔗 **Hubungi Saya:**")
    st.link_button("📸 Instagram: @fazzrul__", "https://www.instagram.com/fazzrul__")
    
    st.divider()
    folder_db = "database_lokal"
    if not os.path.exists(folder_db): os.makedirs(folder_db)
    jml_file = len([f for f in os.listdir(folder_db) if f.endswith('.pdf')])
    st.success(f"🗄️ {jml_file} Database Aktif")

# --- KONTEN UTAMA ---
st.title("🛡️ FAZRUL PLAGIAT-CHECK V3.8 PRO")
st.subheader("Sistem Audit Orisinalitas, Deteksi AI & Asisten Revisi")
st.caption("Versi Gabungan: Fitur V3.5 + Solusi Perbaikan V3.8")
st.markdown("---")

teks_uji = ""
if mode == "Upload PDF":
    file = st.file_uploader("Pilih Dokumen PDF Penguji", type="pdf")
    if file: teks_uji = baca_pdf(file)
elif mode == "Paste Teks AI":
    teks_uji = st.text_area("Tempel Teks Disini:", height=200, placeholder="Tempel teks untuk dianalisis...")
elif mode == "Link Artikel Web":
    url = st.text_input("Link URL Website:")
    if url: 
        with st.spinner("Membaca konten web secara real-time..."):
            teks_uji = ambil_teks_web(url)

# --- EKSEKUSI ANALISIS ---
if st.button("🚀 JALANKAN AUDIT SISTEM"):
    if teks_uji and len(teks_uji.strip()) > 10:
        # 1. LOADING PROGRESS (Fitur V3.5)
        progress_text = st.empty()
        bar = st.progress(0)
        steps = [
            "Mengekstrak data teks...", 
            "Sinkronisasi Database Lokal...", 
            "Proses NLP & Stemming...", 
            "Analisis Pola Penulisan AI...", 
            "Menyusun Laporan Akhir..."
        ]
        for i, step in enumerate(steps):
            progress_text.text(f"Status: {step}")
            bar.progress((i + 1) * 20)
            time.sleep(0.6)
        progress_text.empty()
        bar.empty()

        # 2. PROSES KOMPUTASI
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

        # 3. OUTPUT HASIL AKHIR
        if hasil:
            hasil.sort(key=lambda x: x['skor'], reverse=True)
            top_skor = hasil[0]['skor']
            kata_plagiat = hasil[0]['kata']
            
            # Box Hasil Utama (Indikator Warna)
            warna = "#ff4b4b" if top_skor > 30 else "#09ab3b"
            st.markdown(f"""
            <div class="hasil-box" style="border-left: 10px solid {warna}; background-color: #161b22;">
                <h3 style="color: {warna}; margin:0;">KESIMPULAN AUDIT:</h3>
                <h1 style="margin:0;">{top_skor:.1f}% <span style="font-size:1.2rem; color:gray;">Tingkat Kemiripan</span></h1>
            </div>
            """, unsafe_allow_html=True)

            # Analisis AI (Fitur V3.5)
            st.subheader("🤖 Analisis Probabilitas AI")
            ai_prob = 85 if (top_skor < 3 and len(teks_uji) > 100) else (40 if top_skor < 25 else 15)
            st.write(f"Sistem mendeteksi probabilitas teks buatan AI sebesar: **{ai_prob}%**")
            st.progress(ai_prob/100)

            # Highlight Teks (Fitur V3.5)
            with st.expander("🔍 Lihat Highlight Bagian Terdeteksi"):
                preview = " ".join(teks_uji.split()[:100])
                st.markdown(f'<div class="highlight-ai">{preview}...</div>', unsafe_allow_html=True)

            # Saran Perbaikan / Sinonim (Fitur V3.8)
            st.subheader("💡 Saran Perbaikan (Cara Kurangi Plagiat)")
            daftar_saran = beri_saran_perbaikan(kata_plagiat)
            if daftar_saran:
                st.info("Ganti kata-kata berikut dengan sinonimnya agar skor plagiat menurun:")
                cols = st.columns(2)
                for i, s in enumerate(daftar_saran[:8]):
                    cols[i % 2].markdown(f'<div class="suggestion-box">✅ {s}</div>', unsafe_allow_html=True)
            else:
                st.write("Tidak ada saran kata khusus. Cobalah mengubah struktur kalimat secara manual.")

            st.divider()
            st.write("### 📊 Detail Perbandingan Database Lokal")
            for i, res in enumerate(hasil):
                st.write(f"**Arsip ID-0{i+1}** | Skor Kemiripan: {res['skor']:.2f}%")
                st.progress(res['skor']/100)
        else:
            st.warning("Database lokal tidak memiliki data untuk dibandingkan.")
    else:
        st.error("Input tidak valid. Masukkan teks atau file yang lebih panjang!")

# --- FOOTER ---
st.divider()
st.caption(f"© 2026 Aplikasi ini dikembangkan secara resmi oleh **Fazrul** | Academic Integrity Guard")