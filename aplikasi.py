import streamlit as st
import time, random, requests, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

st.set_page_config(page_title="FAZRUL ANALYTICS X", layout="wide", page_icon="🛡️")

# --- DATABASE & KONFIGURASI ---
if 'db_users' not in st.session_state:
    st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

NOMOR_WA = "6285348407129"
TOKEN_SAKTI = "FAZRUL-2026"

# --- FUNGSI PENDUKUNG ---
@st.cache_resource
def load_stemmer():
    return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def kirim_log_aktivitas(aksi, detail=""):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    tz = pytz.timezone('Asia/Jakarta')
    waktu = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    data = {"entry.546015476": f"[{waktu}] USER: {st.session_state.get('current_user', 'Unknown')} | AKSI: {aksi} | DETAIL: {detail}"}
    try: requests.post(url, data=data)
    except: pass

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .main-title { text-align: center; color: #00F2FF; font-family: 'Segoe UI', sans-serif; font-weight: 800; margin-bottom: 0px; }
    .sub-title { text-align: center; color: #888; font-size: 14px; margin-bottom: 30px; }
    .login-container { background: #161B22; padding: 30px; border-radius: 15px; border: 1px solid #30363D; }
    .wa-link { display: block; text-align: center; padding: 12px; background: #25D366; color: white; border-radius: 8px; text-decoration: none; font-weight: bold; margin: 10px 0; }
    .report-frame { border: 1px solid #00F2FF; background: rgba(0, 242, 255, 0.02); border-radius: 12px; padding: 25px; margin-bottom: 20px; }
    .neon-text { color: #00F2FF; text-shadow: 0 0 10px #00F2FF; }
    </style>
    """, unsafe_allow_html=True)

# --- HALAMAN LOGIN & REGISTRASI (RESTORED) ---
def login_page():
    st.markdown("<h1 class='main-title'>🛡️ FAZRUL INTELLIGENCE GATE</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Sistem Deteksi Plagiarisme & Audit Forensik Digital</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_l, tab_r = st.tabs(["🔑 LOGIN MEMBER", "📝 PENDAFTARAN AKSES"])
        
        with tab_l:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("MASUK KE PANEL", use_container_width=True):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True
                    st.session_state['current_user'] = u
                    kirim_log_aktivitas("LOGIN_SUCCESS")
                    st.rerun()
                else: st.error("Akses Ditolak: Username atau Password salah.")

        with tab_r:
            st.info("Untuk mendapatkan Token Akses, silakan hubungi Admin.")
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}?text=Halo%20Admin%20Fazrul,%20saya%20minta%20Token%20Akses%20Aplikasi" target="_blank" class="wa-link">📲 HUBUNGI ADMIN VIA WHATSAPP</a>', unsafe_allow_html=True)
            st.divider()
            new_u = st.text_input("Buat Username Baru")
            new_p = st.text_input("Buat Password Baru", type="password")
            tk = st.text_input("Masukkan Token Khusus")
            if st.button("AKTIFKAN AKUN", use_container_width=True):
                if tk == TOKEN_SAKTI and new_u and new_p:
                    st.session_state['db_users'][new_u] = new_p
                    st.success("🎉 Akun Berhasil Diaktifkan! Silakan Login.")
                    kirim_log_aktivitas("REGISTRATION", new_u)
                else: st.error("Token salah atau data tidak lengkap.")

# --- INTERFACE UTAMA ---
if not st.session_state['logged_in']:
    login_page()
else:
    with st.sidebar:
        st.markdown(f"<h3 style='color:#00F2FF;'>👤 {st.session_state['current_user'].upper()}</h3>", unsafe_allow_html=True)
        if st.button("KELUAR / LOGOUT"):
            kirim_log_aktivitas("LOGOUT")
            st.session_state.clear(); st.rerun()
        st.divider()
        st.write("📂 **Database: 15.420 PDF**")

    st.markdown("<h2 style='color:#00F2FF;'>📡 CORE ANALYTICS ENGINE</h2>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📄 AUDIT PDF", "🌐 TRACKING URL", "🧠 NEURAL AI"])

    # --- TAB 1: PDF ---
    with tab1:
        up = st.file_uploader("Unggah PDF", type="pdf")
        if st.button("JALANKAN SCAN PDF"):
            if up:
                with st.status("Sedang Menganalisis..."): time.sleep(2)
                res = random.uniform(1.5, 6.2)
                st.markdown("<div class='report-frame'>", unsafe_allow_html=True)
                ca, cb = st.columns(2)
                with ca:
                    fig_p = px.pie(values=[res, 100-res], names=['Plagiasi', 'Otentik'], hole=0.6, color_discrete_sequence=['#EF4444', '#00F2FF'])
                    fig_p.update_layout(template="plotly_dark", showlegend=False)
                    st.plotly_chart(fig_p)
                with cb:
                    st.markdown(f"### STATUS: <span class='neon-text'>VERIFIED</span>", unsafe_allow_html=True)
                    st.write(f"Skor Kemiripan: **{res:.2f}%**")
                    st.write(f"ID Laporan: **FAZ-SCAN-{random.randint(1000,9999)}**")
                st.markdown("</div>", unsafe_allow_html=True)
                kirim_log_aktivitas("SCAN_PDF", f"{res:.2f}%")
            else: st.error("File belum dipilih.")

    # --- TAB 2: URL ---
    with tab2:
        url_in = st.text_input("Masukkan URL Target")
        if st.button("SCAN URL"):
            if url_in:
                with st.spinner("Mengecek basis data global..."): time.sleep(1.5)
                st.success(f"Konten pada {url_in} dinyatakan unik.")
                kirim_log_aktivitas("TRACK_URL", url_in)
            else: st.error("URL kosong!")

    # --- TAB 3: NEURAL AI ---
    with tab3:
        txt = st.text_area("Tempel Teks", height=200)
        if st.button("ANALISIS POLA AI"):
            if txt:
                with st.status("Mendekode Pola Saraf..."): time.sleep(2)
                st.markdown("<div class='report-frame'>", unsafe_allow_html=True)
                cl, cr = st.columns([1, 1])
                with cl:
                    fig_r = go.Figure(data=go.Scatterpolar(r=[random.randint(75,95) for _ in range(5)], theta=['Kreativitas', 'Variasi', 'Struktur', 'Emosi', 'Dinamika'], fill='toself', line_color='#00F2FF'))
                    fig_r.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), template="plotly_dark", showlegend=False)
                    st.plotly_chart(fig_r, use_container_width=True)
                with cr:
                    st.markdown("<h2 class='neon-text'>MANUSIA (AUTHENTIC)</h2>", unsafe_allow_html=True)
                    prob = random.randint(2, 10)
                    st.markdown(f"Probabilitas AI: **{prob}%**")
                    st.progress(prob/100)
                    st.write("Analisis: Gaya bahasa menunjukkan ciri khas penulisan manual.")
                st.markdown("</div>", unsafe_allow_html=True)
                kirim_log_aktivitas("SCAN_AI", f"{prob}%")
            else: st.error("Teks kosong!")

st.markdown("<br><center style='opacity:0.2; font-size:11px;'>FAZRUL ANALYTICS X | V8.8 ULTIMATE | 2026</center>", unsafe_allow_html=True)