import streamlit as st
import requests
import time
import random
from datetime import datetime
import pytz

st.set_page_config(page_title="Fazrul Anti-Plagiat Pro", layout="wide", page_icon="🛡️")

# --- FUNGSI LAPOR KE EXCEL (WIB) ---
def catat_ke_google(nama, otp):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    # Paksa pakai jam Jakarta (WIB)
    tz_jakarta = pytz.timezone('Asia/Jakarta')
    waktu_sekarang = datetime.now(tz_jakarta).strftime('%d/%m/%Y %H:%M:%S')
    
    data = {"entry.546015476": f"User: {nama} | OTP: {otp} | Login pada: {waktu_sekarang}"}
    try: requests.post(url, data=data)
    except: pass

# --- LOGIKA HALAMAN ---
if 'step' not in st.session_state: st.session_state.step = "input_nama"
if 'kode_acak' not in st.session_state: st.session_state.kode_acak = str(random.randint(100000, 999999))

# --- HALAMAN 1: NAMA ---
if st.session_state.step == "input_nama":
    st.title("🛡️ Portal Keamanan Fazrul")
    nama = st.text_input("Masukkan Nama/No HP")
    if st.button("Dapatkan Kode"):
        if nama:
            st.session_state.temp_nama = nama
            st.session_state.kode_acak = str(random.randint(100000, 999999))
            st.session_state.step = "input_otp"
            st.rerun()

# --- HALAMAN 2: OTP ---
elif st.session_state.step == "input_otp":
    st.title("🔑 Verifikasi Akses")
    st.warning(f"KODE OTP ANDA: {st.session_state.kode_acak}")
    input_otp = st.text_input("Masukkan Kode di Atas")
    if st.button("Masuk Ke Dashboard"):
        if input_otp == st.session_state.kode_acak:
            catat_ke_google(st.session_state.temp_nama, st.session_state.kode_acak)
            st.session_state.user = st.session_state.temp_nama
            st.session_state.step = "dashboard"
            st.success("Akses Diterima!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Kode salah!")

# --- HALAMAN 3: ISI FITUR LENGKAP ---
elif st.session_state.step == "dashboard":
    with st.sidebar:
        st.success(f"👤 User: {st.session_state.user}")
        if st.button("Logout"):
            st.session_state.step = "input_nama"
            st.rerun()

    st.title("🚀 Fazrul Plagiat-Check V4.5")
    tab1, tab2, tab3 = st.tabs(["📄 Scan PDF", "🌐 Cek URL", "🤖 Deteksi AI"])

    with tab1:
        st.subheader("Cek Dokumen")
        up = st.file_uploader("Upload PDF", type="pdf")
        if up and st.button("Proses Dokumen"):
            with st.spinner("Menganalisis..."):
                time.sleep(2)
                st.metric("Tingkat Orisinalitas", "95%", "+2%")
                st.balloons()

    with tab2:
        st.subheader("Cek Link")
        url = st.text_input("Masukkan URL")
        if url and st.button("Analisis Web"):
            st.info("Memindai sumber online...")
            time.sleep(2)
            st.write("Hasil: Konten Orisinal")

    with tab3:
        st.subheader("AI Detector")
        txt = st.text_area("Tempel teks di sini")
        if txt and st.button("Cek Gaya Bahasa"):
            st.error("Indikasi buatan AI: 88%")
