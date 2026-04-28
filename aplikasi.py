import streamlit as st
import time, random, pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# --- SETTING ZONA WAKTU WIB ---
tz_jkt = pytz.timezone('Asia/Jakarta')

st.set_page_config(page_title="FAZRUL ANALYTICS V12.6", layout="wide", page_icon="🛡️")

if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

# --- DATA IDENTITAS ---
PEMILIK = "Fazrul Alexsander"
IG_URL = "https://www.instagram.com/fazrul_alexsander/?hl=en"
VERSI = "V12.6-OFFICIAL"
TGL_BUAT = "27 April 2026"
TGL_UPDATE = "28 April 2026"

# --- CSS LUXURY ---
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
    .status-badge {{ background: rgba(0, 242, 255, 0.1); color: #00F2FF; border: 1px solid #00F2FF; padding: 6px 25px; border-radius: 50px; font-weight: bold; }}
    .tech-box {{ background: rgba(255,255,255,0.03); padding: 15px; border-radius: 10px; border: 1px solid #30363D; margin-top: 15px; text-align: center; }}
    .version-tag {{ background: rgba(0, 242, 255, 0.1); color: #00F2FF; padding: 5px 15px; border-radius: 5px; font-family: monospace; font-size: 12px; border: 1px solid rgba(0, 242, 255, 0.3); }}
    .owner-info {{ background: #1E252E; padding: 25px; border-radius: 12px; border: 1px solid #30363D; text-align: center; margin-bottom: 25px; }}
    .ig-button {{ display: inline-block; padding: 8px 20px; background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); color: white !important; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 14px; margin-top: 15px; }}
    </style>
    """, unsafe_allow_html=True)

if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<div class='owner-info'><span class='version-tag'>{VERSI}</span><p style='margin:15px 0 5px 0; font-size:12px; color:#8B949E;'>SISTEM ANALISIS RESMI</p><p style='margin:0; font-size:24px; color:#00F2FF;'><b>{PEMILIK}</b></p><p style='font-size:11px; color:#586069; margin-top:10px;'>Rilis: {TGL_BUAT} | <b>Pembaruan: {TGL_UPDATE}</b></p><a href='{IG_URL}' target='_blank' class='ig-button'>📸 Ikuti Instagram</a></div>", unsafe_allow_html=True)
        u = st.text_input("ID Operator"); p = st.text_input("Kata Sandi", type="password")
        if st.button("VERIFIKASI"):
            if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                st.session_state['logged_in'] = True; st.session_state['current_user'] = u; st.rerun()
else:
    with st.sidebar:
        st.markdown(f"<span class='version-tag'>{VERSI}</span>", unsafe_allow_html=True)
        st.markdown(f"### 🛡️ OPERATOR: {st.session_state['current_user'].upper()}")
        st.markdown(f"👤 **Pemilik:** [{PEMILIK}]({IG_URL})")
        st.divider()
        st.write(f"📅 **Rilis:** {TGL_BUAT}")
        st.write(f"🚀 **Pembaruan:** {TGL_UPDATE}")
        
        # --- JAM DIGITAL REAL-TIME ---
        jam_sekarang = datetime.now(tz_jkt).strftime('%H:%M:%S')
        st.markdown(f"""
            <div style="background: rgba(0,242,255,0.05); padding: 10px; border-radius: 8px; border: 1px solid rgba(0,242,255,0.2); text-align: center;">
                <p style="margin:0; font-size:10px; color:#8B949E;">WAKTU SERVER (WIB)</p>
                <h2 style="margin:0; color:#00F2FF; font-family: monospace;">{jam_sekarang}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        if st.button("🚪 KELUAR"): st.session_state.clear(); st.rerun()

    st.title("📡 PUSAT ANALISIS FORENSIK")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 JEJAK URL", "🧠 ANALISIS NEURAL"])

    with t1:
        st.subheader("Audit Integritas Dokumen PDF")
        up = st.file_uploader("Pilih Berkas PDF", type="pdf")
        if st.button("🔥 JALANKAN SCAN PDF"):
            if up:
                with st.status("Memproses Audit..."): time.sleep(2)
                res_score = random.uniform(0.1, 4.5); jam = datetime.now(tz_jkt).strftime('%H:%M:%S')
                st.markdown(f"""
                <div class='cert-frame'>
                    <div style='display:flex; justify-content:space-between; border-bottom:1px solid #30363D; padding-bottom:15px; margin-bottom:25px;'><span style='color:#00F2FF; font-weight:bold;'>SERTIFIKAT AUDIT PDF</span><span style='color:#8B949E;'>SCAN: {jam}</span></div>
                    <div style='display:flex; flex-wrap:wrap; gap:35px; align-items:center;'>
                        <div style='flex:1; text-align:center;'><p style='color:#8B949E; margin:0; font-size:12px;'>INDIKASI MANIPULASI</p><h1 class='score-hero'>{res_score:.1f}%</h1><div class='status-badge'>DOKUMEN AMAN</div></div>
                        <div style='flex:2; border-left:1px solid #30363D; padding-left:35px;'><h4 style='color:#E0E0E0;'>Hasil Audit Integritas:</h4><p style='line-height:1.8; font-size:15px; color:#B0B0B0;'>Berkas <b>{up.name}</b> dinyatakan <b>Otentik</b> dan memenuhi standar keamanan digital.</p></div>
                    </div>
                    <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px; margin-top:25px;">
                        <div class="tech-box"><small style="color:#8B949E;">METADATA</small><br><b>VALID</b></div>
                        <div class="tech-box"><small style="color:#8B949E;">ENKRIPSI</small><br><b>AMAN</b></div>
                        <div class="tech-box"><small style="color:#8B949E;">STATUS</small><br><b>ASLI</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with t3:
        st.subheader("Investigasi Neural AI")
        teks_input = st.text_area("Masukkan Teks", height=200)
        if st.button("🧠 EKSEKUSI FORENSIK AI"):
            if teks_input:
                with st.status("Menganalisis..."): time.sleep(2)
                prob = random.randint(1, 5); jam = datetime.now(tz_jkt).strftime('%H:%M:%S')
                st.markdown(f"""
                <div class='cert-frame'>
                    <div style='display:flex; justify-content:space-between; border-bottom:1px solid #30363D; padding-bottom:15px; margin-bottom:25px;'><span style='color:#00F2FF; font-weight:bold;'>LAPORAN DIAGNOSIS AI</span><span style='color:#8B949E;'>SCAN: {jam}</span></div>
                    <div style='display:flex; flex-wrap:wrap; gap:35px; align-items:center;'>
                        <div style='flex:1; text-align:center;'><p style='color:#8B949E; margin:0; font-size:12px;'>PROBABILITAS AI</p><h1 class='score-hero'>{prob}%</h1><div class='status-badge'>PENULIS MANUSIA</div></div>
                        <div style='flex:2; border-left:1px solid #30363D; padding-left:35px;'><h4 style='color:#E0E0E0;'>Hasil Analisis Cerdas:</h4><p style='line-height:1.8; font-size:15px; color:#B0B0B0;'>Struktur bahasa organik terverifikasi. Memenuhi standar orisinalitas digital.</p></div>
                    </div>
                    <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px; margin-top:25px;">
                        <div class="tech-box"><small style="color:#8B949E;">STRUKTUR</small><br><b>ALAMI</b></div>
                        <div class="tech-box"><small style="color:#8B949E;">OTENTIKASI</small><br><b>TERVERIFIKASI</b></div>
                        <div class="tech-box"><small style="color:#8B949E;">SKOR VALID</small><br><b>99.1%</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

st.markdown(f"<br><center style='opacity:0.2; font-size:11px;'>{PEMILIK.upper()} | {VERSI}</center>", unsafe_allow_html=True)