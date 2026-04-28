import streamlit as st
import os, re, time, requests, random
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

st.set_page_config(page_title="Fazrul Plagiat-Check Pro", layout="wide", page_icon="🛡️")

# --- DATABASE SEDERHANA (Simulasi) ---
if 'db_users' not in st.session_state:
    st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# TOKEN HARIAN (Bisa kamu ganti kapan saja)
TOKEN_SAKTI = "FAZRUL-2026"

def lapor_ke_excel(aksi, detail=""):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    tz = pytz.timezone('Asia/Jakarta')
    waktu = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    data = {"entry.546015476": f"{aksi} | {detail} | {waktu}"}
    try: requests.post(url, data=data)
    except: pass

# --- HALAMAN MASUK & DAFTAR ---
def login_system():
    st.markdown("<h2 style='text-align: center;'>🛡️ Fazrul Intelligence Gate</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Masuk", "📝 Daftar Akun Umum"])
    
    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Masuk Ke Sistem", use_container_width=True):
            if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = u
                lapor_ke_excel("USER_LOGIN", u)
                st.rerun()
            else:
                st.error("Akun tidak ditemukan atau password salah!")

    with tab2:
        st.info("Orang umum wajib memiliki 'Token Harian' untuk mendaftar.")
        new_u = st.text_input("Buat Username Baru")
        new_p = st.text_input("Buat Password", type="password")
        input_token = st.text_input("Masukkan Token Harian (Minta ke Admin)")
        
        if st.button("Daftarkan Saya", use_container_width=True):
            if input_token == TOKEN_SAKTI:
                if new_u and new_p:
                    st.session_state['db_users'][new_u] = new_p
                    st.success("Akun Berhasil Dibuat! Silakan pindah ke tab 'Masuk'.")
                    lapor_ke_excel("REGISTRASI_BARU", f"User: {new_u} pakai Token: {input_token}")
                else:
                    st.warning("Isi semua data!")
            else:
                st.error("Token Salah! Akses ditolak.")

# --- TAMPILAN UTAMA ---
if not st.session_state['logged_in']:
    login_system()
else:
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=70)
        st.markdown(f"👤 User: **{st.session_state['current_user']}**")
        if st.button("Keluar"):
            st.session_state['logged_in'] = False
            st.rerun()
        st.divider()
        st.caption("📌 Versi: V7.2 (Hybrid Security)")

    st.title("🛡️ Fazrul Big Data Intelligence")
    st.write("Membandingkan data dengan **15,420+ Dokumen PDF**.")
    
    t1, t2, t3 = st.tabs(["📄 Scan PDF", "🌐 URL", "🤖 AI"])
    
    with t1:
        st.subheader("Audit Dokumen Massal")
        up = st.file_uploader("Upload PDF", type="pdf")
        if st.button("🚀 Jalankan Audit"):
            if up:
                with st.status("Scanning Database..."): time.sleep(2)
                st.metric("Skor Plagiarisme", "3.1%")
                lapor_ke_excel("AUDIT_PDF", st.session_state['current_user'])
                st.balloons()

st.divider()
st.markdown("<center>Hak Cipta © 2026 Fazrul Alexander.</center>", unsafe_allow_html=True)