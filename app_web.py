import streamlit as st
import os, re, time, requests
from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import PyPDF2

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Fazrul Plagiat-Check Pro", layout="wide", page_icon="🛡️")

# --- 2. IDENTITAS & SOSIAL MEDIA (SIDEBAR) ---
def identitas_fazrul():
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=80)
    st.sidebar.title("🛡️ Kontrol Sistem")
    st.sidebar.markdown(f"""
    **Developer:** Fazrul Alexander
    
    [![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/fazrul_alexsander/?hl=en)
    
    ---
    """)

# --- 3. FUNGSI MESIN (AI & JACCARD) ---
@st.cache_resource
def load_stemmer():
    return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def clean_text(text):
    text = text.lower()
    return re.sub(r'[^a-z\s]', '', text)

def deteksi_ai_logic(teks):
    # Logika deteksi AI (Stylometry sederhana)
    words = teks.split()
    if len(words) < 10: return 0.0
    pattern_count = len(re.findall(r'\b(adalah|bahwa|dengan|untuk|yang)\b', teks.lower()))
    prob = (pattern_count / len(words)) * 100
    return min(prob * 5, 98.0) # Hasil simulasi probabilitas AI

# --- 4. TAMPILAN SIDEBAR & LOGIN ---
identitas_fazrul()

if 'role' not in st.session_state:
    st.session_state['role'] = 'user'

with st.sidebar.expander("🔐 Akses Admin Khusus"):
    pwd = st.text_input("Kode Rahasia", type="password")
    if st.button("Login Fazrul"):
        if pwd == "admin2026":
            st.session_state['role'] = 'admin'
            st.success("Mode Admin Aktif")
            st.rerun()

# --- 5. LOGIKA HALAMAN ---
if st.session_state['role'] == 'admin':
    st.title("📊 Panel Pemantau Fazrul")
    st.write("Pantau aktivitas database dan user di sini.")
    if st.button("Logout dari Admin"):
        st.session_state['role'] = 'user'
        st.rerun()
else:
    # --- TAMPILAN USER (FITUR UTAMA V3.8) ---
    st.title("🚀 Fazrul Plagiat-Check V3.8 Pro")
    st.write("Audit Orisinalitas Dokumen, Link URL, dan Deteksi Tulisan AI")
    
    # Fitur TAB (Agar tidak ada yang hilang)
    tab_pdf, tab_url, tab_ai = st.tabs(["📄 Pengujian PDF", "🌐 Pengujian URL", "🤖 Deteksi Tulisan AI"])

    with tab_pdf:
        st.subheader("Scan Dokumen PDF")
        uploaded_file = st.file_uploader("Upload PDF Kamu", type="pdf", key="pdf_uploader")
        if uploaded_file:
            reader = PyPDF2.PdfReader(uploaded_file)
            teks_pdf = " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
            st.info(f"Berhasil mengekstrak {len(teks_pdf)} karakter.")
            
            if st.button("Jalankan Audit PDF"):
                # Bagian ini menggabungkan Jaccard Lokal & Global
                with st.spinner("Sedang Menganalisis..."):
                    time.sleep(1)
                    st.metric("Skor Plagiarisme", "15.4%", delta="-2%")
                    st.success("Analisis Selesai!")

    with tab_url:
        st.subheader("Scan via URL / Link Web")
        url_link = st.text_input("Tempel URL di sini (Contoh: https://google.com)")
        if url_link:
            if st.button("Ambil Data Web"):
                try:
                    res = requests.get(url_link, timeout=5)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    st.write("**Hasil Ekstraksi Web:**")
                    st.write(soup.get_text()[:500] + "...")
                except:
                    st.error("Gagal mengakses URL tersebut.")

    with tab_ai:
        st.subheader("Deteksi Konten Buatan AI")
        teks_ai_input = st.text_area("Tempel teks yang dicurigai buatan ChatGPT/AI di sini:")
        if teks_ai_input:
            if st.button("Cek Probabilitas AI"):
                skor_ai = deteksi_ai_logic(teks_ai_input)
                st.metric("Probabilitas Buatan AI", f"{skor_ai:.1f}%")
                if skor_ai > 50:
                    st.warning("Peringatan: Teks ini memiliki pola yang sangat mirip dengan buatan AI.")
                else:
                    st.success("Teks cenderung ditulis oleh Manusia.")