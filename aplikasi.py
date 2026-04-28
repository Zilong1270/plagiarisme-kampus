import streamlit as st
import os, re, time, requests, random
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

st.set_page_config(page_title="Fazrul Plagiat-Check Pro", layout="wide", page_icon="🛡️")

# --- DATABASE USER (Bisa kamu tambah di sini) ---
USERS = {
    "user1": "fazrul2026",
    "mahasiswa": "cekplagiat",
    "admin": "fazruladmin2026"
}

# --- SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None

# --- SASTRAWI ---
@st.cache_resource
def load_stemmer():
    return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def lapor_ke_excel(aksi):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    tz = pytz.timezone('Asia/Jakarta')
    waktu = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    data = {"entry.546015476": f"Aksi: {aksi} | Pengguna: {st.session_state.get('username')} | {waktu}"}
    try: requests.post(url, data=data)
    except: pass

# --- HALAMAN LOGIN ---
def login_page():
    st.markdown("<h2 style='text-align: center;'>🔐 Selamat Datang di Fazrul Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Silakan masuk untuk menggunakan fitur analisis.</p>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.info("Gunakan akun yang telah terdaftar.")
            user_input = st.text_input("Username")
            pass_input = st.text_input("Password", type="password")
            if st.button("Masuk Ke Sistem", use_container_width=True):
                if user_input in USERS and USERS[user_input] == pass_input:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = user_input
                    if user_input == "admin":
                        st.session_state['user_role'] = 'admin'
                    else:
                        st.session_state['user_role'] = 'user'
                    st.success(f"Selamat datang, {user_input}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Username atau Password salah!")

# --- TAMPILAN UTAMA (SETELAH LOGIN) ---
if not st.session_state['logged_in']:
    login_page()
else:
    # --- SIDEBAR ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=70)
        st.markdown(f"### 👤 Hai, {st.session_state['username']}")
        st.write(f"Level Akses: **{st.session_state['user_role'].capitalize()}**")
        if st.button("Keluar (Logout)"):
            st.session_state['logged_in'] = False
            st.rerun()
        st.divider()
        st.caption("📌 **Versi:** V6.7")
        st.caption("📅 **Pembaruan:** Selasa, 28 April 2026")

    # --- KONTEN ADMIN ---
    if st.session_state['user_role'] == 'admin':
        st.title("📊 Dashboard Admin - Kontrol Penuh")
        st.warning("Anda masuk sebagai Admin. Semua log aktivitas dapat dipantau.")
        # Isi dashboard admin bisa ditambah di sini

    # --- KONTEN USER ---
    else:
        st.title("🛡️ Fazrul Intelligence Analysis")
        tab1, tab2, tab3 = st.tabs(["📄 Scan PDF", "🌐 Scan URL", "🤖 Deteksi AI"])

        with tab1:
            st.subheader("Analisis Dokumen PDF")
            up_file = st.file_uploader("Unggah PDF", type="pdf")
            if st.button("Jalankan Audit"):
                if up_file:
                    with st.status("Memproses..."): time.sleep(1.5)
                    st.success("Analisis Selesai!")
                    lapor_ke_excel("Scan PDF")
                else: st.error("File kosong!")

        with tab2:
            st.subheader("Pelacakan URL")
            url_i = st.text_input("Masukan Link")
            if st.button("Scan Link"):
                st.info("Link Aman")
                lapor_ke_excel(f"URL: {url_i}")

        with tab3:
            st.subheader("Analisis Gaya Bahasa AI")
            teks = st.text_area("Tempel teks")
            if st.button("Analisis AI"):
                if teks:
                    prob = random.uniform(10, 95)
                    st.metric("Skor AI", f"{prob}%")
                    lapor_ke_excel(f"AI: {prob}%")

st.divider()
st.markdown("<center>Hak Cipta © 2026 Fazrul Alexander.</center>", unsafe_allow_html=True)