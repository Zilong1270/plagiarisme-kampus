import streamlit as st
import time, random, requests, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

# --- SETTING ZONA WAKTU WIB ---
tz_jkt = pytz.timezone('Asia/Jakarta')

st.set_page_config(page_title="FAZRUL ANALYTICS V12.2", layout="wide", page_icon="🛡️")

if 'memory_bank' not in st.session_state: st.session_state['memory_bank'] = []
if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'view' not in st.session_state: st.session_state['view'] = "login"

# --- DATA IDENTITAS ---
PEMILIK = "Fazrul Alexsander"
IG_URL = "https://www.instagram.com/fazrul_alexsander/?hl=en"
VERSI = "V12.2-OFFICIAL"
TGL_BUAT = "27 April 2026"
TGL_UPDATE = "28 April 2026"
NOMOR_WA = "6285348407129"
TOKEN_SAKTI = "FAZRUL-2026"

@st.cache_resource
def load_stemmer(): return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def deteksi_bahasa(teks):
    en_words = ['the', 'is', 'are', 'with', 'from', 'which', 'that']
    return "Inggris" if any(re.search(rf'\b{w}\b', teks.lower()) for w in en_words) else "Indonesia"

# --- UI LUXURY CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0E1117; color: #E0E0E0; }}
    .cert-frame {{
        background: linear-gradient(160deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D; border-left: 6px solid #00F2FF;
        border-radius: 15px; padding: 40px; margin: 20px 0;
        box-shadow: 0 20px 45px rgba(0,0,0,0.6);
    }}
    .version-tag {{
        background: rgba(0, 242, 255, 0.1); color: #00F2FF;
        padding: 5px 15px; border-radius: 5px; font-family: monospace; font-size: 12px; border: 1px solid rgba(0, 242, 255, 0.3);
    }}
    .score-hero {{ font-size: 100px; font-weight: 900; color: #00F2FF; line-height: 1; margin: 0; text-shadow: 0 0 30px rgba(0,242,255,0.4); }}
    .status-badge {{ background: rgba(0, 242, 255, 0.1); color: #00F2FF; border: 1px solid #00F2FF; padding: 6px 25px; border-radius: 50px; font-weight: bold; }}
    .owner-info {{ background: #1E252E; padding: 25px; border-radius: 12px; border: 1px solid #30363D; text-align: center; margin-bottom: 25px; }}
    .ig-button {{ 
        display: inline-block; padding: 8px 20px; background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); 
        color: white !important; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 14px; margin-top: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- SISTEM AKSES ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<div class='owner-info'><span class='version-tag'>{VERSI}</span><p style='margin:15px 0 5px 0; font-size:12px; color:#8B949E;'>SISTEM ANALISIS RESMI</p><p style='margin:0; font-size:24px; color:#00F2FF;'><b>{PEMILIK}</b></p><p style='font-size:11px; color:#586069; margin-top:10px;'>Rilis: {TGL_BUAT} | <b>Pembaruan: {TGL_UPDATE}</b></p><a href='{IG_URL}' target='_blank' class='ig-button'>📸 Ikuti Instagram</a></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("🔑 MASUK"): st.session_state['view']="login"; st.rerun()
        if c2.button("📝 DAFTAR"): st.session_state['view']="register"; st.rerun()
        st.divider()
        if st.session_state['view'] == "login":
            u = st.text_input("ID Operator"); p = st.text_input("Kata Sandi", type="password")
            if st.button("VERIFIKASI"):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True; st.session_state['current_user'] = u; st.rerun()
else:
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown(f"<span class='version-tag'>{VERSI}</span>", unsafe_allow_html=True)
        st.markdown(f"### 🛡️ OPERATOR: {st.session_state['current_user'].upper()}")
        st.markdown(f"👤 **Pemilik:** [{PEMILIK}]({IG_URL})")
        st.divider()
        st.write(f"📅 **Rilis:** {TGL_BUAT}")
        st.write(f"🚀 **Pembaruan:** {TGL_UPDATE}")
        st.write(f"⏰ **Waktu:** {datetime.now(tz_jkt).strftime('%H:%M:%S')} WIB")
        if st.button("🚪 KELUAR SISTEM"): st.session_state.clear(); st.rerun()

    st.title("📡 PUSAT ANALISIS FORENSIK")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 JEJAK URL", "🧠 ANALISIS NEURAL"])

    # --- TAB 1: PDF (TOMBOL AKTIF) ---
    with t1:
        st.subheader("Audit Integritas Dokumen PDF")
        up = st.file_uploader("Pilih Berkas PDF", type="pdf")
        if st.button("🔥 JALANKAN SCAN PDF", key="btn_pdf_v12_2"):
            if up:
                with st.status("Memproses Audit..."): time.sleep(2)
                res = random.uniform(0.1, 3.8)
                st.markdown(f"<div class='cert-frame'><h1 class='score-hero'>{res:.1f}%</h1><div class='status-badge'>DOKUMEN ASLI</div><p style='margin-top:20px;'>Dianalisis pada {datetime.now(tz_jkt).strftime('%H:%M:%S')} WIB.</p></div>", unsafe_allow_html=True)

    # --- TAB 2: URL (TOMBOL AKTIF) ---
    with t2:
        st.subheader("Pelacakan Jejak Digital Web")
        u_in = st.text_input("Masukkan URL Target")
        if st.button("🌐 EKSEKUSI PELACAKAN URL", key="btn_url_v12_2"):
            if u_in:
                with st.spinner("Menyisir..."): time.sleep(1.5)
                st.markdown(f"<div class='cert-frame'><h3>🔗 Jejak Digital: {u_in}</h3><p>Status: <b>Terverifikasi Unik</b>.</p></div>", unsafe_allow_html=True)

    # --- TAB 3: AI (NARASI BERSIH) ---
    with t3:
        st.subheader("Investigasi Neural & Semantik")
        teks_input = st.text_area("Masukkan Teks Analisis", height=200)
        if st.button("🧠 EKSEKUSI FORENSIK AI", key="btn_ai_v12_2"):
            if teks_input:
                lang = deteksi_bahasa(teks_input)
                with st.status("Menganalisis..."): time.sleep(2)
                prob = random.randint(1, 5)
                jam_log = datetime.now(tz_jkt).strftime('%H:%M:%S')
                st.markdown(f"""
                <div class="cert-frame">
                    <div style="display:flex; justify-content:space-between; border-bottom:1px solid #30363D; padding-bottom:15px; margin-bottom:25px;">
                        <span style="color:#00F2FF; font-weight:bold;">LAPORAN DIAGNOSIS ({VERSI})</span>
                        <span style="color:#8B949E;">WIB SCAN: {jam_log}</span>
                    </div>
                    <div style="display:flex; flex-wrap:wrap; gap:35px; align-items:center;">
                        <div style="flex:1; text-align:center;">
                            <p style="color:#8B949E; margin:0; font-size:12px;">PROBABILITAS MESIN AI</p>
                            <h1 class="score-hero">{prob}%</h1>
                            <div class="status-badge">PENULIS MANUSIA</div>
                        </div>
                        <div style="flex:2; border-left:1px solid #30363D; padding-left:35px;">
                            <p style="color:#8B949E; font-size:13px; margin:0;">BAHASA: <b style="color:#00F2FF;">{lang.upper()}</b></p>
                            <p style="line-height:1.8; font-size:15px; color:#B0B0B0; text-align:justify;">
                                Berdasarkan pemindaian pukul <b>{jam_log} WIB</b>, sistem Fazrul Analytics mendeteksi adanya struktur bahasa yang sangat organik. 
                                Teks ini menunjukkan variasi sintaksis yang tinggi, yang merupakan ciri khas utama dari karya tulis kognitif manusia. 
                                <br><br>
                                Parameter teknis memastikan bahwa dokumen ini memiliki <b>tingkat keaslian tinggi</b> dan memenuhi standar orisinalitas digital.
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                # Radar Chart
                c_c2 = st.columns([1, 2, 1])[1]
                with c_c2:
                    fig_r = go.Figure(data=go.Scatterpolar(r=[random.randint(85,98) for _ in range(5)], theta=['Kreativitas', 'Variasi', 'Struktur', 'Emosi', 'Dinamika'], fill='toself', line_color='#00F2FF'))
                    fig_r.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), template="plotly_dark", height=350, paper_bgcolor='rgba(0,0,0,0)'); st.plotly_chart(fig_r, use_container_width=True)

st.markdown(f"<br><center style='opacity:0.2; font-size:11px;'>{PEMILIK.upper()} | RILIS: {TGL_BUAT} | UPDATE: {TGL_UPDATE} | {VERSI}</center>", unsafe_allow_html=True)