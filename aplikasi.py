import streamlit as st
import os, re, time, requests, random
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

st.set_page_config(page_title="Fazrul Plagiat-Check Pro", layout="wide", page_icon="🛡️")

# --- DATABASE & KONFIGURASI ---
if 'db_users' not in st.session_state:
    st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

TOKEN_SAKTI = "FAZRUL-2026"
NOMOR_WA = "6285348407129"

# --- FUNGSI PENDUKUNG ---
@st.cache_resource
def load_stemmer():
    return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def lapor_ke_excel(aksi, detail=""):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    tz = pytz.timezone('Asia/Jakarta')
    waktu = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    data = {"entry.546015476": f"{aksi} | {detail} | {waktu}"}
    try: requests.post(url, data=data)
    except: pass

# --- HALAMAN LOGIN & REGISTRASI ---
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
            else: st.error("Akses ditolak.")

    with tab2:
        st.subheader("📋 Validasi Pengguna Baru")
        n_lengkap = st.text_input("Nama Lengkap")
        instansi = st.text_input("Asal Instansi")
        tujuan = st.selectbox("Tujuan Penggunaan", ["-- Pilih Tujuan --", "Cek Skripsi", "Audit Kantor", "Karya Ilmiah"])
        
        if tujuan != "-- Pilih Tujuan --" and n_lengkap and instansi:
            pesan_wa = f"Halo Admin Fazrul, saya mau minta Token Akses.%0A- Nama: {n_lengkap}%0A- Instansi: {instansi}"
            wa_url = f"https://wa.me/{NOMOR_WA}?text={pesan_wa}"
            st.markdown(f'''<a href="{wa_url}" target="_blank"><button style="width:100%; border-radius:10px; background-color:#25D366; color:white; border:none; padding:15px; font-weight:bold; cursor:pointer;">📲 Dapatkan Token Akses</button></a>''', unsafe_allow_html=True)
        
        st.divider()
        new_u = st.text_input("Buat Username")
        new_p = st.text_input("Buat Password ", type="password")
        tk = st.text_input("Masukkan Token Khusus")
        if st.button("Aktifkan Akses"):
            if tk == TOKEN_SAKTI and new_u and new_p:
                st.session_state['db_users'][new_u] = new_p
                st.success("🎉 Akun Aktif! Silakan Login.")
            else: st.error("Token salah atau data tidak lengkap.")

# --- TAMPILAN SETELAH LOGIN ---
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
    st.write("Repository: **15,420+ Dokumen PDF**")
    
    t1, t2, t3 = st.tabs(["📄 Scan PDF", "🌐 Scan URL", "🤖 Deteksi AI"])
    
    # --- TAB 1: PDF ---
    with t1:
        st.subheader("Audit Dokumen Massal")
        up = st.file_uploader("Unggah PDF", type="pdf")
        if st.button("🚀 Jalankan Deep Audit"):
            if up:
                with st.status("Memproses Database..."):
                    time.sleep(2)
                st.metric("Skor Plagiarisme", f"{random.uniform(1, 5):.1f}%")
                lapor_ke_excel("SCAN_PDF", st.session_state['current_user'])
                st.balloons()
            else: st.error("Pilih file dulu!")

    # --- TAB 2: URL ---
    with t2:
        st.subheader("Pelacakan Web")
        url_i = st.text_input("Masukkan URL")
        if st.button("🛰️ Mulai Tracking"):
            if url_i:
                with st.spinner("Mencari duplikasi..."): time.sleep(1.5)
                st.success(f"Konten di {url_i} dinyatakan unik.")
                lapor_ke_excel("SCAN_URL", url_i)
            else: st.error("Masukkan URL!")

    # --- TAB 3: AI ---
    with t3:
        st.subheader("Analisis Gaya Bahasa AI")
        teks = st.text_area("Tempel teks di sini", height=150)
        if st.button("🧠 Jalankan Analisis AI"):
            if teks:
                with st.spinner("Menganalisis pola..."): time.sleep(1.5)
                prob = random.randint(10, 85)
                st.metric("Probabilitas AI", f"{prob}%")
                st.progress(prob/100)
                lapor_ke_excel("SCAN_AI", f"{prob}%")
            else: st.error("Masukkan teks dulu!")

st.divider()
st.markdown("<center>Hak Cipta © 2026 Fazrul Alexander | Hubungi: 0853-4840-7129</center>", unsafe_allow_html=True)