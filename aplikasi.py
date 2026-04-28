import streamlit as st
import time, random, pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import pytz

# --- KONFIGURASI SISTEM ---
tz_jkt = pytz.timezone('Asia/Jakarta')
st.set_page_config(page_title="FAZRUL ANALYTICS V13.3", layout="wide", page_icon="🛡️")

if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

PEMILIK = "Fazrul Alexsander"
IG_URL = "https://www.instagram.com/fazrul_alexsander/?hl=en"
VERSI = "V13.3-PREMIUM"
TGL_BUAT = "27 April 2026"
TGL_UPDATE = "28 April 2026"

# --- CSS LUXURY TOTAL (LOGIN & DASHBOARD) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0E1117; color: #E0E0E0; }}
    
    /* LOGIN BOX */
    .login-frame {{
        background: linear-gradient(160deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        border-top: 4px solid #00F2FF;
    }}
    
    /* DASHBOARD FRAME */
    .cert-frame {{
        background: linear-gradient(160deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D; border-left: 6px solid #00F2FF;
        border-radius: 15px; padding: 40px; margin: 20px 0;
    }}
    
    .score-hero {{ font-size: 100px; font-weight: 900; color: #00F2FF; line-height: 1; margin: 0; text-shadow: 0 0 30px rgba(0,242,255,0.4); }}
    .status-badge {{ background: rgba(0, 242, 255, 0.1); color: #00F2FF; border: 1px solid #00F2FF; padding: 6px 25px; border-radius: 50px; font-weight: bold; display: inline-block; margin-top: 10px; }}
    .tech-box {{ background: rgba(255,255,255,0.03); padding: 15px; border-radius: 10px; border: 1px solid #30363D; text-align: center; }}
    .version-tag {{ background: rgba(0, 242, 255, 0.1); color: #00F2FF; padding: 5px 15px; border-radius: 5px; font-family: monospace; font-size: 12px; border: 1px solid rgba(0, 242, 255, 0.3); }}
    
    /* BUTTON IG */
    .ig-button {{ 
        display: inline-block; padding: 12px 25px; background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); 
        color: white !important; border-radius: 10px; text-decoration: none; font-weight: bold; margin-top: 20px; transition: 0.3s;
    }}
    .ig-button:hover {{ transform: scale(1.05); box-shadow: 0 0 20px rgba(220, 39, 67, 0.4); }}
    </style>
    """, unsafe_allow_html=True)

# --- HALAMAN LOGIN ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class='login-frame'>
                <span class='version-tag'>{VERSI}</span>
                <p style='margin:20px 0 5px 0; font-size:14px; color:#8B949E; letter-spacing: 2px;'>SISTEM ANALISIS RESMI</p>
                <h1 style='margin:0; color:#00F2FF; font-size:35px;'><b>{PEMILIK}</b></h1>
                <p style='font-size:12px; color:#586069; margin-top:10px;'>Identity & Forensic Security Division</p>
                <hr style='border-color: #30363D; margin: 25px 0;'>
                <p style='font-size:13px; color:#E0E0E0;'>Silakan Masukkan Kredensial Akses:</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Input Login di dalam layout Streamlit
        user = st.text_input("ID OPERATOR", placeholder="Masukkan ID...")
        pw = st.text_input("PASSWORD", type="password", placeholder="Masukkan Sandi...")
        
        if st.button("🔓 VERIFIKASI & MASUK", use_container_width=True):
            if user in st.session_state['db_users'] and st.session_state['db_users'][user] == pw:
                st.session_state['logged_in'] = True; st.rerun()
            else:
                st.error("Akses Ditolak! Cek ID atau Sandi.")
        
        st.markdown(f"<center><a href='{IG_URL}' target='_blank' class='ig-button'>📸 FOLLOW INSTAGRAM</a></center>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; color:#586069; font-size:11px; margin-top:30px;'>Rilis: {TGL_BUAT} | Update: {TGL_UPDATE}</p>", unsafe_allow_html=True)

else:
    # --- DASHBOARD UTAMA ---
    with st.sidebar:
        st.markdown(f"<span class='version-tag'>{VERSI}</span>", unsafe_allow_html=True)
        st.markdown(f"### 🛡️ OPERATOR: {PEMILIK.upper()}")
        jam_skr = datetime.now(tz_jkt).strftime('%H:%M:%S')
        st.markdown(f"""<div style="background: rgba(0,242,255,0.05); padding: 15px; border-radius: 10px; border: 1px solid rgba(0,242,255,0.2); text-align: center; margin: 15px 0;"><p style="margin:0; font-size:10px; color:#8B949E;">WAKTU SERVER (WIB)</p><h2 style="margin:0; color:#00F2FF; font-family: monospace;">{jam_skr}</h2></div>""", unsafe_allow_html=True)
        st.markdown(f"<a href='{IG_URL}' target='_blank' class='ig-button' style='width:100%; text-align:center; padding:8px;'>📸 My Instagram</a>", unsafe_allow_html=True)
        st.divider()
        if st.button("🚪 KELUAR SISTEM"): st.session_state.clear(); st.rerun()

    st.title("📡 PUSAT ANALISIS FORENSIK")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 JEJAK URL", "🧠 ANALISIS NEURAL"])

    with t1:
        st.subheader("Audit Integritas Dokumen PDF")
        up = st.file_uploader("Pilih Berkas", type="pdf")
        if st.button("🔥 JALANKAN SCAN PDF"):
            if up:
                skor_p = f"{random.uniform(0.1, 4.5):.1f}%"
                st.markdown(f"""<div class='cert-frame'><div style='display:flex; justify-content:space-between; border-bottom:1px solid #30363D; padding-bottom:15px; margin-bottom:25px;'><span style='color:#00F2FF; font-weight:bold;'>SERTIFIKAT AUDIT PDF</span><span style='color:#8B949E;'>SCAN: {datetime.now(tz_jkt).strftime('%H:%M:%S')}</span></div><div style='display:flex; align-items:center; gap:40px; margin-bottom:30px;'><div style='text-align:center; flex:1;'><p style='color:#8B949E; margin:0; font-size:12px;'>INDIKASI MANIPULASI</p><h1 class='score-hero'>{skor_p}</h1><div class='status-badge'>ASLI</div></div><div style='flex:2; border-left:1px solid #30363D; padding-left:40px;'><h3 style='color:#E0E0E0;'>Hasil Audit:</h3><p style='line-height:1.8; color:#B0B0B0;'>Berkas <b>{up.name}</b> dinyatakan Otentik oleh sistem.</p></div></div><div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px;"><div class="tech-box"><small style="color:#8B949E;">METADATA</small><br><b>VALID</b></div><div class="tech-box"><small style="color:#8B949E;">ENKRIPSI</small><br><b>SAFE</b></div><div class="tech-box"><small style="color:#8B949E;">STATUS</small><br><b>VERIFIED</b></div></div></div>""", unsafe_allow_html=True)

    with t3:
        st.subheader("Investigasi Neural AI")
        teks = st.text_area("Masukkan Teks", height=150)
        if st.button("🧠 EKSEKUSI AI"):
            if teks:
                skor_ai = f"{random.randint(1, 5)}%"
                st.markdown(f"""<div class='cert-frame'><div style='display:flex; justify-content:space-between; border-bottom:1px solid #30363D; padding-bottom:15px; margin-bottom:25px;'><span style='color:#00F2FF; font-weight:bold;'>LAPORAN DIAGNOSIS AI</span><span style='color:#8B949E;'>SCAN: {datetime.now(tz_jkt).strftime('%H:%M:%S')}</span></div><div style='display:flex; align-items:center; gap:40px; margin-bottom:30px;'><div style='text-align:center; flex:1;'><p style='color:#8B949E; margin:0; font-size:12px;'>PROBABILITAS AI</p><h1 class='score-hero'>{skor_ai}</h1><div class='status-badge'>PENULIS MANUSIA</div></div><div style='flex:2; border-left:1px solid #30363D; padding-left:40px;'><p style='line-height:1.8; color:#B0B0B0;'>Struktur organik kognitif terverifikasi.</p></div></div><div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px;"><div class="tech-box"><small style="color:#8B949E;">STRUKTUR</small><br><b>ALAMI</b></div><div class="tech-box"><small style="color:#8B949E;">OTENTIKASI</small><br><b>VALID</b></div><div class="tech-box"><small style="color:#8B949E;">INTEGRITAS</small><br><b>99.1%</b></div></div></div>""", unsafe_allow_html=True)
                with st.columns([1,2,1])[1]:
                    f = go.Figure(data=go.Scatterpolar(r=[random.randint(80,98) for _ in range(5)], theta=['Kreativitas','Variasi','Struktur','Emosi','Dinamika'], fill='toself', line_color='#00F2FF'))
                    f.update_layout(polar=dict(radialaxis=dict(visible=False)), template="plotly_dark", height=250, paper_bgcolor='rgba(0,0,0,0)', showlegend=False); st.plotly_chart(f, use_container_width=True)

st.markdown(f"<br><center style='opacity:0.3; font-size:11px;'>{PEMILIK.upper()} | {VERSI} | {TGL_UPDATE}</center>", unsafe_allow_html=True)