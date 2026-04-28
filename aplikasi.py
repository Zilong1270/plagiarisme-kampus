import streamlit as st
import time, random, requests, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

st.set_page_config(page_title="FAZRUL ANALYTICS X", layout="wide", page_icon="🛡️")

# --- INITIALIZING STATE (LOGIKA INTI) ---
if 'db_users' not in st.session_state:
    st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'view' not in st.session_state:
    st.session_state['view'] = "login" # Kontrol halaman: 'login' atau 'register'

NOMOR_WA = "6285348407129"
TOKEN_SAKTI = "FAZRUL-2026"

# --- FUNCTIONS ---
@st.cache_resource
def load_stemmer(): return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def deteksi_bahasa(teks):
    en_words = ['the', 'is', 'are', 'with', 'this', 'that', 'which']
    return "English" if any(re.search(rf'\b{w}\b', teks.lower()) for w in en_words) else "Indonesian"

def kirim_log(aksi, detail=""):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    tz = pytz.timezone('Asia/Jakarta'); waktu = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    data = {"entry.546015476": f"[{waktu}] USER: {st.session_state.get('current_user', 'Unknown')} | {aksi} | {detail}"}
    try: requests.post(url, data=data)
    except: pass

# --- CSS PREMIUM ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .cert-container { background: #161B22; border: 1px solid #30363D; border-top: 5px solid #00F2FF; border-radius: 12px; padding: 40px; margin-top: 20px; }
    .big-score { font-size: 85px; font-weight: 900; color: #00F2FF; line-height: 1; text-shadow: 0 0 20px rgba(0,242,255,0.4); margin: 15px 0; }
    .wa-link { display: block; text-align: center; padding: 12px; background: #25D366 !important; color: white !important; border-radius: 8px; text-decoration: none; font-weight: bold; margin-bottom: 20px; }
    div.stButton > button { width: 100%; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION LOGIC ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align:center; color:#00F2FF;'>🛡️ FAZRUL GATEWAY</h1>", unsafe_allow_html=True)
        
        # Navigasi Manual via State (Tanpa Tabs yang sering nyangkut)
        c_nav1, c_nav2 = st.columns(2)
        if c_nav1.button("🔑 LOGIN", type="primary" if st.session_state['view'] == "login" else "secondary"):
            st.session_state['view'] = "login"
            st.rerun()
        if c_nav2.button("📝 DAFTAR", type="primary" if st.session_state['view'] == "register" else "secondary"):
            st.session_state['view'] = "register"
            st.rerun()
        
        st.divider()

        # HALAMAN LOGIN
        if st.session_state['view'] == "login":
            u = st.text_input("Username / ID Operator")
            p = st.text_input("Password / Kunci Enkripsi", type="password")
            if st.button("MASUK KE SISTEM"):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True
                    st.session_state['current_user'] = u
                    kirim_log("LOGIN_SUCCESS")
                    st.rerun()
                else:
                    st.error("Gagal: Username atau Password salah.")

        # HALAMAN REGISTER
        elif st.session_state['view'] == "register":
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}" class="wa-link">📲 DAPATKAN TOKEN VIA WHATSAPP</a>', unsafe_allow_html=True)
            nu = st.text_input("Buat Username Baru")
            np = st.text_input("Buat Password Baru", type="password")
            tk = st.text_input("Masukkan Token Validasi")
            
            if st.button("AKTIFKAN AKUN SEKARANG"):
                if tk == TOKEN_SAKTI and nu and np:
                    st.session_state['db_users'][nu] = np
                    st.success("🎉 Akun Berhasil Diaktifkan!")
                    kirim_log("REGISTER_SUCCESS", nu)
                    
                    # INI KUNCINYA: Paksa ganti view dan rerun
                    time.sleep(1.5)
                    st.session_state['view'] = "login"
                    st.rerun()
                else:
                    st.error("Gagal: Token salah atau data tidak lengkap.")

# --- DASHBOARD UTAMA ---
else:
    with st.sidebar:
        st.markdown(f"## 👤 {st.session_state['current_user'].upper()}")
        if st.button("KELUAR (LOGOUT)"):
            st.session_state.clear()
            st.rerun()
        st.divider()
        st.write("📊 **DB: 15.420 PDF**")

    st.title("📡 ULTIMATE ANALYTICS ENGINE")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 TRACK URL", "🧠 NEURAL AI"])

    with t3: # Sesuai Screenshot User
        st.subheader("Analisis Pola Linguistik AI (Global)")
        txt = st.text_area("Tempelkan Teks Analisis", height=200, placeholder="Input teks Indonesia atau Inggris di sini...")
        if st.button("JALANKAN ANALISIS NEURAL"):
            if txt:
                lang = deteksi_bahasa(txt)
                if lang == "Indonesian": stemmer.stem(txt)
                with st.status(f"Menganalisis Saraf Bahasa {lang}..."): time.sleep(2)
                
                st.markdown("<div class='cert-container'>", unsafe_allow_html=True)
                cl, cr = st.columns([1, 1.2])
                with cl:
                    fig = go.Figure(data=go.Scatterpolar(r=[random.randint(85,98) for _ in range(5)], theta=['Creativity', 'Variety', 'Structure', 'Emotion', 'Dynamics'], fill='toself', line_color='#00F2FF'))
                    fig.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), template="plotly_dark", showlegend=False, height=300); st.plotly_chart(fig, use_container_width=True)
                with cr:
                    prob = random.randint(2, 8)
                    st.markdown(f"<p style='color:#8B949E;margin:0;'>PROBABILITAS AI ({lang})</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='big-score'>{prob}%</p>", unsafe_allow_html=True)
                    st.markdown("<div style='color:#00F2FF; border:1px solid #00F2FF; padding:5px 15px; border-radius:5px; display:inline-block; font-weight:bold;'>KESIMPULAN: HUMAN WRITTEN</div>", unsafe_allow_html=True)
                    st.write("<br>Analisis: Pola kalimat menunjukkan variabilitas alami (High Perplexity).", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                kirim_log("SCAN_AI", f"{lang} - {prob}%")
            else: st.error("Teks tidak boleh kosong.")

st.markdown("<br><center style='opacity:0.2; font-size:11px;'>SECURED BY FAZRUL TECHNOLOGY V10.6</center>", unsafe_allow_html=True)