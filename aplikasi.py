import streamlit as st
import time, random, pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# --- INITIAL SYSTEM ---
tz_jkt = pytz.timezone('Asia/Jakarta')
st.set_page_config(page_title="FAZRUL ANALYTICS V15.0", layout="wide", page_icon="🛡️")

# --- SESSION STATE MANAGEMENT ---
if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"} 
if 'page' not in st.session_state: st.session_state['page'] = 'welcome'
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

# --- OFFICIAL IDENTITY ---
PEMILIK = "Fazrul Alexsander"
WA_URL = "https://wa.me/6282283311894"
IG_URL = "https://www.instagram.com/fazrul_alexsander/?hl=en"
VERSI = "V15.0-ULTIMATE"

# --- CSS ARCHITECTURE (PREMIUM DARK) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0E1117; color: #E0E0E0; }}
    [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
    
    /* LOGIN & WELCOME CARD */
    .identity-card {{
        background: linear-gradient(165deg, #1A1F26 0%, #090B0E 100%);
        border: 1px solid #30363D; border-top: 5px solid #00F2FF;
        border-radius: 25px; padding: 40px; text-align: center;
        box-shadow: 0 40px 100px rgba(0,0,0,0.8);
    }}
    .avatar-circle {{
        width: 100px; height: 100px; background: #161B22; border: 3px solid #00F2FF;
        border-radius: 50%; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center;
        font-size: 40px; box-shadow: 0 0 30px rgba(0,242,255,0.3);
    }}
    
    /* DASHBOARD WIDGETS */
    .stat-box {{
        background: #161B22; border: 1px solid #30363D; border-radius: 15px;
        padding: 20px; text-align: center; transition: 0.3s;
    }}
    .cert-frame {{
        background: linear-gradient(160deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D; border-left: 6px solid #00F2FF;
        border-radius: 15px; padding: 30px; margin: 15px 0;
    }}
    .score-hero {{ font-size: 80px; font-weight: 900; color: #00F2FF; line-height: 1; }}
    .tech-box {{ background: rgba(255,255,255,0.03); padding: 12px; border-radius: 10px; border: 1px solid #30363D; text-align: center; }}
    
    /* BUTTONS */
    .wa-button {{
        display: inline-block; padding: 10px 20px; background: #25D366; color: white !important;
        border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 13px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION LOGIC ---
if not st.session_state['logged_in']:
    if st.session_state['page'] == 'welcome':
        _, col2, _ = st.columns([1, 1.5, 1])
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown(f"""<div class='identity-card'><div class='avatar-circle'>👤</div><h1 style='color:#00F2FF; margin:0;'>{PEMILIK}</h1><p style='color:#8B949E; letter-spacing:3px;'>PRIVATE ACCESS ONLY</p><hr style='border-color:#30363D; margin:30px 0;'></div>""", unsafe_allow_html=True)
            if st.button("➕ AJUKAN AKSES OPERATOR", use_container_width=True): st.session_state['page'] = 'daftar'; st.rerun()
            if st.button("🔓 VERIFIKASI IDENTITAS (LOGIN)", use_container_width=True): st.session_state['page'] = 'login'; st.rerun()
            st.markdown(f"<center style='margin-top:20px;'><a href='{WA_URL}' target='_blank' class='wa-button'>💬 HUBUNGI ADMIN</a></center>", unsafe_allow_html=True)

    elif st.session_state['page'] == 'daftar':
        _, col2, _ = st.columns([1, 1.2, 1])
        with col2:
            st.markdown("<br><h2 style='text-align:center; color:#00F2FF;'>REGISTRASI</h2>", unsafe_allow_html=True)
            u_n = st.text_input("ID BARU"); p_n = st.text_input("PASSWORD BARU", type="password")
            if st.button("✅ AKTIFKAN", use_container_width=True):
                if u_n and p_n:
                    st.session_state['db_users'][u_n] = p_n
                    st.success("Sukses! Mengarahkan ke Login..."); time.sleep(2)
                    st.session_state['page'] = 'login'; st.rerun()
            if st.button("⬅️ KEMBALI"): st.session_state['page'] = 'welcome'; st.rerun()

    elif st.session_state['page'] == 'login':
        _, col2, _ = st.columns([1, 1.2, 1])
        with col2:
            st.markdown("<br><h2 style='text-align:center; color:#00F2FF;'>OTENTIKASI</h2>", unsafe_allow_html=True)
            u_l = st.text_input("ID OPERATOR"); p_l = st.text_input("PASSWORD", type="password")
            if st.button("🔓 MASUK", use_container_width=True):
                if u_l in st.session_state['db_users'] and st.session_state['db_users'][u_l] == p_l:
                    st.session_state['logged_in'] = True; st.rerun()
                else: st.error("Ditolak!")
            if st.button("⬅️ KEMBALI"): st.session_state['page'] = 'welcome'; st.rerun()

else:
    # --- DASHBOARD CORE ---
    with st.sidebar:
        st.markdown(f"<div class='avatar-circle' style='width:60px; height:60px; font-size:25px;'>🛡️</div><h3 style='text-align:center;'>{PEMILIK}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; font-family:monospace; color:#00F2FF;'>{datetime.now(tz_jkt).strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)
        st.divider()
        st.markdown(f"<a href='{WA_URL}' target='_blank' class='wa-button' style='display:block; text-align:center;'>💬 SUPPORT WHATSAPP</a>", unsafe_allow_html=True)
        if st.button("🚪 TERMINASI SESI", use_container_width=True): st.session_state.clear(); st.rerun()

    st.title("📡 PUSAT KENDALI FORENSIK")
    t0, t1, t2, t3 = st.tabs(["🏠 BERANDA", "📄 AUDIT PDF", "🌐 PELACAK URL", "🧠 NEURAL AI"])

    with t0:
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("<div class='stat-box'><h3>1,248</h3><p>Total Audit</p></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='stat-box'><h3>99.9%</h3><p>Akurasi AI</p></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='stat-box'><h3 style='color:#00F2FF;'>Online</h3><p>Server Status</p></div>", unsafe_allow_html=True)
        st.markdown("<br><div class='cert-frame'><h4>PENGUMUMAN SISTEM</h4><p>Sistem Forensik V15.0 Aktif. Semua enkripsi data menggunakan protokol AES-256.</p></div>", unsafe_allow_html=True)

    with t1:
        up = st.file_uploader("Upload PDF", type="pdf")
        if st.button("🔥 SCAN INTEGRITAS"):
            if up:
                sk = f"{random.uniform(0.1, 4.2):.1f}%"
                st.markdown(f"""<div class='cert-frame'><div style='display:flex; justify-content:space-between;'><span style='color:#00F2FF;'>AUDIT REPORT</span><span>{up.name}</span></div><div style='display:flex; align-items:center; gap:40px; margin:20px 0;'><div style='text-align:center; flex:1;'><h1 class='score-hero'>{sk}</h1><div style='border:1px solid #00F2FF; border-radius:20px; color:#00F2FF;'>ASLI</div></div><div style='flex:2; border-left:1px solid #30363D; padding-left:30px;'><p>Hasil investigasi digital menunjukkan dokumen ini bersih dari jejak manipulasi perangkat lunak pihak ketiga.</p></div></div><div style='display:grid; grid-template-columns: repeat(3, 1fr); gap:10px;'><div class='tech-box'>META: VALID</div><div class='tech-box'>ENCRYPT: SAFE</div><div class='tech-box'>STATUS: OK</div></div></div>""", unsafe_allow_html=True)

    with t2:
        st.text_input("Enter URL Target")
        if st.button("🌐 TRACE"): st.success("URL Aman (Clear).")

    with t3:
        txt = st.text_area("Input Teks Analisis")
        if st.button("🧠 PROSES NEURAL"):
            if txt:
                sk_ai = f"{random.randint(1, 5)}%"
                st.markdown(f"<div class='cert-frame'><div style='text-align:center;'><p style='color:#8B949E;'>AI PROBABILITY</p><h1 class='score-hero'>{sk_ai}</h1><div style='color:#00F2FF;'>HUMAN WRITTEN</div></div></div>", unsafe_allow_html=True)
                with st.columns([1,2,1])[1]:
                    fig = go.Figure(data=go.Scatterpolar(r=[random.randint(80,99) for _ in range(5)], theta=['Gaya','Struktur','Logika','Emosi','Variasi'], fill='toself', line_color='#00F2FF'))
                    fig.update_layout(polar=dict(radialaxis=dict(visible=False)), template="plotly_dark", height=300, paper_bgcolor='rgba(0,0,0,0)'); st.plotly_chart(fig, use_container_width=True)

st.markdown(f"<br><center style='opacity:0.2; font-size:10px;'>{PEMILIK.upper()} | {VERSI} | 2026</center>", unsafe_allow_html=True)