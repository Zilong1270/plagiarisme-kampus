import streamlit as st
import time, random
from datetime import datetime

st.set_page_config(page_title="Fazrul Anti-Plagiat", layout="centered")

# --- FUNGSI JEJAK DIGITAL ---
def catat_log(info):
    print(f"🕵️ JEJAK DIGITAL: [{datetime.now().strftime('%H:%M:%S')}] {info}")

if 'step' not in st.session_state: st.session_state.step = "login"

# --- HALAMAN LOGIN ---
if st.session_state.step == "login":
    st.title("🛡️ Portal Keamanan Fazrul")
    identitas = st.text_input("Masukkan Nama atau No. HP")
    
    if st.button("Dapatkan Kode Akses"):
        if identitas:
            st.session_state.user = identitas
            # Kita buat kode OTP simpel: 1227 (Atau bisa random)
            st.session_state.otp = "1227" 
            st.session_state.step = "otp"
            st.rerun()

# --- HALAMAN OTP ---
elif st.session_state.step == "otp":
    st.subheader("🛡️ Verifikasi Perangkat")
    st.write(f"Halo **{st.session_state.user}**, masukkan kode verifikasi.")
    
    # Simulasi: Seolah-olah kode dikirim, padahal kodenya statis (1227)
    st.info("Tips: Masukkan kode rahasia '1227' untuk masuk.")
    
    input_user = st.text_input("Masukkan 4 Digit Kode", type="password")
    
    if st.button("Konfirmasi"):
        if input_user == st.session_state.otp:
            catat_log(f"LOGIN BERHASIL: {st.session_state.user}")
            st.session_state.step = "dashboard"
            st.success("Akses Diterima!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Kode salah! Silakan coba lagi.")

# --- HALAMAN UTAMA ---
elif st.session_state.step == "dashboard":
    st.title(f"🚀 Dashboard {st.session_state.user}")
    st.write("Selamat! Kamu berhasil masuk ke sistem Fazrul.")
    if st.button("Keluar"):
        st.session_state.step = "login"
        st.rerun()
