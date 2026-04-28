import streamlit as st
import requests
import time
import random
from datetime import datetime
import pytz # Tambahan library untuk zona waktu

st.set_page_config(page_title="Fazrul Anti-Plagiat Pro", layout="wide", page_icon="🛡️")

# --- FUNGSI LAPOR KE EXCEL (JAM WIB) ---
def catat_ke_google(nama, otp):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    
    # Setting zona waktu ke Jakarta (WIB)
    tz_jakarta = pytz.timezone('Asia/Jakarta')
    waktu_sekarang = datetime.now(tz_jakarta).strftime('%d/%m/%Y %H:%M:%S')
    
    data = {"entry.546015476": f"User: {nama} | OTP: {otp} | Login: {waktu_sekarang}"}
    try: 
        requests.post(url, data=data)
    except: 
        pass

# --- MANAJEMEN HALAMAN ---
if 'step' not in st.session_state: st.session_state.step = "input_nama"
if 'kode_acak' not in st.session_state: st.session_state.kode_acak = str(random.randint(100000, 999999))

if st.session_state.step == "input_nama":
    st.title("🛡️ Portal Fazrul")
    nama = st.text_input("Masukkan Nama Anda")
    if st.button("Dapatkan Kode Akses"):
        if nama:
            st.session_state.temp_nama = nama
            st.session_state.kode_acak = str(random.randint(100000, 999999))
            st.session_state.step = "input_otp"
            st.rerun()

elif st.session_state.step == "input_otp":
    st.title("🔑 Verifikasi Kode")
    st.info(f"KODE OTP ANDA: **{st.session_state.kode_acak}**")
    input_otp = st.text_input("Masukkan angka di atas")
    if st.button("Masuk Ke Sistem"):
        if input_otp == st.session_state.kode_acak:
            catat_ke_google(st.session_state.temp_nama, st.session_state.kode_acak)
            st.session_state.user = st.session_state.temp_nama
            st.session_state.step = "dashboard"
            st.success("Verifikasi Berhasil!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Kode salah!")

elif st.session_state.step == "dashboard":
    st.title(f"🚀 Dashboard {st.session_state.user}")
    st.write("Sistem Pemantauan Aktif.")
    if st.button("Log Out"):
        st.session_state.step = "input_nama"
        st.rerun()
