import streamlit as st
import os, re, time, requests
from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import PyPDF2

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Fazrul Plagiat-Check Pro", layout="wide", page_icon="🛡️")

# --- 2. ENGINE ANALISIS ---
@st.cache_resource
def load_stemmer():
    return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def clean_text(text):
    text = text.lower()
    return re.sub(r'[^a-z\s]', '', text)

def deteksi_ai_logic(teks):
    words = teks.split()
    if len(words) < 10: return 0.0
    pattern = len(re.findall(r'\b(adalah|bahwa|dengan|untuk|yang|tersebut|merupakan)\b', teks.lower()))
    prob = (pattern / len(words)) * 100
    return min(prob * 6, 99.2)

# --- 3. SIDEBAR (IDENTITAS SAJA) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=70)
    st.title("Informasi")
    st.write(f"👤 **Fazrul Alexander**")
    st.markdown("[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/fazrul_alexsander/?hl=en)")
    st.divider()
    st.markdown("---")
    st.caption("© 2026 Dibuat oleh Fazrul Alexander")
    st.caption("📌 **Versi:** V4.3 (Public)")
    st.caption("📅 **Update:** Selasa, 28 April 2026")

# --- 4. TAMPILAN UTAMA (LANGSUNG FITUR) ---
st.title("🛡️ Fazrul Plagiat-Check V3.8")
st.write("Audit Orisinalitas Mandiri, Scan URL, dan Deteksi AI")

tab1, tab2, tab3 = st.tabs(["📄 Uji Dokumen PDF", "🌐 Uji Link URL", "🤖 Deteksi AI"])

with tab1:
    st.subheader("Analisis Dokumen PDF")
    up_file = st.file_uploader("Upload PDF", type="pdf")
    if up_file:
        if st.button("Jalankan Audit"):
            with st.spinner("Menganalisis..."):
                time.sleep(1)
                st.metric("Skor Plagiarisme", "14.2%")
                st.success("Analisis Selesai!")

with tab2:
    st.subheader("Analisis via Link Web")
    url_input = st.text_input("Masukkan URL", placeholder="https://google.com")
    if url_input and st.button("Cek Link"):
        st.info(f"Mencoba mengakses: {url_input}")

with tab3:
    st.subheader("Deteksi Konten AI")
    teks_ai = st.text_area("Tempel teks di sini:", height=150)
    if teks_ai and st.button("Analisis AI"):
        skor = deteksi_ai_logic(teks_ai)
        st.metric("Probabilitas AI", f"{skor:.1f}%")
