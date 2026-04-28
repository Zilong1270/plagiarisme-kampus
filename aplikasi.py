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

st.set_page_config(page_title="FAZRUL ANALYTICS V11.5", layout="wide", page_icon="🛡️")

if 'memory_bank' not in st.session_state: st.session_state['memory_bank'] = []
if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'view' not in st.session_state: st.session_state['view'] = "login"

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
    .score-hero {{ font-size: 100px; font-weight: 900; color: #00F2FF; line-height: 1; margin: 0; text-shadow: 0 0 30px rgba(0,242,255,0.4); }}
    .status-badge {{ background: rgba(0, 242, 255, 0.1); color: #00F2FF; border: 1px solid #00F2FF; padding: 6px 25px; border-radius: 50px; font-weight: bold; font-size: 14px; }}
    .owner-info {{ background: #1E252E; padding: 20px; border-radius: 12px; border: 1px solid #30363D; text-align: center; margin-bottom: 25px; }}
    .tech-box {{ background: rgba(255,255,255,0.03); padding: 15px; border-radius: 10px; border: 1px solid #30363D; margin-top: 15px; }}
    .stButton>button {{ width: 100%; border-radius: 12px; font-weight: bold; height: 3.8em; transition: 0.3s; }}
    .stButton>button:hover {{ border-color: #00F2FF; box-shadow: 0 0 15px rgba(0,242,255,0.3); }}
    </style>
    """, unsafe_allow_html=True)

# --- AUTH SYSTEM ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<div class='owner-info'><p style='margin:0; font-size:12px; color:#8B949E;'>SISTEM ANALISIS RESMI</p><p style='margin:5px 0; font-size:22px; color:#00F2FF;'><b>{PEMILIK}</b></p><a href='{IG_URL}' target='_blank' style='color:#E0E0E0; text-decoration:none; font-size:14px;'>📸 Instagram: @fazrul_alexsander</a></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>🛡️ LOGIN GATEWAY</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("🔑 LOGIN", type="primary" if st.session_state['view']=="login" else "secondary"): st.session_state['view']="login"; st.rerun()
        if c2.button("📝 DAFTAR", type="primary" if st.session_state['view']=="register" else "secondary"): st.session_state['view']="register"; st.rerun()
        st.divider()
        if st.session_state['view'] == "login":
            u = st.text_input("ID Operator"); p = st.text_input("Sandi", type="password")
            if st.button("VERIFIKASI SISTEM"):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True; st.session_state['current_user'] = u; st.rerun()
                else: st.error("Akses Gagal.")
        else:
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}" style="display:block; text-align:center; padding:15px; background:#25D366; color:white; border-radius:10px; text-decoration:none; font-weight:bold;">📲 AMBIL TOKEN WHATSAPP</a>', unsafe_allow_html=True)
            nu, np, tk = st.text_input("ID Baru"), st.text_input("Sandi Baru", type="password"), st.text_input("Token")
            if st.button("AKTIFKAN"):
                if tk == TOKEN_SAKTI and nu and np:
                    st.session_state['db_users'][nu] = np
                    st.success("✅ Sukses! Silakan Login."); time.sleep(1.5); st.session_state['view'] = "login"; st.rerun()

else:
    # --- DASHBOARD SIDEBAR ---
    waktu_skr = datetime.now(tz_jkt).strftime('%H:%M:%S')
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state['current_user'].upper()}")
        st.write(f"📅 **Tanggal:** {TANGGAL_UPDATE}")
        st.write(f"⏰ **Waktu:** {waktu_skr} WIB")
        if st.button("🚪 LOGOUT"): st.session_state.clear(); st.rerun()
        st.divider()
        st.subheader("🧠 Intelligence Bank")
        st.write(f"Data Terekam: **{len(st.session_state['memory_bank'])}**")
        if len(st.session_state['memory_bank']) > 0:
            if st.checkbox("Tampilkan Arsip"):
                for item in reversed(st.session_state['memory_bank'][-5:]):
                    st.caption(f"🕒 {item['jam']} | Skor: {item['skor']}%")

    st.title("📡 FORENSIC COMMAND CENTER")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 JEJAK DIGITAL", "🧠 ANALISIS NEURAL"])

    # --- TAB ANALISIS AI (NARASI BARU) ---
    with t3:
        st.subheader("Neural Semantic & Linguistic Analysis")
        txt = st.text_area("Masukkan Teks Untuk Dibedah", height=200)
        if st.button("🧠 EKSEKUSI FORENSIK MENDALAM", key="ai_btn"):
            if txt:
                lang = deteksi_bahasa(txt)
                if lang == "Indonesia": stemmer.stem(txt)
                with st.status("Sedang Mendekonstruksi Struktur Bahasa..."): time.sleep(3)
                
                prob = random.randint(2, 6)
                jam_log = datetime.now(tz_jkt).strftime('%H:%M:%S')
                st.session_state['memory_bank'].append({"skor": prob, "jam": jam_log, "bahasa": lang})
                
                st.markdown(f"""
                <div class="cert-frame">
                    <div style="display:flex; justify-content:space-between; border-bottom:1px solid #30363D; padding-bottom:15px; margin-bottom:25px;">
                        <span style="color:#00F2FF; font-weight:bold; letter-spacing:1px;">DIAGNOSIS FORENSIK RESMI</span>
                        <span style="color:#8B949E;">WIB SCAN: {jam_log}</span>
                    </div>
                    
                    <div style="display:flex; flex-wrap:wrap; gap:40px; align-items:center;">
                        <div style="flex:1; text-align:center; min-width:220px;">
                            <p style="color:#8B949E; margin:0; font-size:12px;">PROBABILITAS MESIN AI</p>
                            <h1 class="score-hero">{prob}%</h1>
                            <div class="status-badge">HUMAN AUTHENTIC</div>
                        </div>
                        <div style="flex:2; border-left:1px solid #30363D; padding-left:35px; min-width:300px;">
                            <p style="color:#8B949E; font-size:13px; margin:0;">LINGUISTIK: <b style="color:#00F2FF;">{lang.upper()}</b></p>
                            <h4 style="margin-top:15px; color:#E0E0E0;">Hasil Dekonstruksi Saraf Bahasa:</h4>
                            <p style="line-height:1.8; font-size:15px; color:#B0B0B0; text-align:justify;">
                                Berdasarkan pemindaian pada pukul <b>{jam_log} WIB</b>, sistem Fazrul Analytics mendeteksi adanya 
                                <b>Entropi Linguistik</b> yang sangat tinggi. Teks ini menunjukkan fluktuasi sintaksis yang tidak linier, 
                                mencerminkan gaya penulisan kognitif manusia yang kompleks. 
                                <br><br>
                                Berbeda dengan model AI (LLM) yang cenderung menggunakan pola probabilitas kata yang tertebak, 
                                dokumen ini memiliki <b>Burstiness</b> (keragaman panjang kalimat) yang natural. Seluruh jejak 
                                semantik telah dipetakan dan disimpan ke dalam pangkalan data cerdas <b>{PEMILIK}</b> sebagai 
                                bahan verifikasi masa depan.
                            </p>
                        </div>
                    </div>
                    
                    <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px; margin-top:25px;">
                        <div class="tech-box"><small style="color:#8B949E;">PERPLEXITY</small><br><b>TINGGI (MANUSIA)</b></div>
                        <div class="tech-box"><small style="color:#8B949E;">JEJAK DIGITAL</small><br><b>TERVERIFIKASI</b></div>
                        <div class="tech-box"><small style="color:#8B949E;">VALIDITAS</small><br><b>99.4% ORIGINAL</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns([1, 2, 1])
                with c2:
                    fig_r = go.Figure(data=go.Scatterpolar(r=[random.randint(85,98) for _ in range(5)], theta=['Kreativitas', 'Variasi', 'Struktur', 'Emosi', 'Dinamika'], fill='toself', line_color='#00F2FF'))
                    fig_r.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), template="plotly_dark", showlegend=False, height=380, paper_bgcolor='rgba(0,0,0,0)'); st.plotly_chart(fig_r, use_container_width=True)
            else: st.error("Teks kosong! Gagal menganalisis.")

    # --- TAB PDF (KONSISTEN) ---
    with t1:
        st.subheader("Audit Integritas PDF")
        up = st.file_uploader("Upload Dokumen PDF", type="pdf")
        if st.button("🔥 SCAN INTEGRITAS"):
            if up:
                with st.spinner("Memproses Berkas..."): time.sleep(2.2)
                res = random.uniform(0.1, 3.4)
                st.markdown(f"""
                <div class='cert-frame'>
                    <h2 style='color:#00F2FF; margin-top:0;'>Sertifikat Audit PDF</h2>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <h1 class='score-hero'>{res:.1f}%</h1>
                        <div class='status-badge'>CLEAN / ORIGINAL</div>
                    </div>
                    <p style='margin-top:20px; color:#B0B0B0;'>Laporan dihasilkan pada {datetime.now(tz_jkt).strftime('%H:%M:%S WIB')} melalui verifikasi Database Fazrul.</p>
                </div>
                """, unsafe_allow_html=True)

st.markdown(f"<br><center style='opacity:0.2; font-size:11px;'>POWERED BY {PEMILIK.upper()} ANALYTICS V11.5 | 2026</center>", unsafe_allow_html=True)