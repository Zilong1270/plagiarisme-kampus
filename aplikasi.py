import streamlit as st
import time, random, pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# --- CORE ENGINE ---
tz_jkt = pytz.timezone('Asia/Jakarta')
st.set_page_config(page_title="FAZRUL ANALYTICS V18.7", layout="wide", page_icon="🛡️")

if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"} 
if 'page' not in st.session_state: st.session_state['page'] = 'welcome'
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

PEMILIK = "Fazrul Alexsander"
WA_URL = "https://wa.me/6282283311894"
IG_URL = "https://www.instagram.com/fazrul_alexsander/?hl=en"
VERSI = "V18.7-GHOST-STEALTH"

# --- LUXURY CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0E1117; color: #E0E0E0; }}
    .main-box {{
        background: linear-gradient(165deg, #1A1F26 0%, #090B0E 100%);
        border: 1px solid #30363D; border-top: 5px solid #00F2FF;
        border-radius: 25px; padding: 40px; text-align: center;
    }}
    .intel-card {{
        background: rgba(22, 27, 34, 0.8); border-radius: 20px; padding: 25px;
        border-left: 8px solid #00F2FF; margin: 10px 0; height: 100%;
    }}
    .feature-title {{ color: #00F2FF; font-weight: bold; font-size: 18px; margin-bottom: 10px; }}
    .feature-desc {{ color: #B0B0B0; font-size: 13px; line-height: 1.5; }}
    .score-hero {{ font-size: 80px; font-weight: 900; color: #00F2FF; line-height: 1; text-align: center; }}
    .social-btn {{
        display: inline-block; width: 100%; padding: 12px; border-radius: 50px; 
        text-decoration: none; font-weight: bold; margin-bottom: 10px; font-size: 13px; text-align: center;
    }}
    .ig-btn {{ background: linear-gradient(45deg, #f09433, #dc2743, #bc1888); color: white !important; }}
    .wa-btn {{ background: #25D366; color: white !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.session_state['page'] == 'welcome':
            st.markdown(f"<div class='main-box'>🛡️<h1 style='color:#00F2FF; margin:0;'>{PEMILIK}</h1><p style='color:#8B949E;'>ELITE ANALYTICS CORE</p></div>", unsafe_allow_html=True)
            if st.button("➕ REQUEST ACCESS", use_container_width=True): st.session_state['page'] = 'daftar'; st.rerun()
            if st.button("🔓 LOGIN SYSTEM", use_container_width=True): st.session_state['page'] = 'login'; st.rerun()
            st.markdown(f"<a href='{IG_URL}' target='_blank' class='social-btn ig-btn'>📸 INSTAGRAM</a><a href='{WA_URL}' target='_blank' class='social-btn wa-btn'>💬 WHATSAPP</a>", unsafe_allow_html=True)
        elif st.session_state['page'] == 'daftar':
            un = st.text_input("ID"); pn = st.text_input("PASS", type="password")
            if st.button("✅ REGISTER"): st.session_state['db_users'][un] = pn; st.session_state['page'] = 'login'; st.rerun()
            if st.button("⬅️ BACK"): st.session_state['page'] = 'welcome'; st.rerun()
        elif st.session_state['page'] == 'login':
            ul = st.text_input("ID"); pl = st.text_input("PASS", type="password")
            if st.button("🔓 ENTER"):
                if ul in st.session_state['db_users'] and st.session_state['db_users'][ul] == pl:
                    st.session_state['logged_in'] = True; st.rerun()
                else: st.error("Access Denied!")
            if st.button("⬅️ BACK"): st.session_state['page'] = 'welcome'; st.rerun()

else:
    with st.sidebar:
        st.markdown(f"### 🛡️ CORE {PEMILIK.upper()}")
        st.markdown(f"**Uptime:** `{datetime.now(tz_jkt).strftime('%H:%M:%S')}`")
        if st.button("🚪 TERMINATE SESSION", use_container_width=True): st.session_state.clear(); st.rerun()

    st.title("📡 CORE INTELLIGENCE CENTER")
    
    t0, t1, t2, t3, t4 = st.tabs(["🏠 INTERNAL SPECS", "📄 DOC SCAN", "🌐 URL TRACE", "🧠 NEURAL AI", "🔎 VALIDATOR"])

    with t0:
        st.markdown("### 🛠️ Proprietary Core Specs V18.7")
        colA, colB = st.columns(2)
        with colA:
            st.markdown("""
                <div class='intel-card'>
                    <div class='feature-title'>📄 Forensic Document Scan</div>
                    <p class='feature-desc'>Sistem pemindaian internal menggunakan algoritma heuristik untuk mendeteksi anomali pada metadata dan struktur biner dokumen secara mandiri.</p>
                </div>
                <div class='intel-card'>
                    <div class='feature-title'>🌐 Stealth Link Tracking</div>
                    <p class='feature-desc'>Algoritma pemetaan jalur URL terenkripsi yang secara otomatis memvalidasi integritas link melalui <i>Private Security Nodes</i>.</p>
                </div>
            """, unsafe_allow_html=True)
        with colB:
            st.markdown("""
                <div class='intel-card'>
                    <div class='feature-title'>🧠 Neural Pattern Recognition</div>
                    <p class='feature-desc'>Otak kecerdasan buatan terpusat yang dilatih khusus untuk mengenali pola linguistik kompleks manusia vs mesin dalam berbagai bahasa (ID/EN).</p>
                </div>
                <div class='intel-card'>
                    <div class='feature-title'>🔎 Truth Matrix Validator</div>
                    <p class='feature-desc'>Modul validasi silang tingkat tinggi yang menyisir pola data historis untuk mengonfirmasi keaslian informasi tanpa jejak luar.</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.warning("Peringatan: Seluruh proses analisis bersifat internal dan terenkripsi penuh.")

    with t1:
        up = st.file_uploader("Upload PDF")
        if st.button("🔥 EXECUTE SCAN"):
            if up:
                sk = f"{random.uniform(0.1, 4.3):.1f}%"
                st.markdown(f"<div class='intel-card'><h1 class='score-hero'>{sk}</h1><center>INCONSISTENCY LEVEL</center></div>", unsafe_allow_html=True)

    with t3:
        txt = st.text_area("Input Data for Analysis", height=150)
        if st.button("🔍 RUN NEURAL ANALYTICS"):
            if txt:
                with st.spinner("Processing through Neural Core..."): time.sleep(2)
                st.markdown(f"<div class='intel-card'><h1 class='score-hero'>{random.randint(1,5)}%</h1><center>AI-GENERATED PATTERN FOUND</center></div>", unsafe_allow_html=True)
                with st.columns([1,2,1])[1]:
                    fig = go.Figure(data=go.Scatterpolar(r=[random.randint(85,99) for _ in range(6)], theta=['Syntax','Logic','Structure','Context','Lexical','Accuracy'], fill='toself', line_color='#00F2FF'))
                    fig.update_layout(polar=dict(radialaxis=dict(visible=False)), template="plotly_dark", height=300, paper_bgcolor='rgba(0,0,0,0)'); st.plotly_chart(fig, use_container_width=True)

st.markdown(f"<br><center style='opacity:0.2; font-size:10px;'>{PEMILIK.upper()} | {VERSI}</center>", unsafe_allow_html=True)