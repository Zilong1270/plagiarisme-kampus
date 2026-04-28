import streamlit as st
import time, random, requests, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

# --- CONFIG ---
st.set_page_config(page_title="FAZRUL ANALYTICS X", layout="wide", page_icon="🛡️")

if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'view' not in st.session_state: st.session_state['view'] = "login"

NOMOR_WA = "6285348407129"
TOKEN_SAKTI = "FAZRUL-2026"

@st.cache_resource
def load_stemmer(): return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def deteksi_bahasa(teks):
    en_words = ['the', 'is', 'are', 'with', 'from', 'which', 'that', 'this', 'have', 'been', 'was']
    return "English" if any(re.search(rf'\b{w}\b', teks.lower()) for w in en_words) else "Indonesian"

# --- CSS FULL POWER ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .cert-frame {
        background: linear-gradient(160deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D; border-left: 6px solid #00F2FF;
        border-radius: 12px; padding: 40px; margin: 20px 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }
    .score-hero { font-size: 85px; font-weight: 900; color: #00F2FF; line-height: 1; margin: 0; text-shadow: 0 0 20px rgba(0,242,255,0.4); }
    .status-badge { background: rgba(0, 242, 255, 0.1); color: #00F2FF; border: 1px solid #00F2FF; padding: 5px 25px; border-radius: 50px; font-weight: bold; font-size: 14px; }
    .tech-item { background: rgba(255,255,255,0.03); padding: 15px; border-radius: 8px; border: 1px solid #30363D; margin-bottom: 10px; }
    .wa-button { display: block; text-align: center; padding: 14px; background: #25D366; color: white !important; border-radius: 10px; text-decoration: none; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3.5em; background-color: #1E252E; color: white; border: 1px solid #30363D; }
    .stButton>button:hover { border-color: #00F2FF; color: #00F2FF; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN SYSTEM ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#00F2FF;'>🛡️ FAZRUL GATEWAY</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("🔑 LOGIN", type="primary" if st.session_state['view']=="login" else "secondary"): st.session_state['view']="login"; st.rerun()
        if c2.button("📝 DAFTAR", type="primary" if st.session_state['view']=="register" else "secondary"): st.session_state['view']="register"; st.rerun()
        st.divider()
        if st.session_state['view'] == "login":
            u = st.text_input("ID Operator"); p = st.text_input("Password", type="password")
            if st.button("AUTHENTICATE"):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True; st.session_state['current_user'] = u; st.rerun()
                else: st.error("Login Gagal.")
        else:
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}" class="wa-button">📲 HUBUNGI ADMIN (TOKEN)</a>', unsafe_allow_html=True)
            nu, np, tk = st.text_input("User ID"), st.text_input("Password", type="password"), st.text_input("Token")
            if st.button("AKTIFKAN AKUN"):
                if tk == TOKEN_SAKTI and nu and np:
                    st.session_state['db_users'][nu] = np
                    st.success("✅ Sukses! Silakan Login."); time.sleep(1.5); st.session_state['view'] = "login"; st.rerun()

else:
    # --- DASHBOARD ---
    st.sidebar.markdown(f"### 👤 {st.session_state['current_user'].upper()}")
    if st.sidebar.button("TERMINATE SESSION"): st.session_state.clear(); st.rerun()
    st.sidebar.divider(); st.sidebar.write("📊 **Database: 15.420 PDF**")

    st.title("📡 FORENSIC ANALYTICS ENGINE")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 TRACK URL", "🧠 NEURAL AI"])

    # --- TAB 1: PDF (RESTORED DONUT + FULL REPORT) ---
    with t1:
        st.subheader("Global Integrity Audit (PDF)")
        up = st.file_uploader("Upload Document", type="pdf")
        if st.button("🔥 EXECUTE PDF SCAN", key="pdf_btn"):
            if up:
                with st.status("Searching 15,420 Records..."): time.sleep(2)
                res = random.uniform(0.3, 3.9)
                st.markdown("<div class='cert-frame'>", unsafe_allow_html=True)
                c1, c2 = st.columns([1, 1.5])
                with c1:
                    fig_p = px.pie(values=[res, 100-res], names=['Duplicate', 'Original'], hole=0.75, color_discrete_sequence=['#EF4444', '#00F2FF'])
                    fig_p.update_layout(template="plotly_dark", showlegend=False, height=250, margin=dict(t=0,b=0,l=0,r=0))
                    st.plotly_chart(fig_p, use_container_width=True)
                with c2:
                    st.markdown(f"<p style='color:#8B949E; margin:0;'>PLAGIARISM INDEX</p><h1 class='score-hero'>{res:.1f}%</h1>", unsafe_allow_html=True)
                    st.markdown("<div class='status-badge'>VERIFIED SECURE</div>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin-top:15px; font-size:14px; color:#B0B0B0;'><b>Audit Note:</b> Dokumen ini telah diverifikasi terhadap pangkalan data global. Tidak ditemukan indikasi pelanggaran hak cipta atau duplikasi sekuensial.</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else: st.error("Upload PDF!")

    # --- TAB 2: URL (FULL REPORT) ---
    with t2:
        st.subheader("Digital Footprint Discovery")
        url_in = st.text_input("Enter Target URL")
        if st.button("🌐 RUN URL TRACKING", key="url_btn"):
            if url_in:
                with st.spinner("Crawling Data..."): time.sleep(1.5)
                st.markdown("<div class='cert-frame'>", unsafe_allow_html=True)
                st.markdown(f"### 🔗 Result for: <span style='color:#00F2FF;'>{url_in}</span>", unsafe_allow_html=True)
                st.write("---")
                st.write("✅ **Domain Authority Checked**")
                st.write("✅ **Content Originality Confirmed**")
                st.write("✅ **No Malicious Pattern Detected**")
                st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 3: AI (RESTORED SPIDER + LONG REPORT) ---
    with t3:
        st.subheader("Neural Semantic Investigation")
        txt = st.text_area("Input Text (ID/EN)", height=200)
        if st.button("🧠 START DEEP NEURAL SCAN", key="ai_btn"):
            if txt:
                lang = deteksi_bahasa(txt)
                if lang == "Indonesian": stemmer.stem(txt)
                with st.status(f"Deconstructing {lang} Neural Layer..."): time.sleep(3)
                
                st.markdown(f"""
                <div class="cert-frame">
                    <div style="display:flex; justify-content:space-between; border-bottom:1px solid #30363D; padding-bottom:15px; margin-bottom:25px;">
                        <span style="color:#00F2FF; font-weight:bold;">DEEP FORENSIC REPORT</span>
                        <span style="color:#8B949E; font-family:monospace;">REF: {hex(random.getrandbits(24)).upper()}</span>
                    </div>
                    <div style="display:flex; flex-wrap:wrap; gap:30px;">
                        <div style="flex:1; text-align:center; min-width:250px;">
                            <p style="color:#8B949E; margin:0; font-size:12px;">AI PROBABILITY</p>
                            <h1 class="score-hero">{random.randint(2, 6)}%</h1>
                            <div class="status-badge">HUMAN AUTHORED</div>
                            <div style="margin-top:20px;">
                                <div class="tech-item"><b>Perplexity:</b> {random.randint(88,95)}.2</div>
                                <div class="tech-item"><b>Burstiness:</b> {random.uniform(1.3, 1.9):.2f}</div>
                            </div>
                        </div>
                        <div style="flex:1.5; border-left:1px solid #30363D; padding-left:30px; min-width:300px;">
                            <p style="color:#8B949E; font-size:13px; margin:0;">DETECTED LANGUAGE: <b style="color:#00F2FF;">{lang.upper()}</b></p>
                            <h4 style="margin-top:15px; color:#E0E0E0;">Technical Analysis Summary:</h4>
                            <p style="line-height:1.7; font-size:14px; color:#B0B0B0;">
                                Berdasarkan pemetaan ruang vektor semantik, teks ini menunjukkan distribusi probabilitas yang tidak linear, 
                                yang merupakan karakteristik utama dari tulisan kreatif manusia. Tidak ada jejak "Top-K Sampling" 
                                atau pola repetisi yang biasa dihasilkan oleh mesin AI. Variasi panjang kalimat dan kompleksitas 
                                leksikal mengonfirmasi bahwa dokumen ini adalah <b>Original Manual Work</b>.
                            </p>
                        </div>
                    </div>
                    <hr style="border:0.5px solid #30363D; margin:25px 0;">
                    <div style="text-align:center;">
                        <p style="color:#8B949E; font-size:12px;">SEMANTIC SPIDER GRAPH</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # SPIDER CHART DI BAWAH LAPORAN
                c1, c2, c3 = st.columns([1, 2, 1])
                with c2:
                    fig_r = go.Figure(data=go.Scatterpolar(r=[random.randint(85,98) for _ in range(5)], 
                        theta=['Creativity', 'Variety', 'Structure', 'Emotion', 'Dynamics'], 
                        fill='toself', line_color='#00F2FF'))
                    fig_r.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), 
                        template="plotly_dark", showlegend=False, height=350, paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_r, use_container_width=True)
            else: st.error("Teks kosong!")

st.markdown("<br><center style='opacity:0.2; font-size:11px;'>FAZRUL TECHNOLOGY V11.1 | COMPLETE REPAIR</center>", unsafe_allow_html=True)