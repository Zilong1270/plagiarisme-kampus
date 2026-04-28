import streamlit as st
import time, random
from datetime import datetime
import pytz

# --- 1. SETTING WAKTU & IDENTITAS HISTORIS ---
tz_jkt = pytz.timezone('Asia/Jakarta')
now = datetime.now(tz_jkt)

TGL_BUAT = "27 April 2026"  # DIKUNCI SESUAI INSTRUKSI BOS FAZRUL
PEMILIK = "Fazrul Alexsander"
WA_URL = "https://wa.me/6282283311894"
IG_URL = "https://www.instagram.com/fazrul_alexsander/?hl=en"
VERSI = "V19.8-ORIGIN-FIX"

st.set_page_config(page_title=f"{PEMILIK} ANALYTICS", layout="wide", page_icon="🛡️")

# --- 2. DATABASE & SESSION ---
if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"} 
if 'page' not in st.session_state: st.session_state['page'] = 'welcome'
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

# --- 3. CSS MEWAH ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0E1117; color: #E0E0E0; }}
    .main-box {{
        background: linear-gradient(165deg, #1A1F26 0%, #090B0E 100%);
        border: 1px solid #30363D; border-top: 5px solid #00F2FF;
        border-radius: 25px; padding: 40px; text-align: center;
        box-shadow: 0 20px 60px rgba(0,0,0,0.7);
    }}
    .footer-box {{
        text-align: center; font-size: 11px; color: #484F58; margin-top: 40px;
        border-top: 1px solid #1A1F26; padding-top: 20px; line-height: 1.6;
    }}
    .social-btn {{
        display: inline-block; width: 100%; padding: 12px; border-radius: 50px; 
        text-decoration: none; font-weight: bold; margin-bottom: 10px; font-size: 13px; text-align: center;
    }}
    .ig-btn {{ background: linear-gradient(45deg, #f09433, #dc2743, #bc1888); color: white !important; }}
    .wa-btn {{ background: #25D366; color: white !important; }}
    .est-badge {{
        background: rgba(0, 242, 255, 0.1); color: #00F2FF; padding: 4px 12px;
        border-radius: 5px; font-size: 10px; font-weight: bold; letter-spacing: 1px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.session_state['page'] == 'welcome':
            st.markdown(f"""
                <div class='main-box'>
                    <div style='font-size:40px; margin-bottom:10px;'>🛡️</div>
                    <h1 style='color:#00F2FF; margin:0;'>{PEMILIK}</h1>
                    <p style='color:#8B949E; margin-bottom:15px;'>ELITE ANALYTICS SYSTEM</p>
                    <span class='est-badge'>ESTABLISHED: {TGL_BUAT.upper()}</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ DAFTAR AKSES BARU", use_container_width=True): st.session_state['page'] = 'daftar'; st.rerun()
            if st.button("🔓 LOGIN OPERATOR", use_container_width=True): st.session_state['page'] = 'login'; st.rerun()
            
            st.markdown(f"<a href='{IG_URL}' target='_blank' class='social-btn ig-btn'>📸 OFFICIAL INSTAGRAM</a><a href='{WA_URL}' target='_blank' class='social-btn wa-btn'>💬 WHATSAPP ADMIN</a>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='footer-box'>
                    © {now.year} {PEMILIK.upper()} • ENCRYPTED SYSTEM<br>
                    Creation Date: <b>{TGL_BUAT}</b> | Version: {VERSI}<br>
                    <span style='color:#58A6FF;'>Property of Fazrul Alexander Security Division</span>
                </div>
            """, unsafe_allow_html=True)

        elif st.session_state['page'] == 'daftar':
            st.markdown("<div class='main-box'><h2>REGISTRASI</h2></div>", unsafe_allow_html=True)
            un = st.text_input("SET ID OPERATOR"); pn = st.text_input("SET PASSWORD", type="password")
            if st.button("✅ AKTIFKAN AKSES"): 
                st.session_state['db_users'][un] = pn; st.success("Data Tersimpan!"); time.sleep(1); st.session_state['page'] = 'login'; st.rerun()
            if st.button("⬅️ KEMBALI"): st.session_state['page'] = 'welcome'; st.rerun()

        elif st.session_state['page'] == 'login':
            st.markdown("<div class='main-box'><h2>LOGIN SYSTEM</h2></div>", unsafe_allow_html=True)
            ul = st.text_input("ID OPERATOR"); pl = st.text_input("PASSWORD", type="password")
            if st.button("🔓 MASUK"):
                if ul in st.session_state['db_users'] and st.session_state['db_users'][ul] == pl:
                    st.session_state['logged_in'] = True; st.rerun()
                else: st.error("Akses Ditolak! Cek ID/Pass.")
            if st.button("⬅️ KEMBALI"): st.session_state['page'] = 'welcome'; st.rerun()

else:
    # --- DASHBOARD CONTENT ---
    with st.sidebar:
        st.markdown(f"### 🛡️ {PEMILIK}")
        st.markdown(f"<p style='font-size:11px;'>System Created:<br><b>{TGL_BUAT}</b></p>", unsafe_allow_html=True)
        st.divider()
        if st.button("🚪 KELUAR", use_container_width=True): st.session_state.clear(); st.rerun()

    st.title("📡 CORE INTELLIGENCE CENTER")
    st.info(f"Sistem Berjalan Sejak: {TGL_BUAT}")
    # ... Fitur PDF, Neural AI, dll ...

st.markdown(f"<br><center style='opacity:0.2; font-size:10px;'>{PEMILIK.upper()} | SINCE {TGL_BUAT}</center>", unsafe_allow_html=True)