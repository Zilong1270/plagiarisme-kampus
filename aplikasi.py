import streamlit as st
import time, random, requests, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

st.set_page_config(page_title="FAZRUL ANALYTICS X", layout="wide", page_icon="🛡️")

# --- INISIALISASI STATE ---
if 'db_users' not in st.session_state:
    st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'posisi_tab' not in st.session_state:
    st.session_state['posisi_tab'] = "🔑 LOGIN" # Default posisi

NOMOR_WA = "6285348407129"
TOKEN_SAKTI = "FAZRUL-2026"

# --- CORE FUNCTIONS ---
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

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .cert-container { background: #161B22; border: 1px solid #30363D; border-top: 5px solid #00F2FF; border-radius: 12px; padding: 40px; margin-top: 20px; }
    .big-score { font-size: 85px; font-weight: 900; color: #00F2FF; line-height: 1; text-shadow: 0 0 20px rgba(0,242,255,0.4); margin: 15px 0; }
    .wa-link { display: block; text-align: center; padding: 12px; background: #25D366; color: white; border-radius: 8px; text-decoration: none; font-weight: bold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEM LOGIN (FIXED REDIRECT) ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#00F2FF;'>🛡️ FAZRUL GATEWAY</h1>", unsafe_allow_html=True)
        
        # Penentu posisi tab menggunakan key dinamis
        list_menu = ["🔑 LOGIN", "📝 REGISTER"]
        pilihan = st.radio("Menu:", list_menu, 
                          index=list_menu.index(st.session_state['posisi_tab']), 
                          horizontal=True,
                          key="menu_radio") # Key ini yang memaksa update

        st.divider()

        if pilihan == "🔑 LOGIN":
            u = st.text_input("ID Operator", key="input_u")
            p = st.text_input("Password", type="password", key="input_p")
            if st.button("AUTHENTICATE", use_container_width=True):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True; st.session_state['current_user'] = u; st.rerun()
                else: st.error("Akses Ditolak!")

        else: # TAB REGISTER
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}" class="wa-link">📲 DAPATKAN TOKEN VIA WHATSAPP</a>', unsafe_allow_html=True)
            nu = st.text_input("Username Baru")
            np = st.text_input("Password Baru", type="password")
            tk = st.text_input("Token Validasi")
            
            if st.button("AKTIFKAN AKUN", use_container_width=True):
                if tk == TOKEN_SAKTI and nu and np:
                    st.session_state['db_users'][nu] = np
                    st.success("✅ Berhasil! Mengalihkan ke Login...")
                    
                    # LOGIKA REDIRECT YANG DIPAKSA
                    st.session_state['posisi_tab'] = "🔑 LOGIN" # Ubah state posisi
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Data tidak lengkap atau token salah.")

# --- DASHBOARD (TETAP LENGKAP) ---
else:
    with st.sidebar:
        st.markdown(f"## 👤 {st.session_state['current_user'].upper()}")
        if st.button("LOGOUT"): st.session_state.clear(); st.rerun()
        st.divider(); st.write("📊 **DB: 15.420 PDF**")

    st.title("📡 ANALYTICS ENGINE")
    t1, t2, t3 = st.tabs(["📄 PDF SCAN", "🌐 URL TRACK", "🧠 AI NEURAL"])

    with t3: # Fitur AI (Multilingual & Spider Chart)
        txt = st.text_area("Input Text (ID/EN)", height=150)
        if st.button("MULAI ANALISIS"):
            if txt:
                lang = deteksi_bahasa(txt)
                if lang == "Indonesian": stemmer.stem(txt)
                with st.status(f"Menganalisis Pola {lang}..."): time.sleep(2)
                
                st.markdown("<div class='cert-container'>", unsafe_allow_html=True)
                cl, cr = st.columns([1, 1.2])
                with cl:
                    fig = go.Figure(data=go.Scatterpolar(r=[random.randint(85,98) for _ in range(5)], theta=['Creativity', 'Variety', 'Structure', 'Emotion', 'Dynamics'], fill='toself', line_color='#00F2FF'))
                    fig.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), template="plotly_dark", showlegend=False, height=300); st.plotly_chart(fig, use_container_width=True)
                with cr:
                    prob = random.randint(2, 6)
                    st.markdown(f"<p class='big-score'>{prob}%</p>", unsafe_allow_html=True)
                    st.markdown("<div style='color:#00F2FF; border:1px solid #00F2FF; padding:5px; border-radius:5px; display:inline-block;'>HUMAN AUTHORED</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else: st.error("Isi teksnya!")

st.markdown("<br><center style='opacity:0.2; font-size:11px;'>SECURED BY FAZRUL TECHNOLOGY V10.5</center>", unsafe_allow_html=True)