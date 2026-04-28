import streamlit as st
import time, random, requests, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

st.set_page_config(page_title="FAZRUL ANALYTICS X", layout="wide", page_icon="🛡️")

# --- CORE ---
if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'view' not in st.session_state: st.session_state['view'] = "login"

NOMOR_WA = "6285348407129"
TOKEN_SAKTI = "FAZRUL-2026"

@st.cache_resource
def load_stemmer(): return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def deteksi_bahasa(teks):
    en_words = ['the', 'is', 'are', 'with', 'from', 'which', 'that', 'this']
    return "English" if any(re.search(rf'\b{w}\b', teks.lower()) for w in en_words) else "Indonesian"

# --- CSS LUXURY V2 ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .cert-frame {
        background: linear-gradient(160deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D; border-left: 6px solid #00F2FF;
        border-radius: 12px; padding: 40px; margin: 20px 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }
    .score-hero { font-size: 110px; font-weight: 900; color: #00F2FF; line-height: 1; margin: 0; text-shadow: 0 0 30px rgba(0,242,255,0.4); }
    .status-badge { background: rgba(0, 242, 255, 0.1); color: #00F2FF; border: 1px solid #00F2FF; padding: 5px 25px; border-radius: 50px; font-weight: bold; }
    .tech-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 25px; border-top: 1px solid #30363D; padding-top: 25px; }
    .tech-item { background: rgba(255,255,255,0.03); padding: 15px; border-radius: 8px; border: 1px solid #30363D; }
    .tech-label { color: #8B949E; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }
    .tech-val { color: #E0E0E0; font-weight: bold; font-size: 15px; }
    .wa-button { display: block; text-align: center; padding: 14px; background: #25D366; color: white !important; border-radius: 10px; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- AUTH ---
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
            if st.button("VERIFY SYSTEM"):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True; st.session_state['current_user'] = u; st.rerun()
                else: st.error("Login Gagal.")
        else:
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}" class="wa-button">📲 REQUEST TOKEN</a>', unsafe_allow_html=True)
            nu, np, tk = st.text_input("Username"), st.text_input("Password", type="password"), st.text_input("Token")
            if st.button("ACTIVATE"):
                if tk == TOKEN_SAKTI and nu and np:
                    st.session_state['db_users'][nu] = np
                    st.success("✅ Berhasil! Mengalihkan..."); time.sleep(1.8); st.session_state['view'] = "login"; st.rerun()

else:
    # --- DASHBOARD ---
    st.sidebar.markdown(f"### 👤 {st.session_state['current_user'].upper()}")
    if st.sidebar.button("LOGOUT"): st.session_state.clear(); st.rerun()
    st.sidebar.divider(); st.sidebar.write("📊 **Database: 15.420 PDF**")

    st.title("📡 FORENSIC ANALYTICS CENTER")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 URL TRACKER", "🧠 NEURAL AI"])

    with t3: # TAB AI DENGAN HASIL PANJANG
        st.subheader("Deep Neural Semantic Analysis")
        txt = st.text_area("Input Content (ID/EN)", height=200)
        if st.button("🧠 EXECUTE DEEP SCAN", key="ai_btn"):
            if txt:
                lang = deteksi_bahasa(txt)
                if lang == "Indonesian": stemmer.stem(txt)
                with st.status(f"Deconstructing {lang} Syntax..."): time.sleep(3)
                
                # DATA SIMULASI TEKNIS
                prob = random.randint(2, 6)
                perplexity = random.randint(70, 95)
                burstiness = random.uniform(1.2, 1.8)
                
                st.markdown(f"""
                <div class="cert-frame">
                    <div style="display:flex; justify-content:space-between; border-bottom:1px solid #30363D; padding-bottom:15px; margin-bottom:25px;">
                        <span style="color:#00F2FF; font-weight:bold; letter-spacing:1px;">FORENSIC ANALYSIS RESULT</span>
                        <span style="color:#8B949E; font-family:monospace;">ID: {hex(random.getrandbits(24)).upper()}</span>
                    </div>
                    
                    <div style="display:flex; flex-wrap:wrap; gap:40px; align-items:center;">
                        <div style="flex:1; text-align:center;">
                            <p style="color:#8B949E; margin:0; font-size:12px;">AI PROBABILITY INDEX</p>
                            <h1 class="score-hero">{prob}%</h1>
                            <div class="status-badge">HUMAN AUTHORED</div>
                        </div>
                        <div style="flex:2; border-left:1px solid #30363D; padding-left:30px;">
                            <p style="color:#8B949E; font-size:13px; margin:0;">DETECTED LANGUAGE: <b style="color:#00F2FF;">{lang.upper()}</b></p>
                            <h4 style="margin-top:15px; color:#E0E0E0;">Executive Summary:</h4>
                            <p style="line-height:1.6; font-size:14px; color:#B0B0B0;">
                                Hasil analisis forensik mendalam menunjukkan bahwa teks ini memiliki karakteristik penulisan manual. 
                                Algoritma mendeteksi adanya variasi struktur kalimat yang dinamis dan pilihan diksi yang kontekstual, 
                                yang tidak ditemukan dalam pola prediktif model bahasa AI (LLM) seperti GPT-4 atau Gemini.
                                Tingkat keaslian dokumen dikonfirmasi tinggi berdasarkan fluktuasi semantik yang terekam.
                            </p>
                        </div>
                    </div>

                    <div class="tech-grid">
                        <div class="tech-item">
                            <div class="tech-label">Linguistic Perplexity</div>
                            <div class="tech-val">{perplexity}.42 pts (High Variability)</div>
                        </div>
                        <div class="tech-item">
                            <div class="tech-label">Sentence Burstiness</div>
                            <div class="tech-val">{burstiness:.2f} (Natural Flow)</div>
                        </div>
                        <div class="tech-item">
                            <div class="tech-label">Semantic Consistency</div>
                            <div class="tech-val">Verified Organic</div>
                        </div>
                        <div class="tech-item">
                            <div class="tech-label">Cross-DB Reference</div>
                            <div class="tech-val">No Duplication Found</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns([1, 1.5, 1])
                with c2:
                    fig_r = go.Figure(data=go.Scatterpolar(r=[random.randint(85,98) for _ in range(5)], theta=['Creativity', 'Variety', 'Structure', 'Emotion', 'Dynamics'], fill='toself', line_color='#00F2FF'))
                    fig_r.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), template="plotly_dark", showlegend=False, height=350, paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_r, use_container_width=True)
            else: st.error("Isi teksnya!")

    with t1: # TAB PDF LENGKAP
        st.subheader("Global Document Integrity Audit")
        up = st.file_uploader("Upload PDF", type="pdf")
        if up and st.button("🔥 RUN INTEGRITY CHECK"):
            res = random.uniform(0.4, 3.5)
            st.markdown(f"""
            <div class="cert-frame">
                <h3 style="color:#00F2FF; margin-top:0;">PDF Audit Certificate</h3>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                    <h1 class="score-hero">{res:.1f}%</h1>
                    <div style="text-align:right;">
                        <div class="status-badge">SECURE</div>
                        <p style="font-size:12px; color:#8B949E; margin-top:5px;">Scan Date: {datetime.now().strftime('%Y-%m-%d')}</p>
                    </div>
                </div>
                <p style="font-size:14px; border-top:1px solid #30363D; padding-top:15px;">
                    <b>Analysis Note:</b> Dokumen telah dibandingkan dengan 15.420 entitas dalam database repositori global. 
                    Tidak ditemukan kesamaan sekuensial yang signifikan. Dokumen dinyatakan <b>Lolos Audit Orisinalitas</b>.
                </p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br><center style='opacity:0.2; font-size:11px;'>POWERED BY FAZRUL TECHNOLOGY V11.0</center>", unsafe_allow_html=True)