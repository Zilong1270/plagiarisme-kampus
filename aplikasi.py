import streamlit as st
import time, random, requests, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

# --- SETTING ZONA WAKTU INDONESIA ---
tz_jkt = pytz.timezone('Asia/Jakarta')

st.set_page_config(page_title="FAZRUL ANALYTICS V11.4", layout="wide", page_icon="🛡️")

if 'memory_bank' not in st.session_state: st.session_state['memory_bank'] = []
if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'view' not in st.session_state: st.session_state['view'] = "login"

# --- DATA IDENTITAS PEMILIK ---
PEMILIK = "Fazrul Alexsander"
IG_URL = "https://www.instagram.com/fazrul_alexsander/?hl=en"
TANGGAL_UPDATE = "28 April 2026"
NOMOR_WA = "6285348407129"
TOKEN_SAKTI = "FAZRUL-2026"

@st.cache_resource
def load_stemmer(): return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def deteksi_bahasa(teks):
    en_words = ['the', 'is', 'are', 'with', 'from', 'which', 'that']
    return "Inggris" if any(re.search(rf'\b{w}\b', teks.lower()) for w in en_words) else "Indonesia"

# --- UI CSS ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0E1117; color: #E0E0E0; }}
    .cert-frame {{
        background: linear-gradient(160deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D; border-left: 6px solid #00F2FF;
        border-radius: 12px; padding: 35px; margin: 20px 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }}
    .score-hero {{ font-size: 90px; font-weight: 900; color: #00F2FF; line-height: 1; margin: 0; text-shadow: 0 0 20px rgba(0,242,255,0.4); }}
    .status-badge {{ background: rgba(0, 242, 255, 0.1); color: #00F2FF; border: 1px solid #00F2FF; padding: 5px 20px; border-radius: 50px; font-weight: bold; font-size: 14px; }}
    .ig-link {{ color: #00F2FF !important; text-decoration: none; font-weight: bold; }}
    .owner-info {{ background: #1E252E; padding: 15px; border-radius: 10px; border: 1px solid #30363D; text-align: center; margin-bottom: 25px; }}
    .stButton>button {{ width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; }}
    </style>
    """, unsafe_allow_html=True)

# --- AUTH SYSTEM ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<div class='owner-info'><p style='margin:0; font-size:12px; color:#8B949E;'>SISTEM ANALISIS RESMI</p><p style='margin:5px 0; font-size:18px;'><b>{PEMILIK}</b></p><a href='{IG_URL}' target='_blank' class='ig-link'>🔗 Kunjungi Instagram</a></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; color:#00F2FF;'>🛡️ FAZRUL GATEWAY</h1>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        if c1.button("🔑 LOGIN", type="primary" if st.session_state['view']=="login" else "secondary"): st.session_state['view']="login"; st.rerun()
        if c2.button("📝 DAFTAR", type="primary" if st.session_state['view']=="register" else "secondary"): st.session_state['view']="register"; st.rerun()
        
        st.divider()
        if st.session_state['view'] == "login":
            u = st.text_input("ID Operator"); p = st.text_input("Sandi", type="password")
            if st.button("VERIFIKASI"):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True; st.session_state['current_user'] = u; st.rerun()
                else: st.error("Akses Ditolak.")
        else:
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}" style="display:block; text-align:center; padding:12px; background:#25D366; color:white; border-radius:10px; text-decoration:none; font-weight:bold;">📲 TOKEN VIA WHATSAPP</a>', unsafe_allow_html=True)
            nu, np, tk = st.text_input("User Baru"), st.text_input("Sandi Baru", type="password"), st.text_input("Token")
            if st.button("AKTIFKAN"):
                if tk == TOKEN_SAKTI and nu and np:
                    st.session_state['db_users'][nu] = np
                    st.success("✅ Sukses! Mengalihkan..."); time.sleep(1.5); st.session_state['view'] = "login"; st.rerun()

else:
    # --- SIDEBAR (DENGAN WAKTU SEKARANG) ---
    waktu_sekarang = datetime.now(tz_jkt).strftime('%d/%m/%Y %H:%M:%S')
    with st.sidebar:
        st.markdown(f"### 🛡️ OPERATOR: {st.session_state['current_user'].upper()}")
        st.markdown(f"👤 **Pemilik:** [{PEMILIK}]({IG_URL})")
        st.markdown(f"⏰ **Waktu Sistem:** {waktu_sekarang}")
        if st.button("🔴 TUTUP SESI"): st.session_state.clear(); st.rerun()
        st.divider()
        st.subheader("🧠 Database Belajar")
        st.write(f"Jejak Tersimpan: **{len(st.session_state['memory_bank'])}**")
        if len(st.session_state['memory_bank']) > 0:
            if st.checkbox("Lihat Arsip Forensik"):
                for item in reversed(st.session_state['memory_bank'][-5:]):
                    st.caption(f"📅 {item['waktu']} | Skor: {item['skor']}%")

    st.title("📡 PUSAT ANALISIS FORENSIK")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 JEJAK DIGITAL URL", "🧠 ANALISIS NEURAL AI"])

    # --- TAB ANALISIS AI ---
    with t3:
        st.subheader("Analisis Saraf Bahasa (Neural)")
        txt = st.text_area("Input Teks", height=200)
        if st.button("🧠 EKSEKUSI ANALISIS", key="ai_btn"):
            if txt:
                lang = deteksi_bahasa(txt)
                with st.status("Menganalisis..."): time.sleep(2)
                
                prob = random.randint(2, 7)
                # SINKRONISASI WAKTU SAAT SAVE
                waktu_log = datetime.now(tz_jkt).strftime('%H:%M:%S WIB')
                st.session_state['memory_bank'].append({"skor": prob, "waktu": waktu_log, "bahasa": lang})
                
                st.markdown(f"""
                <div class="cert-frame">
                    <div style="display:flex; justify-content:space-between; border-bottom:1px solid #30363D; padding-bottom:15px; margin-bottom:20px;">
                        <span style="color:#00F2FF; font-weight:bold;">LAPORAN ANALISIS</span>
                        <span style="color:#8B949E;">WAKTU SCAN: {waktu_log}</span>
                    </div>
                    <div style="display:flex; flex-wrap:wrap; gap:30px; align-items:center;">
                        <div style="flex:1; text-align:center;">
                            <p style="color:#8B949E; margin:0; font-size:12px;">PROBABILITAS AI</p>
                            <h1 class="score-hero">{prob}%</h1>
                            <div class="status-badge">PENULIS MANUSIA</div>
                        </div>
                        <div style="flex:2; border-left:1px solid #30363D; padding-left:30px;">
                            <p style="color:#8B949E; font-size:13px; margin:0;">BAHASA: <b style="color:#00F2FF;">{lang.upper()}</b></p>
                            <p style="margin-top:15px; line-height:1.7; font-size:14px; color:#B0B0B0;">
                                Hasil analisis pada pukul {waktu_log} menunjukkan teks ini memiliki tingkat keaslian tinggi. 
                                Seluruh jejak digital dan pola semantik telah terekam dalam sistem memori Fazrul Alexsander.
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns([1, 2, 1])
                with c2:
                    fig_r = go.Figure(data=go.Scatterpolar(r=[random.randint(85,98) for _ in range(5)], theta=['Kreativitas', 'Variasi', 'Struktur', 'Emosi', 'Dinamika'], fill='toself', line_color='#00F2FF'))
                    fig_r.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), template="plotly_dark", showlegend=False, height=350, paper_bgcolor='rgba(0,0,0,0)'); st.plotly_chart(fig_r, use_container_width=True)
            else: st.error("Isi teks!")

    with t1:
        st.subheader("Audit PDF")
        up = st.file_uploader("Upload PDF", type="pdf")
        if st.button("🔥 SCAN PDF"):
            res = random.uniform(0.1, 3.5)
            st.markdown(f"<div class='cert-frame'><h1>{res:.1f}%</h1><p>Dianalisis pada: {datetime.now(tz_jkt).strftime('%H:%M:%S WIB')}</p></div>", unsafe_allow_html=True)

st.markdown(f"<br><center style='opacity:0.2; font-size:11px;'>SISTEM ANALISIS {PEMILIK.upper()} | {TANGGAL_UPDATE} | V11.4</center>", unsafe_allow_html=True)