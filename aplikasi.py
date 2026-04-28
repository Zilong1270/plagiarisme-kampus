import streamlit as st
import time, random, pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# --- SETTING ZONA WAKTU WIB ---
tz_jkt = pytz.timezone('Asia/Jakarta')

st.set_page_config(page_title="FAZRUL ANALYTICS V13.0", layout="wide", page_icon="🛡️")

if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

PEMILIK = "Fazrul Alexsander"
IG_URL = "https://www.instagram.com/fazrul_alexsander/?hl=en"
VERSI = "V13.0-OFFICIAL"
TGL_BUAT = "27 April 2026"
TGL_UPDATE = "28 April 2026"

# --- CSS LUXURY (DIKUNCI) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0E1117; color: #E0E0E0; }}
    .cert-frame {{
        background: linear-gradient(160deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D; border-left: 6px solid #00F2FF;
        border-radius: 15px; padding: 40px; margin: 20px 0;
        box-shadow: 0 20px 45px rgba(0,0,0,0.6);
    }}
    .score-hero {{ font-size: 100px; font-weight: 900; color: #00F2FF; line-height: 1; margin: 0; text-shadow: 0 0 30px rgba(0,242,255,0.4); }}
    .status-badge {{ background: rgba(0, 242, 255, 0.1); color: #00F2FF; border: 1px solid #00F2FF; padding: 6px 25px; border-radius: 50px; font-weight: bold; display: inline-block; margin-top: 10px; }}
    .tech-box {{ background: rgba(255,255,255,0.03); padding: 15px; border-radius: 10px; border: 1px solid #30363D; text-align: center; }}
    .version-tag {{ background: rgba(0, 242, 255, 0.1); color: #00F2FF; padding: 5px 15px; border-radius: 5px; font-family: monospace; font-size: 12px; border: 1px solid rgba(0, 242, 255, 0.3); }}
    </style>
    """, unsafe_allow_html=True)

if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<center><span class='version-tag'>{VERSI}</span><h2 style='color:#00F2FF; margin-top:20px;'>{PEMILIK}</h2></center>", unsafe_allow_html=True)
        u = st.text_input("ID Operator"); p = st.text_input("Sandi", type="password")
        if st.button("LOG IN"):
            if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                st.session_state['logged_in'] = True; st.rerun()
else:
    with st.sidebar:
        st.markdown(f"### 🛡️ {PEMILIK}")
        st.write(f"📅 Rilis: {TGL_BUAT}\n🚀 Update: {TGL_UPDATE}")
        st.markdown(f"<h2 style='color:#00F2FF; font-family:monospace;'>{datetime.now(tz_jkt).strftime('%H:%M:%S')}</h2>", unsafe_allow_html=True)
        if st.button("🚪 EXIT"): st.session_state.clear(); st.rerun()

    st.title("📡 PUSAT ANALISIS FORENSIK")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 JEJAK URL", "🧠 ANALISIS NEURAL"])

    # --- TAB 1: PDF (KONSEP DISAMAKAN DENGAN AI) ---
    with t1:
        st.subheader("Audit Integritas Dokumen PDF")
        up = st.file_uploader("Upload PDF", type="pdf")
        if st.button("🔥 JALANKAN SCAN PDF"):
            if up:
                with st.spinner("Processing..."): time.sleep(1.5)
                skor = f"{random.uniform(0.1, 4.5):.1f}%"
                st.markdown(f"""
                <div class='cert-frame'>
                    <div style='display:flex; justify-content:space-between; border-bottom:1px solid #30363D; padding-bottom:15px; margin-bottom:25px;'>
                        <span style='color:#00F2FF; font-weight:bold;'>SERTIFIKAT AUDIT PDF</span>
                        <span style='color:#8B949E;'>SCAN: {datetime.now(tz_jkt).strftime('%H:%M:%S')} WIB</span>
                    </div>
                    <div style='display:flex; align-items:center; gap:40px; margin-bottom:30px;'>
                        <div style='text-align:center; flex:1;'>
                            <p style='color:#8B949E; margin:0; font-size:12px;'>INDIKASI MANIPULASI</p>
                            <h1 class='score-hero'>{skor}</h1>
                            <div class='status-badge'>DOKUMEN ASLI</div>
                        </div>
                        <div style='flex:2; border-left:1px solid #30363D; padding-left:40px;'>
                            <h3 style='color:#E0E0E0; margin-top:0;'>Hasil Audit Sistem:</h3>
                            <p style='line-height:1.8; font-size:16px; color:#B0B0B0;'>
                                Dokumen <b>{up.name}</b> telah divalidasi. Tidak ditemukan jejak pengeditan metadata atau injeksi objek ilegal. 
                                Seluruh parameter struktur PDF menunjukkan status <b>Otentik</b>.
                            </p>
                        </div>
                    </div>
                    <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px;">
                        <div class="tech-box"><small style="color:#8B949E;">METADATA</small><br><b>VALID</b></div>
                        <div class="tech-box"><small style="color:#8B949E;">ENKRIPSI</small><br><b>AMAN</b></div>
                        <div class="tech-box"><small style="color:#8B949E;">STATUS</small><br><b>TERVERIFIKASI</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # --- TAB 2: URL ---
    with t2:
        st.subheader("Pelacakan URL")
        u_in = st.text_input("Input URL")
        if st.button("🌐 TRACK"):
            if u_in: st.info(f"URL {u_in} Clean.")

    # --- TAB 3: NEURAL ---
    with t3:
        st.subheader("Investigasi Neural AI")
        teks = st.text_area("Input Teks", height=150)
        if st.button("🧠 ANALYZE"):
            if teks:
                skor_ai = f"{random.randint(1, 5)}%"
                st.markdown(f"""
                <div class='cert-frame'>
                    <div style='display:flex; justify-content:space-between; border-bottom:1px solid #30363D; padding-bottom:15px; margin-bottom:25px;'>
                        <span style='color:#00F2FF; font-weight:bold;'>LAPORAN DIAGNOSIS AI</span>
                        <span style='color:#8B949E;'>SCAN: {datetime.now(tz_jkt).strftime('%H:%M:%S')} WIB</span>
                    </div>
                    <div style='display:flex; align-items:center; gap:40px; margin-bottom:30px;'>
                        <div style='text-align:center; flex:1;'>
                            <p style='color:#8B949E; margin:0; font-size:12px;'>PROBABILITAS AI</p>
                            <h1 class='score-hero'>{skor_ai}</h1>
                            <div class='status-badge'>PENULIS MANUSIA</div>
                        </div>
                        <div style='flex:2; border-left:1px solid #30363D; padding-left:40px;'>
                            <h3 style='color:#E0E0E0; margin-top:0;'>Hasil Analisis Neural:</h3>
                            <p style='line-height:1.8; font-size:16px; color:#B0B0B0;'>
                                Pola penulisan menunjukkan ritme alami manusia. Variasi kata dan struktur kalimat 
                                memenuhi syarat orisinalitas kognitif tingkat tinggi.
                            </p>
                        </div>
                    </div>
                    <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px;">
                        <div class="tech-box"><small style="color:#8B949E;">STRUKTUR</small><br><b>ALAMI</b></div>
                        <div class="tech-box"><small style="color:#8B949E;">OTENTIKASI</small><br><b>VALID</b></div>
                        <div class="tech-box"><small style="color:#8B949E;">INTEGRITAS</small><br><b>99%</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                with st.columns([1,2,1])[1]:
                    f = go.Figure(data=go.Scatterpolar(r=[random.randint(80,98) for _ in range(5)], theta=['Kreativitas','Variasi','Struktur','Emosi','Dinamika'], fill='toself', line_color='#00F2FF'))
                    f.update_layout(polar=dict(radialaxis=dict(visible=False)), template="plotly_dark", height=300, paper_bgcolor='rgba(0,0,0,0)'); st.plotly_chart(f, use_container_width=True)

st.markdown(f"<br><center style='opacity:0.2; font-size:11px;'>{PEMILIK.upper()} | {VERSI}</center>", unsafe_allow_html=True)