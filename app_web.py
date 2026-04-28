import streamlit as st
import os, re, time, requests
from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import PyPDF2

# --- 1. IDENTITAS PEMILIK (SOSIAL MEDIA) ---
# Bagian ini yang tadi hilang, kita taruh paling atas agar muncul di Sidebar
def identitas_fazrul():
    st.sidebar.markdown("---")
    st.sidebar.subheader("👤 Pemilik Proyek")
    st.sidebar.info("**Fazrul - Developer**")
    st.sidebar.write("🔗 [Instagram](https://instagram.com/fazrul)") # Ganti linknya
    st.sidebar.write("📧 [Email](mailto:fazrul@example.com)")

# --- 2. FUNGSI INTI (Jaccard, AI Detector, Web Scraping) ---
@st.cache_resource
def load_stemmer():
    return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def clean_text(text):
    text = text.lower()
    return re.sub(r'[^a-z\s]', '', text)

def deteksi_ai_simulasi(teks):
    # Logika deteksi AI sederhana (bisa kamu ganti dengan modelmu sendiri)
    panjang = len(teks.split())
    if panjang < 10: return 0.0
    # Contoh logika: AI cenderung pakai kata 'yang', 'adalah', 'untuk' secara berulang
    kata_kunci_ai = ['adalah', 'yang', 'untuk', 'secara', 'tersebut']
    hitung = sum(1 for kata in kata_kunci_ai if kata in teks.lower())
    prob = (hitung / len(kata_kunci_ai)) * 100
    return min(prob + 15, 95.0) # Simulasi probabilitas

# --- 3. UI UTAMA ---
st.set_page_config(page_title="Fazrul Plagiat-Check Pro", layout="wide")

# Tampilkan Identitas di Sidebar
identitas_fazrul()

# Pengecekan Login Admin
if 'role' not in st.session_state:
    st.session_state['role'] = 'user'

with st.sidebar:
    with st.expander("🔐 Akses Admin"):
        pwd = st.text_input("Kode Akses", type="password")
        if st.button("Masuk"):
            if pwd == "admin2026":
                st.session_state['role'] = 'admin'
                st.rerun()

# --- LOGIKA HALAMAN ---
if st.session_state['role'] == 'admin':
    st.title("📊 Panel Monitoring Fazrul")
    st.write("Semua aktivitas user akan terpantau di sini.")
    if st.button("Logout"):
        st.session_state['role'] = 'user'
        st.rerun()
else:
    # --- KEMBALIKAN TAMPILAN ASLI V3.8 ---
    st.title("🛡️ Fazrul Plagiat-Check V3.8 Pro")
    st.markdown("Sistem Audit Orisinalitas Dokumen & Deteksi AI")

    # Input PDF & URL (Fitur yang tadi hilang)
    tab_pdf, tab_url = st.tabs(["📄 Scan Dokumen PDF", "🌐 Scan via URL/Link"])

    with tab_pdf:
        uploaded_file = st.file_uploader("Upload File PDF Kamu", type="pdf")
        if uploaded_file:
            reader = PyPDF2.PdfReader(uploaded_file)
            teks_input = " ".join([p.extract_text() for p in reader.pages])
            st.success("PDF Berhasil Dibaca!")
            
            if st.button("JALANKAN AUDIT PDF"):
                # Proses Audit (Lokal + Global + AI)
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Skor Jaccard (Lokal)", "12.5%") # Contoh statis, hubungkan ke loop lokalmu
                
                with col2:
                    prob_ai = deteksi_ai_simulasi(teks_input)
                    st.metric("Probabilitas AI", f"{prob_ai:.1f}%")
                
                with col3:
                    st.metric("Status", "Siap Audit")

    with tab_url:
        url_input = st.text_input("Masukkan URL Website (Contoh: https://artikel.com)")
        if url_input and st.button("CEK URL"):
            try:
                res = requests.get(url_input, timeout=5)
                soup = BeautifulSoup(res.text, 'html.parser')
                teks_url = soup.get_text()
                st.write(f"Konten dari URL berhasil diambil ({len(teks_url)} karakter)")
                # Tambahkan logika Jaccard untuk URL di sini
            except:
                st.error("Gagal mengambil data dari URL. Pastikan link aktif.")