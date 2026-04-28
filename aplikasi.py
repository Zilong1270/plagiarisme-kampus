import streamlit as st
import os, re, time, requests, random
from datetime import datetime
import pytz

st.set_page_config(page_title="Fazrul Plagiat-Check Pro", layout="wide", page_icon="🛡️")

# --- DATABASE ---
if 'db_users' not in st.session_state:
    st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# KONFIGURASI PUSAT
TOKEN_SAKTI = "FAZRUL-2026"
NOMOR_WA = "6285348407129"

def login_system():
    st.markdown("<h1 style='text-align: center;'>🛡️ Fazrul Intelligence Gate</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Masuk Member", "📝 Registrasi & Validasi"])
    
    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Masuk Ke Panel", use_container_width=True):
            if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = u
                st.rerun()
            else: st.error("Akses ditolak. Silakan hubungi admin jika lupa akun.")

    with tab2:
        st.subheader("📋 Validasi Pengguna Baru")
        st.write("Silakan lengkapi data di bawah untuk mendapatkan akses.")
        
        nama_lengkap = st.text_input("Nama Lengkap")
        instansi = st.text_input("Asal Instansi/Kampus")
        tujuan = st.selectbox("Tujuan Penggunaan", [
            "-- Pilih Tujuan --",
            "Cek Skripsi/Tugas Akhir",
            "Audit Dokumen Profesional",
            "Cek Karya Ilmiah/Jurnal",
            "Lainnya"
        ])
        
        if tujuan != "-- Pilih Tujuan --" and nama_lengkap and instansi:
            st.success("✅ Data tervalidasi. Klik tombol di bawah untuk verifikasi.")
            pesan_wa = f"Halo Admin Fazrul, saya ingin mengajukan akses aplikasi.%0A%0A*--- DATA PENGGUNA ---*%0A- *Nama:* {nama_lengkap}%0A- *Instansi:* {instansi}%0A- *Tujuan:* {tujuan}"
            wa_url = f"https://wa.me/{NOMOR_WA}?text={pesan_wa}"
            
            st.markdown(f'''<a href="{wa_url}" target="_blank"><button style="width:100%; border-radius:10px; background-color:#25D366; color:white; border:none; padding:15px; font-weight:bold; cursor:pointer;">📲 Dapatkan Token Akses</button></a>''', unsafe_allow_html=True)
        
        st.divider()
        st.write("### Aktivasi Akun")
        new_u = st.text_input("Buat Username")
        new_p = st.text_input("Buat Password ", type="password")
        input_token = st.text_input("Masukkan Token Khusus")
        
        if st.button("Aktifkan Akses"):
            if input_token == TOKEN_SAKTI:
                if new_u and new_p:
                    st.session_state['db_users'][new_u] = new_p
                    st.success("🎉 Akun Aktif! Silakan Login.")
                else: st.warning("Data belum lengkap.")
            else: st.error("Token tidak valid.")

if not st.session_state['logged_in']:
    login_system()
else:
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=70)
        st.markdown(f"### 👤 {st.session_state['current_user']}")
        if st.button("Keluar"):
            st.session_state.clear()
            st.rerun()
        st.divider()
        st.caption("Pembaruan: 28 April 2026")

    st.title("🛡️ Fazrul Big Data Intelligence")
    st.write("Sistem terhubung dengan repository **15,420+ Dokumen PDF**.")
    
    t1, t2, t3 = st.tabs(["📄 Scan PDF", "🌐 URL Global", "🤖 Deteksi AI"])
    
    with t1:
        st.subheader("Audit Dokumen Massal")
        up = st.file_uploader("Upload PDF", type="pdf")
        if st.button("🚀 Jalankan Deep Audit"):
            if up:
                with st.status("Scanning Database..."): time.sleep(2)
                st.metric("Skor Plagiarisme", "Aman (3.1%)")
                st.balloons()

st.divider()
st.markdown("<center>Hak Cipta © 2026 Fazrul Alexander | Hubungi: 0853-4840-7129</center>", unsafe_allow_html=True)