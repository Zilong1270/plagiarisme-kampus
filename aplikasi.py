import streamlit as st
import time, random
import plotly.graph_objects as go
from datetime import datetime
import pytz

# --- CORE SYSTEM ---
tz_jkt = pytz.timezone('Asia/Jakarta')
st.set_page_config(page_title="FAZRUL ANALYTICS V14.0", layout="wide", page_icon="🛡️")

# --- DATABASE & NAVIGATION ---
if 'db_users' not in st.session_state: 
    st.session_state['db_users'] = {"admin": "fazruladmin2026"} 
if 'page' not in st.session_state: 
    st.session_state['page'] = 'welcome'
if 'logged_in' not in st.session_state: 
    st.session_state['logged_in'] = False

# --- IDENTITAS RESMI ---
PEMILIK = "Fazrul Alexsander"
IG_URL = "https://www.instagram.com/fazrul_alexsander/?hl=en"
WA_URL = "https://wa.me/6282283311894" # Nomor WA Resmi Bos Fazrul
VERSI = "V14.0-FINAL-COMM"

# --- CSS LUXURY ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0E1117; color: #E0E0E0; }}
    .main-card {{
        background: linear-gradient(165deg, #1A1F26 0%, #090B0E 100%);
        border: 1px solid #30363D; border-top: 5px solid #00F2FF;
        border-radius: 25px; padding: 50px 40px; text-align: center;
        box-shadow: 0 40px 100px rgba(0,0,0,0.8);
    }}
    .avatar-large {{
        width: 100px; height: 100px; background: #161B22; border: 3px solid #00F2FF;
        border-radius: 50%; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center;
        font-size: 40px; box-shadow: 0 0 30px rgba(0,242,255,0.3);
    }}
    .contact-btn {{
        display: inline-block; padding: 10px 25px; border-radius: 50px; text-decoration: none; 
        font-weight: bold; margin: 10px 5px; font-size: 13px; transition: 0.3s;
    }}
    .ig-theme {{ background: linear-gradient(45deg, #f09433, #dc2743, #bc1888); color: white !important; }}
    .wa-theme {{ background: #25D366; color: white !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 1. HALAMAN WELCOME (AKSES USER) ---
if st.session_state['page'] == 'welcome':
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class='main-card'>
                <div class='avatar-large'>👤</div>
                <h1 style='color:#00F2FF; margin:0;'>{PEMILIK}</h1>
                <p style='color:#8B949E; letter-spacing:2px; font-size:12px;'>OFFICIAL SECURITY DIVISION</p>
                <hr style='border:0; border-top:1px solid #30363D; margin:30px 0;'>
                <p style='color:#B0B0B0; margin-bottom:20px;'>Hubungi Admin untuk Bantuan:</p>
                <a href='{IG_URL}' target='_blank' class='contact-btn ig-theme'>📸 INSTAGRAM</a>
                <a href='{WA_URL}' target='_blank' class='contact-btn wa-theme'>💬 WHATSAPP</a>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📝 DAFTAR AKUN OPERATOR", use_container_width=True):
            st.session_state['page'] = 'daftar'; st.rerun()
        if st.button("🔓 LOGIN SISTEM", use_container_width=True):
            st.session_state['page'] = 'login'; st.rerun()

# --- 2. HALAMAN DAFTAR ---
elif st.session_state['page'] == 'daftar':
    _, col2, _ = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br><h2 style='text-align:center; color:#00F2FF;'>REGISTRASI</h2>", unsafe_allow_html=True)
        new_u = st.text_input("Buat ID")
        new_p = st.text_input("Buat Password", type="password")
        if st.button("✅ DAFTAR SEKARANG", use_container_width=True):
            if new_u and new_p:
                st.session_state['db_users'][new_u] = new_p
                st.success("Berhasil! Mengarahkan ke Halaman Login...")
                time.sleep(2)
                st.session_state['page'] = 'login'; st.rerun()
        st.markdown(f"<center><p style='font-size:12px; color:#586069;'>Kendala daftar? <a href='{WA_URL}' style='color:#25D366;'>Chat WhatsApp</a></p></center>", unsafe_allow_html=True)
        if st.button("⬅️ KEMBALI"): st.session_state['page'] = 'welcome'; st.rerun()

# --- 3. HALAMAN LOGIN ---
elif st.session_state['page'] == 'login' and not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br><h2 style='text-align:center; color:#00F2FF;'>LOGIN</h2>", unsafe_allow_html=True)
        u = st.text_input("ID OPERATOR")
        p = st.text_input("PASSWORD", type="password")
        if st.button("🔓 MASUK", use_container_width=True):
            if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                st.session_state['logged_in'] = True; st.rerun()
            else: st.error("Salah!")
        if st.button("⬅️ KEMBALI"): st.session_state['page'] = 'welcome'; st.rerun()

# --- 4. DASHBOARD ---
elif st.session_state['logged_in']:
    with st.sidebar:
        st.markdown(f"### 🛡️ {PEMILIK}")
        st.markdown(f"<a href='{WA_URL}' target='_blank' class='contact-btn wa-theme' style='display:block; text-align:center;'>💬 Chat Admin</a>", unsafe_allow_html=True)
        st.divider()
        if st.button("🚪 LOGOUT", use_container_width=True): st.session_state.clear(); st.rerun()
    st.title("📡 PUSAT ANALISIS FORENSIK")
    st.success("Sistem Berjalan Normal.")

st.markdown(f"<br><center style='opacity:0.2; font-size:10px;'>{PEMILIK} | {VERSI}</center>", unsafe_allow_html=True)