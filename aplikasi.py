import streamlit as st
import time, random
import plotly.graph_objects as go
from datetime import datetime
import pytz

# --- CORE ---
tz_jkt = pytz.timezone('Asia/Jakarta')
st.set_page_config(page_title="FAZRUL ANALYTICS V17.1", layout="wide", page_icon="🛡️")

# --- DATA ---
if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"} 
if 'page' not in st.session_state: st.session_state['page'] = 'welcome'
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

PEMILIK = "Fazrul Alexsander"
IG_URL = "https://www.instagram.com/fazrul_alexsander/?hl=en"
WA_URL = "https://wa.me/6282283311894"
VERSI = "V17.1-SOCIAL-LOCKED"

# --- CSS LUXURY ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0E1117; color: #E0E0E0; }}
    .main-box {{
        background: linear-gradient(165deg, #1A1F26 0%, #090B0E 100%);
        border: 1px solid #30363D; border-top: 5px solid #00F2FF;
        border-radius: 25px; padding: 40px; text-align: center;
        box-shadow: 0 40px 100px rgba(0,0,0,0.8);
    }}
    .avatar-frame {{
        width: 100px; height: 100px; background: #161B22; border: 3px solid #00F2FF;
        border-radius: 50%; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center;
        font-size: 40px; box-shadow: 0 0 30px rgba(0,242,255,0.3);
    }}
    .social-btn {{
        display: inline-block; width: 85%; padding: 12px; border-radius: 50px; 
        text-decoration: none; font-weight: bold; margin-top: 10px; font-size: 13px;
    }}
    .ig-btn {{ background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); color: white !important; }}
    .wa-btn {{ background: #25D366; color: white !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        if st.session_state['page'] == 'welcome':
            st.markdown(f"""<div class='main-box'><div class='avatar-frame'>🛡️</div><h1 style='color:#00F2FF; margin:0;'>{PEMILIK}</h1><p style='color:#8B949E;'>OFFICIAL SECURITY SYSTEM</p><hr style='border-color:#30363D; margin:30px 0;'></div>""", unsafe_allow_html=True)
            if st.button("➕ AJUKAN AKSES OTORITAS", use_container_width=True): st.session_state['page'] = 'daftar'; st.rerun()
            if st.button("🔓 VERIFIKASI LOGIN", use_container_width=True): st.session_state['page'] = 'login'; st.rerun()
            
            # LINK SOSMED
            st.markdown(f"""
                <center style='margin-top:20px;'>
                    <a href='{IG_URL}' target='_blank' class='social-btn ig-btn'>📸 OFFICIAL INSTAGRAM</a>
                    <a href='{WA_URL}' target='_blank' class='social-btn wa-btn'>💬 WHATSAPP ADMIN</a>
                </center>
            """, unsafe_allow_html=True)

        elif st.session_state['page'] == 'daftar':
            st.markdown("<div class='main-box'><h2>REGISTRASI</h2></div>", unsafe_allow_html=True)
            u_n = st.text_input("ID OPERATOR")
            p_n = st.text_input("PASSWORD", type="password")
            if st.button("✅ AKTIFKAN", use_container_width=True):
                if u_n and p_n:
                    st.session_state['db_users'][u_n] = p_n
                    st.success("Tersimpan! Mengarahkan ke Login..."); time.sleep(1.5)
                    st.session_state['page'] = 'login'; st.rerun()
            if st.button("⬅️ KEMBALI"): st.session_state['page'] = 'welcome'; st.rerun()

        elif st.session_state['page'] == 'login':
            st.markdown("<div class='main-box'><h2>OTENTIKASI</h2></div>", unsafe_allow_html=True)
            u_l = st.text_input("ID OPERATOR")
            p_l = st.text_input("PASSWORD", type="password")
            if st.button("🔓 MASUK", use_container_width=True):
                if u_l in st.session_state['db_users'] and st.session_state['db_users'][u_l] == p_l:
                    st.session_state['logged_in'] = True; st.rerun()
                else: st.error("Ditolak!")
            if st.button("⬅️ KEMBALI"): st.session_state['page'] = 'welcome'; st.rerun()

else:
    # --- DASHBOARD ---
    with st.sidebar:
        st.markdown(f"<div class='avatar-frame' style='width:60px; height:60px; font-size:25px;'>🛡️</div><h3 style='text-align:center;'>{PEMILIK}</h3>", unsafe_allow_html=True)
        st.divider()
        st.markdown(f"<center><a href='{IG_URL}' target='_blank' style='color:#E1306C; text-decoration:none;'>📸 Instagram</a> | <a href='{WA_URL}' target='_blank' style='color:#25D366; text-decoration:none;'>💬 WhatsApp</a></center>", unsafe_allow_html=True)
        st.divider()
        if st.button("🚪 LOGOUT", use_container_width=True): st.session_state.clear(); st.rerun()

    st.title("📡 SISTEM ANALISIS PUSAT")
    st.info(f"Selamat Datang, Operator Terverifikasi.")
    # Fitur-fitur dashboard tetap terkunci di sini...

st.markdown(f"<br><center style='opacity:0.2; font-size:10px;'>{PEMILIK.upper()} | {VERSI}</center>", unsafe_allow_html=True)