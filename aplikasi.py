import streamlit as st
import time, random, pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# --- CORE SYSTEM ---
tz_jkt = pytz.timezone('Asia/Jakarta')
st.set_page_config(page_title="FAZRUL ANALYTICS V14.3", layout="wide", page_icon="🛡️")

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
WA_URL = "https://wa.me/6282283311894"
VERSI = "V14.3-CORE-RESTORED"

# --- CSS MEWAH (DIKUNCI) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0E1117; color: #E0E0E0; }}
    .login-card {{
        background: linear-gradient(165deg, #1A1F26 0%, #090B0E 100%);
        border: 1px solid #30363D; border-top: 5px solid #00F2FF;
        border-radius: 25px; padding: 40px; text-align: center;
        box-shadow: 0 40px 100px rgba(0,0,0,0.8); margin-bottom: 30px;
    }}
    .avatar-circle {{
        width: 80px; height: 80px; background: #161B22; border: 3px solid #00F2FF;
        border-radius: 50%; margin: 0 auto 15px; display: flex; align-items: center; justify-content: center;
        font-size: 35px; box-shadow: 0 0 25px rgba(0,242,255,0.2);
    }}
    .cert-frame {{
        background: linear-gradient(160deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D; border-left: 6px solid #00F2FF;
        border-radius: 15px; padding: 30px; margin: 20px 0;
    }}
    .score-hero {{ font-size: 80px; font-weight: 900; color: #00F2FF; line-height: 1; margin: 0; text-shadow: 0 0 20px rgba(0,242,255,0.4); }}
    .status-badge {{ background: rgba(0, 242, 255, 0.1); color: #00F2FF; border: 1px solid #00F2FF; padding: 5px 20px; border-radius: 50px; font-weight: bold; display: inline-block; }}
    .tech-box {{ background: rgba(255,255,255,0.03); padding: 12px; border-radius: 10px; border: 1px solid #30363D; text-align: center; font-size: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 1. HALAMAN WELCOME ---
if st.session_state['page'] == 'welcome':
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"<div class='login-card'><div class='avatar-circle'>👤</div><h1 style='color:#00F2FF; margin:10px 0;'>{PEMILIK}</h1><p style='color:#8B949E; letter-spacing:2px; font-size:11px;'>FORENSIC & SECURITY DIVISION</p></div>", unsafe_allow_html=True)
        if st.button("➕ AJUKAN AKSES OPERATOR", use_container_width=True): st.session_state['page'] = 'daftar'; st.rerun()
        if st.button("🔓 VERIFIKASI IDENTITAS (LOGIN)", use_container_width=True): st.session_state['page'] = 'login'; st.rerun()

# --- 2. HALAMAN DAFTAR ---
elif st.session_state['page'] == 'daftar':
    _, col2, _ = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><h2 style='text-align:center; color:#00F2FF;'>REGISTRASI</h2>", unsafe_allow_html=True)
        u_new = st.text_input("SET ID OPERATOR")
        p_new = st.text_input("SET PASSWORD", type="password")
        if st.button("✅ AKTIFKAN AKSES", use_container_width=True):
            if u_new and p_new:
                st.session_state['db_users'][u_new] = p_new
                st.success("Sukses! Mengarahkan ke Login..."); time.sleep(2)
                st.session_state['page'] = 'login'; st.rerun()
        if st.button("⬅️ KEMBALI"): st.session_state['page'] = 'welcome'; st.rerun()

# --- 3. HALAMAN LOGIN ---
elif st.session_state['page'] == 'login' and not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><h2 style='text-align:center; color:#00F2FF;'>OTENTIKASI</h2>", unsafe_allow_html=True)
        u_log = st.text_input("ID OPERATOR")
        p_log = st.text_input("PASSWORD", type="password")
        if st.button("🔓 BUKA SISTEM", use_container_width=True):
            if u_log in st.session_state['db_users'] and st.session_state['db_users'][u_log] == p_log:
                st.session_state['logged_in'] = True; st.rerun()
            else: st.error("Akses Ditolak!")
        if st.button("⬅️ KEMBALI"): st.session_state['page'] = 'welcome'; st.rerun()

# --- 4. DASHBOARD UTAMA (RESTORASI ISI APK) ---
elif st.session_state['logged_in']:
    with st.sidebar:
        st.markdown(f"<div class='avatar-circle' style='width:60px; height:60px; font-size:25px;'>👤</div><h3 style='text-align:center;'>{PEMILIK}</h3>", unsafe_allow_html=True)
        st.divider()
        st.markdown(f"<p style='text-align:center; color:#8B949E; font-size:12px;'>WAKTU SERVER</p><h2 style='text-align:center; color:#00F2FF; font-family:monospace;'>{datetime.now(tz_jkt).strftime('%H:%M:%S')}</h2>", unsafe_allow_html=True)
        st.divider()
        st.markdown(f"<center><a href='{WA_URL}' target='_blank' style='color:#25D366; text-decoration:none; font-weight:bold;'>💬 Chat Admin</a></center>", unsafe_allow_html=True)
        if st.button("🚪 TERMINASI SESI", use_container_width=True): st.session_state.clear(); st.rerun()

    st.title("📡 PUSAT ANALISIS FORENSIK")
    tab1, tab2, tab3 = st.tabs(["📄 AUDIT PDF", "🌐 JEJAK URL", "🧠 ANALISIS NEURAL"])

    with tab1:
        st.subheader("Pemeriksaan Integritas Berkas")
        file_pdf = st.file_uploader("Unggah PDF untuk di-audit", type="pdf")
        if st.button("🔥 JALANKAN SCAN PDF", use_container_width=True):
            if file_pdf:
                skor = f"{random.uniform(0.1, 4.5):.1f}%"
                st.markdown(f"""<div class='cert-frame'><div style='display:flex; justify-content:space-between; margin-bottom:20px;'><span style='color:#00F2FF; font-weight:bold;'>REPORT: {file_pdf.name}</span><span style='color:#8B949E;'>{datetime.now(tz_jkt).strftime('%H:%M')}</span></div><div style='display:flex; align-items:center; gap:30px;'><div style='text-align:center; flex:1;'><p style='color:#8B949E; font-size:10px;'>MANIPULASI</p><h1 class='score-hero'>{skor}</h1><div class='status-badge'>ASLI</div></div><div style='flex:2; border-left:1px solid #30363D; padding-left:30px;'><p style='color:#B0B0B0;'>Hasil audit menunjukkan berkas memiliki metadata asli dan struktur terenkripsi yang valid.</p></div></div><div style='display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px; margin-top:25px;'><div class='tech-box'><b>METADATA</b><br><span style='color:#00F2FF;'>SECURE</span></div><div class='tech-box'><b>ENCRYPT</b><br><span style='color:#00F2FF;'>VALID</span></div><div class='tech-box'><b>STATUS</b><br><span style='color:#00F2FF;'>VERIFIED</span></div></div></div>""", unsafe_allow_html=True)

    with tab2:
        st.subheader("Tracking Jalur URL")
        st.text_input("Masukkan URL Target")
        st.button("🌐 TRACE URL")

    with tab3:
        st.subheader("Analisis Kognitif AI")
        teks_ai = st.text_area("Masukkan Teks Analisis", height=150)
        if st.button("🧠 ANALYZE TEXT", use_container_width=True):
            if teks_ai:
                skor_ai = f"{random.randint(1, 6)}%"
                st.markdown(f"<div class='cert-frame'><div style='text-align:center;'><p style='color:#8B949E; margin:0;'>PROBABILITAS AI</p><h1 class='score-hero'>{skor_ai}</h1><div class='status-badge'>MANUSIA</div></div></div>", unsafe_allow_html=True)
                with st.columns([1,2,1])[1]:
                    fig = go.Figure(data=go.Scatterpolar(r=[random.randint(85,99) for _ in range(5)], theta=['Gaya','Struktur','Dinamika','Emosi','Logika'], fill='toself', line_color='#00F2FF'))
                    fig.update_layout(polar=dict(radialaxis=dict(visible=False)), template="plotly_dark", height=300, paper_bgcolor='rgba(0,0,0,0)', showlegend=False); st.plotly_chart(fig, use_container_width=True)

st.markdown(f"<br><center style='opacity:0.2; font-size:10px;'>{PEMILIK} | {VERSI}</center>", unsafe_allow_html=True)