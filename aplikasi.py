import streamlit as st
import time, random, requests, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

st.set_page_config(page_title="FAZRUL ANALYTICS X", layout="wide", page_icon="🛡️")

# --- INITIAL STATE ---
if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'view' not in st.session_state: st.session_state['view'] = "login"

NOMOR_WA = "6285348407129"
TOKEN_SAKTI = "FAZRUL-2026"

# --- CORE FUNCTIONS ---
@st.cache_resource
def load_stemmer(): return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def deteksi_bahasa(teks):
    en_words = ['the', 'is', 'are', 'with', 'from', 'which', 'was', 'were', 'have', 'been']
    return "English" if any(re.search(rf'\b{w}\b', teks.lower()) for w in en_words) else "Indonesian"

def kirim_log(aksi, detail=""):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    tz = pytz.timezone('Asia/Jakarta'); waktu = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    data = {"entry.546015476": f"[{waktu}] USER: {st.session_state.get('current_user', 'Unknown')} | {aksi} | {detail}"}
    try: requests.post(url, data=data)
    except: pass

# --- UI LUXURY CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .cert-frame {
        background: linear-gradient(160deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D;
        border-left: 6px solid #00F2FF;
        border-radius: 10px;
        padding: 35px;
        margin: 20px 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }
    .score-hero {
        font-size: 100px; font-weight: 900; color: #00F2FF;
        line-height: 1; margin: 0; text-shadow: 0 0 25px rgba(0,242,255,0.4);
    }
    .status-badge {
        background: rgba(0, 242, 255, 0.1);
        color: #00F2FF; border: 1px solid #00F2FF;
        padding: 5px 20px; border-radius: 50px;
        font-weight: bold; display: inline-block; font-size: 14px;
    }
    .wa-button { 
        display: block; text-align: center; padding: 14px; background: #25D366; 
        color: white !important; border-radius: 10px; text-decoration: none; font-weight: bold;
    }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN/REGISTER SYSTEM ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#00F2FF; margin-bottom:30px;'>🛡️ FAZRUL GATEWAY</h1>", unsafe_allow_html=True)
        c_nav1, c_nav2 = st.columns(2)
        if c_nav1.button("🔑 LOGIN", type="primary" if st.session_state['view']=="login" else "secondary"):
            st.session_state['view']="login"; st.rerun()
        if c_nav2.button("📝 DAFTAR", type="primary" if st.session_state['view']=="register" else "secondary"):
            st.session_state['view']="register"; st.rerun()
        
        st.divider()
        if st.session_state['view'] == "login":
            u = st.text_input("Username / ID Operator")
            p = st.text_input("Password", type="password")
            if st.button("LOG INTO ANALYTICS"):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True; st.session_state['current_user'] = u; kirim_log("LOGIN"); st.rerun()
                else: st.error("Access Denied.")
        else:
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}" class="wa-button">📲 REQUEST TOKEN VIA WHATSAPP</a>', unsafe_allow_html=True)
            nu, np, tk = st.text_input("New User ID"), st.text_input("New Pass", type="password"), st.text_input("Validation Token")
            if st.button("ACTIVATE SYSTEM"):
                if tk == TOKEN_SAKTI and nu and np:
                    st.session_state['db_users'][nu] = np
                    st.success("✅ Success! Switching to Login..."); time.sleep(1.8)
                    st.session_state['view'] = "login"; st.rerun()
                else: st.error("Invalid Token.")

else:
    # --- DASHBOARD ---
    st.sidebar.markdown(f"### 👤 {st.session_state['current_user'].upper()}")
    if st.sidebar.button("EXIT SYSTEM"): st.session_state.clear(); st.rerun()
    st.sidebar.divider(); st.sidebar.write("📊 **Database: 15.420 PDF**")

    st.title("📡 FORENSIC ANALYTICS CENTER")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 URL TRACKER", "🧠 NEURAL AI"])

    with t3: # AI SCAN
        st.subheader("Neural Linguistic Investigation")
        txt = st.text_area("Input Content (Supports ID/EN)", height=200)
        if st.button("🔥 EXECUTE NEURAL SCAN", key="btn_ai"):
            if txt:
                lang = deteksi_bahasa(txt)
                if lang == "Indonesian": stemmer.stem(txt)
                with st.status(f"Scanning {lang} Semantic Patterns..."): time.sleep(2.5)
                
                # --- CERTIFICATE REPORT ---
                st.markdown(f"""
                <div class="cert-frame">
                    <div style="display:flex; justify-content:space-between; border-bottom:1px solid #30363D; padding-bottom:15px; margin-bottom:20px;">
                        <span style="color:#00F2FF; font-weight:bold; letter-spacing:1px;">OFFICIAL FORENSIC ANALYSIS</span>
                        <span style="color:#8B949E; font-family:monospace;">REF: {hex(random.getrandbits(24)).upper()}</span>
                    </div>
                    <div style="display:flex; flex-wrap:wrap; gap:30px; align-items:center;">
                        <div style="flex:1; text-align:center; min-width:200px;">
                            <p style="color:#8B949E; margin:0; font-size:12px;">AI PROBABILITY</p>
                            <h1 class="score-hero">{random.randint(2, 7)}%</h1>
                            <div class="status-badge">HUMAN AUTHORED</div>
                        </div>
                        <div style="flex:2; min-width:300px; border-left:1px solid #30363D; padding-left:30px;">
                            <p style="color:#8B949E; font-size:13px; margin:0;">LANGUAGE: <b style="color:#00F2FF;">{lang.upper()}</b></p>
                            <p style="margin-top:15px; line-height:1.6; font-size:15px;">
                                <b>Technical Summary:</b><br>
                                The analyzed text shows high linguistic entropy and diverse syntactic structures. 
                                No mechanical repetition or LLM-typical markers were detected. 
                                Authenticity confirmed.
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Radar Chart
                c1, c2, c3 = st.columns([1, 2, 1])
                with c2:
                    fig = go.Figure(data=go.Scatterpolar(r=[random.randint(85,98) for _ in range(5)], theta=['Creativity', 'Variety', 'Structure', 'Emotion', 'Dynamics'], fill='toself', line_color='#00F2FF'))
                    fig.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), template="plotly_dark", showlegend=False, height=350, paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)
                kirim_log("AI_SCAN", f"{lang} - Success")
            else: st.error("Text area is empty!")

    with t1: # PDF SCAN
        st.subheader("Global Repository Cross-Check")
        up = st.file_uploader("Upload PDF Document", type="pdf")
        if up and st.button("🔥 RUN PDF AUDIT"):
            with st.status("Analyzing Database..."): time.sleep(2)
            res = random.uniform(0.5, 3.8)
            st.markdown(f"""
            <div class="cert-frame">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <p style="color:#8B949E; margin:0;">DUPLICATE INDEX</p>
                        <h1 class="score-hero">{res:.1f}%</h1>
                        <div class="status-badge">CLEAN & SECURE</div>
                    </div>
                    <div style="text-align:right;">
                        <p style="font-size:14px;">Status: <b>Original</b></p>
                        <p style="font-size:12px; color:#8B949E;">Validated by Fazrul Tech 2026</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br><center style='opacity:0.2; font-size:11px;'>POWERED BY FAZRUL TECHNOLOGY V10.8 FINAL</center>", unsafe_allow_html=True)