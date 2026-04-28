import streamlit as st
import requests
import time
import random
from datetime import datetime

st.set_page_config(page_title="Fazrul Anti-Plagiat Pro", layout="wide")

def catat_ke_google(nama, otp):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    data = {"entry.546015476": f"User: {nama} | OTP: {otp} | Login pada {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"}
    try: requests.post(url, data=data)
    except: pass

if 'step' not in st.session_state: st.session_state.step = "input_nama"
if 'kode_acak' not in st.session_state: st.session_state.kode_acak = str(random.randint(100000, 999999))

# STEP 1: INPUT NAMA
if st.session_state.step == "input_nama":
    st.title("🛡️ Portal Fazrul")
    nama = st.text_input("Masukkan Nama Anda")
    if st.button("Dapatkan OTP"):
        if nama:
            st.session_state.temp_nama = nama
            # Generate kode baru setiap klik
            st.session_state.kode_acak = str(random.randint(100000, 999999))
            st.session_state.step = "input_otp"
            st.rerun()

# STEP 2: INPUT OTP
elif st.session_state.step == "input_otp":
    st.title("🔑 Verifikasi Keamanan")
    st.write(f"Halo **{st.session_state.temp_nama}**.")
    
    # Menampilkan kode yang harus dimasukkan (Simulasi pengiriman kode)
    st.warning(f"KODE VERIFIKASI ANDA: {st.session_state.kode_acak}")
    st.caption("Gunakan kode di atas untuk memverifikasi bahwa Anda bukan robot.")
    
    input_otp = st.text_input("Masukkan Kode OTP di atas", type="default")
    
    if st.button("Konfirmasi Login"):
        if input_otp == st.session_state.kode_acak:
            catat_ke_google(st.session_state.temp_nama, st.session_state.kode_acak)
            st.session_state.user = st.session_state.temp_nama
            st.session_state.step = "dashboard"
            st.success("Akses Diterima!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Kode salah! Pastikan sama dengan angka yang muncul di atas.")
    
    if st.button("Kembali"):
        st.session_state.step = "input_nama"
        st.rerun()

# STEP 3: DASHBOARD
elif st.session_state.step == "dashboard":
    st.title(f"🚀 Dashboard {st.session_state.user}")
    st.write("Selamat bekerja di sistem Fazrul.")
    if st.button("Log Out"):
        st.session_state.step = "input_nama"
        st.rerun()
