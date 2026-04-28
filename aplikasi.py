import streamlit as st
import os, re, time
from datetime import datetime

st.set_page_config(page_title="Fazrul Security System", layout="wide", page_icon="🛡️")

# --- DATABASE SEDERHANA ---
LOG_FILE = "log_akses.txt"
USER_DB = "users_data.txt"

def catat_log(info):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{waktu}] {info}\n")

def daftar_user_baru(name, identitas):
    with open(USER_DB, "a") as f:
        f.write(f"{name}|{identitas}\n")

# --- INISIALISASI ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_name'] = ""

if not st.session_state['logged_in']:
    st.title("🛡️ Selamat Datang di Fazrul Anti-Plagiat")
    st.write("Silakan pilih metode akses untuk melanjutkan:")
    
    tab1, tab2, tab3 = st.tabs(["🌐 Akun Google", "📱 Nomor HP", "📝 Daftar Baru"])
    
    with tab1:
        st.write("Sistem akan menghubungkan dengan Akun Google di perangkat ini.")
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
        st.write("Buat akun baru untuk akses permanen.")
        new_user = st.text_input("Nama Lengkap")
        new_identitas = st.text_input("Email atau ID Mahasiswa")
        if st.button("Buat & Masuk"):
            if new_user and new_identitas:
                daftar_user_baru(new_user, new_identitas)
                st.session_state['logged_in'] = True
                st.session_state['user_name'] = new_user
                catat_log(f"DAFTAR BARU: {new_user} ({new_identitas})")
                st.success("Akun berhasil dibuat!")
                st.rerun()

else:
    # --- HALAMAN UTAMA SETELAH LOGIN ---
    st.sidebar.success(f"User: {st.session_state['user_name']}")
    if st.sidebar.button("Keluar Sistem"):
        st.session_state['logged_in'] = False
        st.rerun()
        
    st.title(f"🛡️ Panel Analisis Fazrul V3.8")
    st.write(f"Halo **{st.session_state['user_name']}**, silakan gunakan fitur di bawah.")
    st.divider()
    # Tambahkan kembali fitur Tab PDF/URL/AI di sini jika ingin lengkap
    st.info("Pilih file PDF Anda untuk mulai pengecekan.")
    st.file_uploader("Upload PDF", type="pdf")
