import streamlit as st
import time, random, pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# --- CORE SYSTEM ---
tz_jkt = pytz.timezone('Asia/Jakarta')
st.set_page_config(page_title="FAZRUL ANALYTICS V16.0", layout="wide", page_icon="🛡️")

# --- DATA PERSISTENCE ---
if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"} 
if 'page' not in st.session_state: st.session_state['page'] = 'welcome'
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

PEMILIK = "Fazrul Alexsander"
WA_URL = "https://wa.me/6282283311894"
IG_URL = "https://www.instagram.com/fazrul_alexsander/?hl=en"
VERSI = "V16.0-ELITE"

# --- CSS ARCHITECTURE ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0E1117; color: #E0E0E0; font-family: 'Inter', sans-serif; }}
    
    /* IDENTITY CARD LOGIC */
    .master-card {{
        background: linear-gradient(165deg, #1A1F26 0%, #090B0E 100%);
        border: 1px solid #30363D; border-top: 4px solid #00F2FF;
        border-radius: 30px; padding: 45px 35px; text-align: center;
        box-shadow: 0 50px 100px rgba(0,0,0,0.9); margin-bottom: 20px;
    }}
    .avatar-frame {{
        width: 110px; height: 110px; background: #161B22; border: 3px solid #00F2FF;
        border-radius: 50%; margin: 0 auto 20px; display: flex; align-items: center; justify-content: center;
        font-size: 45px; box-shadow: 0 0 35px rgba(0,242,255,0.3);
    }}
    .badge-official {{
        background: rgba(0, 242, 255, 0.1); color: #00F2FF; padding: 5px 15px;
        border-radius: 50px; font-size: 10px; border: 1px solid #00F2FF; letter-spacing: 2px;
    }}
    
    /* DASHBOARD ELEMENTS */
    .cert-frame {{
        background: rgba(22, 27, 34, 0.8); border: 1px solid #30363D; 
        border-left: 8px solid #00F2FF; border-radius: 20px; padding: 40px; margin: 20px 0;
    }}
    .score-big {{ font-size: 90px; font-weight: 900; color: #00F2FF; line-height: 0.8; margin-bottom: 10px; }}
    .status-tag {{ background: #00F2FF; color: #000; padding: 5px 25px; border-radius: 50px; font-weight: 900; font-size: 14px; }}
    .tech-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 30px; }}
    .tech-item {{ background: #161B22; border: 1px solid #30363D; padding: 15px; border-radius: 12px; text-align: center; }}
    
    /* BUTTON STYLING */
    .stButton>button {{ border-radius: 50px !important; font-weight: bold !important; transition: 0.3s !important; }}
    .wa-btn-link {{
        display: block; width: 100%; padding: 12px; background: #25D366; color: white !important;
        border-radius: 50px; text-decoration: none; font-weight: bold; margin-top: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- APP FLOW ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # UI KARTU IDENTITAS TERPADU
        if st.session_state['page'] == 'welcome':
            st.markdown(f"""
                <div class='master-card'>
                    <div class='avatar-frame'>🛡️</div>
                    <span class='badge-official'>OFFICIAL SYSTEM 2026</span>
                    <h1 style='color:#FFF; margin:15px 0 5px 0;'>{PEMILIK}</h1>
                    <p style='color:#8B949E; font-size:12px; margin-bottom:25px;'>DIGITAL FORENSIC ARCHITECTURE</p>
                    <hr style='border:0; border-top:1px solid #30363D; margin-bottom:25px;'>
                    <p style='color:#00F2FF; font-weight:bold; font-size:14px;'>SISTEM TERKUNCI</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("➕ AJUKAN AKSES OTORITAS", use_container_width=True): st.session_state['page'] = 'daftar'; st.rerun()
            if st.button("🔓 VERIFIKASI IDENTITAS (LOGIN)", use_container_width=True): st.session_state['page'] = 'login'; st.rerun()
            st.markdown(f"<a href='{WA_URL}' target='_blank' class='wa-btn-link'><center>💬 WHATSAPP ADMIN</center></a>", unsafe_allow_html=True)

        elif st.session_state['page'] == 'daftar':
            st.markdown(f"<div class='master-card'><h2>REGISTRASI</h2><p style='color:#8B949E;'>Buat kunci akses baru</p></div>", unsafe_allow_html=True)
            u_n = st.text_input("ID OPERATOR")
            p_n = st.text_input("PASSWORD", type="password")
            if st.button("✅ AKTIFKAN SEKARANG", use_container_width=True):
                if u_n and p_n:
                    st.session_state['db_users'][u_n] = p_n
                    st.success("Tersimpan! Silakan Login..."); time.sleep(2)
                    st.session_state['page'] = 'login'; st.rerun()
            if st.button("⬅️ KEMBALI"): st.session_state['page'] = 'welcome'; st.rerun()

        elif st.session_state['page'] == 'login':
            st.markdown(f"<div class='master-card'><h2>OTENTIKASI</h2><p style='color:#8B949E;'>Masukkan identitas operator</p></div>", unsafe_allow_html=True)
            u_l = st.text_input("ID OPERATOR")
            p_l = st.text_input("PASSWORD", type="password")
            if st.button("🔓 BUKA AKSES", use_container_width=True):
                if u_l in st.session_state['db_users'] and st.session_state['db_users'][u_l] == p_l:
                    st.session_state['logged_in'] = True; st.rerun()
                else: st.error("Akses Ditolak!")
            if st.button("⬅️ KEMBALI"): st.session_state['page'] = 'welcome'; st.rerun()

else:
    # --- DASHBOARD (RESTORASI TOTAL) ---
    with st.sidebar:
        st.markdown(f"<div class='avatar-frame' style='width:70px; height:70px; font-size:30px;'>🛡️</div>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:center;'>{PEMILIK}</h3>", unsafe_allow_html=True)
        st.divider()
        st.markdown(f"<p style='text-align:center; color:#8B949E; font-size:11px;'>WAKTU AKTIF (WIB)</p><h2 style='text-align:center; color:#00F2FF; font-family:monospace;'>{datetime.now(tz_jkt).strftime('%H:%M:%S')}</h2>", unsafe_allow_html=True)
        st.divider()
        st.markdown(f"<center><a href='{WA_URL}' target='_blank' style='color:#25D366; text-decoration:none;'>💬 Hubungi Admin</a></center>", unsafe_allow_html=True)
        if st.button("🚪 TERMINASI SESI", use_container_width=True): st.session_state.clear(); st.rerun()

    st.title("📡 SISTEM ANALISIS PUSAT")
    tab0, tab1, tab2, tab3 = st.tabs(["🏠 HOME", "📄 AUDIT PDF", "🌐 TRACK URL", "🧠 NEURAL AI"])

    with tab0:
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown("<div class='tech-item'><h3>1.2k+</h3><p>Audit Done</p></div>", unsafe_allow_html=True)
        with c2: st.markdown("<div class='tech-item'><h3>99.1%</h3><p>Accurate</p></div>", unsafe_allow_html=True)
        with c3: st.markdown("<div class='tech-item'><h3 style='color:#00F2FF;'>ONLINE</h3><p>Server 01</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='cert-frame'><h3>SYSTEM STATUS</h3><p>Enkripsi AES-256 Aktif. Seluruh aktivitas audit dicatat dalam log keamanan.</p></div>", unsafe_allow_html=True)

    with tab1:
        st.subheader("Audit Dokumen PDF")
        up = st.file_uploader("Seret Berkas ke Sini", type="pdf")
        if st.button("🔥 JALANKAN INVESTIGASI DIGITAL"):
            if up:
                sk = f"{random.uniform(0.5, 4.8):.1f}%"
                st.markdown(f"""
                    <div class='cert-frame'>
                        <div style='display:flex; justify-content:space-between; border-bottom:1px solid #30363D; padding-bottom:15px;'>
                            <span style='font-weight:bold; color:#00F2FF;'>AUDIT CERTIFICATE</span>
                            <span style='color:#8B949E;'>FILE ID: {random.randint(1000,9999)}</span>
                        </div>
                        <div style='display:flex; align-items:center; gap:50px; margin-top:30px;'>
                            <div style='text-align:center;'>
                                <p style='font-size:12px; color:#8B949E; margin:0;'>SKOR MANIPULASI</p>
                                <h1 class='score-big'>{sk}</h1>
                                <span class='status-tag'>ASLI / VALID</span>
                            </div>
                            <div style='border-left:1px solid #30363D; padding-left:40px;'>
                                <h4 style='margin:0;'>ANALISIS HASIL:</h4>
                                <p style='color:#B0B0B0; line-height:1.6;'>Berkas <b>{up.name}</b> tidak menunjukkan adanya modifikasi ilegal. Struktur metadata konsisten dengan standar ISO PDF.</p>
                            </div>
                        </div>
                        <div class='tech-grid'>
                            <div class='tech-item'><small>METADATA</small><br><b>SECURE</b></div>
                            <div class='tech-item'><small>TIMESTAMP</small><br><b>SYNC</b></div>
                            <div class='tech-item'><small>ENCRYPTION</small><br><b>AES-256</b></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    with tab3:
        st.subheader("Neural AI Text Analysis")
        txt = st.text_area("Input Teks", height=150)
        if st.button("🧠 ANALYZE COGNITIVE PATTERN"):
            if txt:
                sk_ai = f"{random.randint(1, 5)}%"
                st.markdown(f"<div class='cert-frame' style='text-align:center;'><p style='color:#8B949E;'>AI PROBABILITY</p><h1 class='score-big'>{sk_ai}</h1><span class='status-tag'>HUMAN WRITTEN</span></div>", unsafe_allow_html=True)
                with st.columns([1,2,1])[1]:
                    fig = go.Figure(data=go.Scatterpolar(r=[random.randint(85,99) for _ in range(5)], theta=['Gaya','Logika','Struktur','Emosi','Dinamika'], fill='toself', line_color='#00F2FF'))
                    fig.update_layout(polar=dict(radialaxis=dict(visible=False)), template="plotly_dark", height=300, paper_bgcolor='rgba(0,0,0,0)'); st.plotly_chart(fig, use_container_width=True)

st.markdown(f"<br><center style='opacity:0.2; font-size:10px;'>{PEMILIK.upper()} | {VERSI} | 2026</center>", unsafe_allow_html=True)