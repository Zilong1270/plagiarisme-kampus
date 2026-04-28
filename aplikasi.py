import streamlit as st
import os, re, time
from datetime import datetime

st.set_page_config(page_title="Fazrul Security System", layout="wide", page_icon="🛡️")

# --- FUNGSI CATAT LOG KE DASHBOARD (PRINT) ---
def catat_log(info):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Print ini akan muncul di menu "Manage App -> Logs" di web Streamlit Cloud
    print(f"🕵️ JEJAK DIGITAL: [{waktu}] {info}")
    st.toast(f"Aktivitas tercatat: {info}")

# --- INISIALISASI ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_name'] = ""

if not st.session_state['logged_in']:
    st.title("🛡️ Portal Akses Fazrul")
    st.write("Silakan pilih metode akses untuk melanjutkan:")
    
    tab1, tab2, tab3 = st.tabs(["🌐 Akun Google", "📱 Nomor HP", "📝 Daftar Baru"])
    
    with tab1:
        nama_g = st.text_input("Nama Akun Google", key="g_name")
        if st.button("Masuk dengan Google"):
            if nama_g:
                st.session_state['logged_in'] = True
                st.session_state['user_name'] = nama_g
                catat_log(f"LOGIN GOOGLE: {nama_g}")
                st.rerun()

    with tab2:
        no_hp = st.text_input("Masukkan Nomor HP/WhatsApp", placeholder="08...")
        if st.button("Masuk via OTP SMS"):
            if len(no_hp) > 9:
                st.session_state['logged_in'] = True
                st.session_state['user_name'] = no_hp
                catat_log(f"LOGIN NO-HP: {no_hp}")
                st.rerun()

    with tab3:
        new_user = st.text_input("Nama Lengkap")
        new_identitas = st.text_input("Email/ID")
        if st.button("Buat & Masuk"):
            if new_user and new_identitas:
                st.session_state['logged_in'] = True
                st.session_state['user_name'] = new_user
                catat_log(f"DAFTAR BARU: {new_user} ({new_identitas})")
                st.rerun()

else:
    st.sidebar.success(f"User: {st.session_state['user_name']}")
    if st.sidebar.button("Keluar"):
        catat_log(f"LOGOUT: {st.session_state['user_name']}")
        st.session_state['logged_in'] = False
        st.rerun()
        
    st.title(f"🛡️ Panel Analisis Fazrul V3.8")
    st.write(f"Halo **{st.session_state['user_name']}**, silakan upload file PDF Anda.")
    st.file_uploader("Upload PDF", type="pdf")
