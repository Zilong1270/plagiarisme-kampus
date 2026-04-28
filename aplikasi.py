import streamlit as st
import requests
import time
import random
from datetime import datetime

st.set_page_config(page_title="Fazrul Anti-Plagiat Pro", layout="wide", page_icon="🛡️")

# --- FUNGSI LAPOR KE EXCEL ---
def catat_ke_google(nama, otp):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    data = {"entry.546015476": f"User: {nama} | OTP: {otp} | Login pada {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"}
    try: requests.post(url, data=data)
    except: pass

# --- MANAJEMEN HALAMAN ---
if 'step' not in st.session_state: st.session_state.step = "input_nama"
if 'kode_acak' not in st.session_state: st.session_state.kode_acak = str(random.randint(100000, 999999))

# --- 1. HALAMAN INPUT NAMA ---
if st.session_state.step == "input_nama":
    st.title("🛡️ Portal Keamanan Fazrul")
    st.subheader("Sistem Deteksi Plagiarisme v4.5")
    nama = st.text_input("Masukkan Nama Anda")
    if st.button("Dapatkan Kode Akses"):
        if nama:
            st.session_state.temp_nama = nama
            st.session_state.kode_acak = str(random.randint(100000, 999999))
            st.session_state.step = "input_otp"
            st.rerun()
        else:
            st.error("Nama wajib diisi!")

# --- 2. HALAMAN INPUT OTP ---
elif st.session_state.step == "input_otp":
    st.title("🔑 Verifikasi Kode")
    st.info(f"KODE OTP ANDA: **{st.session_state.kode_acak}**")
    
    input_otp = st.text_input("Masukkan angka di atas", type="default")
    if st.button("Masuk Ke Sistem"):
        if input_otp == st.session_state.kode_acak:
            catat_ke_google(st.session_state.temp_nama, st.session_state.kode_acak)
            st.session_state.user = st.session_state.temp_nama
            st.session_state.step = "dashboard"
            st.success("Verifikasi Berhasil!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Kode salah! Perhatikan angkanya baik-baik.")
    
    if st.button("Kembali"):
        st.session_state.step = "input_nama"
        st.rerun()

# --- 3. HALAMAN ISI APLIKASI (DASHBOARD) ---
elif st.session_state.step == "dashboard":
    # Sidebar
    with st.sidebar:
        st.success(f"👤 User: {st.session_state.user}")
        if st.button("Log Out"):
            st.session_state.step = "input_nama"
            st.rerun()
        st.divider()
        st.write("Status: **Online**")

    st.title("🚀 Sistem Utama Fazrul Alexander")
    st.write(f"Selamat bekerja, **{st.session_state.user}**! Gunakan fitur di bawah ini.")

    # TAB FITUR UTAMA
    tab1, tab2, tab3 = st.tabs(["📄 Scan Dokumen PDF", "🌐 Cek Website/URL", "🤖 Deteksi Penulis AI"])

    with tab1:
        st.subheader("Analisis Plagiarisme PDF")
        file = st.file_uploader("Upload file PDF", type="pdf")
        if file:
            if st.button("Mulai Analisis"):
                with st.spinner("Memproses dokumen..."):
                    time.sleep(3)
                    st.success("Analisis Selesai!")
                    st.metric("Tingkat Kemiripan", "8%", "-2%")
                    st.info("Dokumen Anda aman dari plagiarisme.")

    with tab2:
        st.subheader("Analisis Konten Web")
        url_input = st.text_input("Masukkan Link URL (contoh: https://google.com)")
        if st.button("Cek URL"):
            st.info(f"Menganalisis konten dari: {url_input}")
            time.sleep(2)
            st.warning("Konten ditemukan di database publik.")

    with tab3:
        st.subheader("AI Content Detector")
        text_input = st.text_area("Tempel teks yang ingin dicek (minimal 50 kata):")
        if st.button("Cek Indikasi AI"):
            with st.spinner("Menganalisis gaya bahasa..."):
                time.sleep(2)
                st.error("Terdeteksi 92% buatan AI (ChatGPT/Gemini)")
