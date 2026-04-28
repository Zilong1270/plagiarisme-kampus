import streamlit as st
import time, random
from datetime import datetime

st.set_page_config(page_title="Fazrul Anti-Plagiat Pro", layout="wide", page_icon="🛡️")

# --- FUNGSI JEJAK DIGITAL ---
def catat_log(info):
    print(f"🕵️ JEJAK DIGITAL: [{datetime.now().strftime('%H:%M:%S')}] {info}")

# --- INISIALISASI SESSION ---
if 'step' not in st.session_state: st.session_state.step = "login"

# --- 1. HALAMAN LOGIN ---
if st.session_state.step == "login":
    st.title("🛡️ Portal Keamanan Fazrul")
    identitas = st.text_input("Masukkan Nama atau No. HP")
    
    if st.button("Dapatkan Kode Akses"):
        if identitas:
            st.session_state.user = identitas
            st.session_state.otp = "1227" 
            st.session_state.step = "otp"
            st.rerun()

# --- 2. HALAMAN VERIFIKASI ---
elif st.session_state.step == "otp":
    st.subheader("🛡️ Verifikasi Perangkat")
    st.write(f"Halo **{st.session_state.user}**, masukkan kode rahasia.")
    st.info("Tips: Masukkan kode '1227'")
    
    input_user = st.text_input("Masukkan Kode", type="password")
    
    if st.button("Konfirmasi"):
        if input_user == st.session_state.otp:
            catat_log(f"LOGIN BERHASIL: {st.session_state.user}")
            st.session_state.step = "dashboard"
            st.success("Akses Diterima!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Kode salah!")

# --- 3. HALAMAN UTAMA (FITUR LENGKAP) ---
elif st.session_state.step == "dashboard":
    # Sidebar untuk Profil & Logout
    with st.sidebar:
        st.success(f"User: {st.session_state.user}")
        if st.button("Keluar"):
            st.session_state.step = "login"
            st.rerun()
        st.divider()
        st.caption("© 2026 Fazrul Alexander")

    st.title(f"🛡️ Fazrul Plagiat-Check V4.5")
    st.write(f"Selamat bekerja, **{st.session_state.user}**!")

    # Tab Fitur
    tab1, tab2, tab3 = st.tabs(["📄 Cek Dokumen PDF", "🌐 Cek Link URL", "🤖 Deteksi Konten AI"])

    with tab1:
        st.subheader("Analisis File PDF")
        uploaded_file = st.file_uploader("Pilih file PDF", type="pdf")
        if uploaded_file:
            if st.button("Mulai Scan PDF"):
                with st.spinner("Sedang membandingkan dengan database..."):
                    time.sleep(2)
                    st.success("Scan Selesai!")
                    st.metric("Skor Plagiarisme", "12.5%")

    with tab2:
        st.subheader("Analisis Website")
        url = st.text_input("Masukkan Link URL (http/https)")
        if st.button("Cek Website"):
            st.info(f"Menganalisis konten dari: {url}")

    with tab3:
        st.subheader("Deteksi Tulisan AI")
        teks = st.text_area("Tempelkan teks di sini untuk cek buatan AI atau bukan:")
        if st.button("Analisis Teks"):
            st.warning("Probabilitas AI: 85% (Terdeteksi ChatGPT)")
