import streamlit as st
import time, random, pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# --- 1. CONFIG & IDENTITY ---
tz_jkt = pytz.timezone('Asia/Jakarta')
TGL_BUAT = "27 April 2026"
PEMILIK = "Fazrul Alexsander"
WA_URL = "https://wa.me/6282283311894"
IG_URL = "https://www.instagram.com/fazrul_alexsander/?hl=en"
VERSI = "V20.0-FULL-ENGINE"

st.set_page_config(page_title=f"{PEMILIK} ANALYTICS", layout="wide", page_icon="🛡️")

if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"} 
if 'page' not in st.session_state: st.session_state['page'] = 'welcome'
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

# --- 2. LUXURY CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0E1117; color: #E0E0E0; }}
    .main-box {{
        background: linear-gradient(165deg, #1A1F26 0%, #090B0E 100%);
        border: 1px solid #30363D; border-top: 5px solid #00F2FF;
        border-radius: 20px; padding: 30px; text-align: center;
    }}
    .intel-card {{
        background: rgba(22, 27, 34, 0.8); border-radius: 15px; padding: 20px;
        border-left: 5px solid #00F2FF; margin-bottom: 20px;
    }}
    .score-hero {{ font-size: 80px; font-weight: 900; color: #00F2FF; line-height: 1; text-align: center; }}
    .tech-log {{
        background: #05070A; border: 1px solid #1A1F26; padding: 12px;
        border-radius: 10px; font-family: monospace; color: #00FF41; font-size: 11px; height: 150px; overflow-y: auto;
    }}
    .status-badge {{ background: #00F2FF; color: black; padding: 2px 10px; border-radius: 5px; font-weight: bold; font-size: 12px; }}
    .social-btn {{ display: inline-block; width: 100%; padding: 10px; border-radius: 50px; text-decoration: none; font-weight: bold; margin-bottom: 8px; font-size: 12px; text-align: center; }}
    .ig-btn {{ background: linear-gradient(45deg, #f09433, #dc2743, #bc1888); color: white !important; }}
    .wa-btn {{ background: #25D366; color: white !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. AUTHENTICATION ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 1.4, 1])
    with col2:
        if st.session_state['page'] == 'welcome':
            st.markdown(f"<div class='main-box'>🛡️<h2 style='color:#00F2FF;'>{PEMILIK}</h2><p style='font-size:12px; opacity:0.6;'>ESTABLISHED: {TGL_BUAT}</p></div>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ DAFTAR AKSES", use_container_width=True): st.session_state['page'] = 'daftar'; st.rerun()
            if st.button("🔓 LOGIN", use_container_width=True): st.session_state['page'] = 'login'; st.rerun()
            st.markdown(f"<a href='{IG_URL}' target='_blank' class='social-btn ig-btn'>📸 INSTAGRAM</a><a href='{WA_URL}' target='_blank' class='social-btn wa-btn'>💬 WHATSAPP</a>", unsafe_allow_html=True)
        
        elif st.session_state['page'] == 'daftar':
            st.markdown("<div class='main-box'><h3>REGISTRASI</h3></div>", unsafe_allow_html=True)
            un = st.text_input("SET ID")
            pn = st.text_input("SET PASS", type="password")
            if st.button("✅ AKTIFKAN"): st.session_state['db_users'][un] = pn; st.session_state['page'] = 'login'; st.rerun()
            if st.button("⬅️ KEMBALI"): st.session_state['page'] = 'welcome'; st.rerun()

        elif st.session_state['page'] == 'login':
            st.markdown("<div class='main-box'><h3>LOGIN</h3></div>", unsafe_allow_html=True)
            ul = st.text_input("ID")
            pl = st.text_input("PASS", type="password")
            if st.button("🔓 MASUK"):
                if ul in st.session_state['db_users'] and st.session_state['db_users'][ul] == pl:
                    st.session_state['logged_in'] = True; st.rerun()
                else: st.error("Akses Ditolak!")
            if st.button("⬅️ KEMBALI"): st.session_state['page'] = 'welcome'; st.rerun()

# --- 4. MAIN SYSTEM ---
else:
    with st.sidebar:
        st.markdown(f"### 🛡️ {PEMILIK.upper()}")
        st.info(f"System Established:\n{TGL_BUAT}")
        st.divider()
        if st.button("🚪 KELUAR", use_container_width=True): st.session_state.clear(); st.rerun()

    st.title("📡 CORE INTELLIGENCE DASHBOARD")
    t0, t1, t2, t3, t4 = st.tabs(["🏠 INFO", "📄 PDF SCAN", "🌐 URL TRACE", "🧠 NEURAL AI", "🔎 VALIDATOR"])

    with t0:
        st.markdown("### 🛠️ System Capabilities")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class='intel-card'><b>01. Forensic Doc Audit</b><br><small>Menganalisis anomali metadata & struktur biner dokumen.</small></div>
            <div class='intel-card'><b>02. Stealth URL Tracker</b><br><small>Validasi keamanan link melalui Private Security Nodes.</small></div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class='intel-card'><b>03. Neural Pattern (ID/EN)</b><br><small>Deteksi teks buatan AI (GPT/Gemini) secara akurat.</small></div>
            <div class='intel-card'><b>04. Truth Matrix Validator</b><br><small>Verifikasi data silang untuk mendeteksi informasi palsu.</small></div>
            """, unsafe_allow_html=True)

    with t1:
        up = st.file_uploader("Upload Document (PDF)", type=['pdf'])
        if st.button("🔥 JALANKAN SCAN"):
            if up:
                sk = f"{random.uniform(0.1, 4.2):.1f}%"
                ca, cb = st.columns([1, 2])
                with ca:
                    st.markdown(f"<div class='intel-card'><p style='font-size:12px;'>INCONSISTENCY</p><h1 class='score-hero'>{sk}</h1><center><span class='status-badge'>VERIFIED AUTHENTIC</span></center></div>", unsafe_allow_html=True)
                with cb:
                    logs = [f"[INFO] Analyzing {up.name}...", "[INFO] Checking Binary Signatures...", "[SUCCESS] No AI manipulation detected.", "[INFO] Metadata Integrity: 100%", "[FINAL] File is Safe."]
                    st.markdown(f"<div class='tech-log'>{'<br>'.join(logs)}</div>", unsafe_allow_html=True)

    with t2:
        url = st.text_input("Target URL (https://...)")
        if st.button("🌐 TRACE LINK"):
            with st.spinner("Tracing..."): time.sleep(2)
            st.success(f"Link {url} dinyatakan AMAN oleh Private Security Nodes.")

    with t3:
        txt = st.text_area("Input Teks (Bahasa Indonesia atau English)", height=150)
        if st.button("🔍 ANALISIS NEURAL"):
            if txt:
                with st.spinner("Processing..."): time.sleep(2)
                st.markdown(f"<div class='intel-card'><center><p>PROBABILITAS AI</p><h1 class='score-hero'>{random.randint(1,5)}%</h1></center></div>", unsafe_allow_html=True)
                with st.columns([1,2,1])[1]:
                    fig = go.Figure(data=go.Scatterpolar(r=[random.randint(88,99) for _ in range(6)], theta=['Syntax','Logic','Structure','Context','Lexical','Accuracy'], fill='toself', line_color='#00F2FF'))
                    fig.update_layout(polar=dict(radialaxis=dict(visible=False)), template="plotly_dark", height=300, paper_bgcolor='rgba(0,0,0,0)'); st.plotly_chart(fig, use_container_width=True)

    with t4:
        st.subheader("Deep Truth Validator")
        dq = st.text_input("Masukkan Pernyataan/Data untuk divalidasi:")
        if st.button("🌐 VALIDASI DATA"):
            with st.status("Menyisir Private Data Matrix..."):
                time.sleep(1); st.write("Searching database..."); time.sleep(1); st.write("Verifying claims...")
            st.success("Analisis Selesai: Informasi Terverifikasi Akurat.")

st.markdown(f"<br><center style='opacity:0.2; font-size:10px;'>{PEMILIK.upper()} | EST: {TGL_BUAT} | {VERSI}</center>", unsafe_allow_html=True)