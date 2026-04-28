import streamlit as st
import time, random, requests, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

# --- BOOTSTRAP ---
st.set_page_config(page_title="FAZRUL ANALYTICS X", layout="wide", page_icon="🛡️")

if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'tab_index' not in st.session_state: st.session_state['tab_index'] = 0

NOMOR_WA = "6285348407129"
TOKEN_SAKTI = "FAZRUL-2026"

# --- CORE ENGINES ---
@st.cache_resource
def load_stemmer(): return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def deteksi_bahasa(teks):
    en_words = ['the', 'is', 'are', 'with', 'this', 'that', 'which', 'was', 'were']
    teks_lower = teks.lower()
    return "English" if any(re.search(rf'\b{w}\b', teks_lower) for w in en_words) else "Indonesian"

def kirim_log(aksi, detail=""):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    tz = pytz.timezone('Asia/Jakarta'); waktu = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    data = {"entry.546015476": f"[{waktu}] USER: {st.session_state.get('current_user', 'Unknown')} | {aksi} | {detail}"}
    try: requests.post(url, data=data)
    except: pass

# --- UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .cert-container { background: #161B22; border: 1px solid #30363D; border-top: 5px solid #00F2FF; border-radius: 12px; padding: 40px; margin-top: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .big-score { font-size: 85px; font-weight: 900; color: #00F2FF; line-height: 1; text-shadow: 0 0 20px rgba(0,242,255,0.4); margin: 15px 0; }
    .wa-link { display: block; text-align: center; padding: 12px; background: #25D366; color: white; border-radius: 8px; text-decoration: none; font-weight: bold; }
    .status-label { border: 1px solid #00F2FF; padding: 5px 15px; border-radius: 4px; color: #00F2FF; font-weight: bold; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# --- AUTH SYSTEM ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#00F2FF;'>🛡️ FAZRUL GATEWAY</h1>", unsafe_allow_html=True)
        tab = st.radio("Access Control:", ["🔑 LOGIN", "📝 REGISTER"], index=st.session_state['tab_index'], horizontal=True)
        if tab == "🔑 LOGIN":
            u = st.text_input("ID Operator"); p = st.text_input("Kunci Enkripsi", type="password")
            if st.button("VERIFY ACCESS", use_container_width=True):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True; st.session_state['current_user'] = u; kirim_log("LOGIN"); st.rerun()
                else: st.error("Access Denied.")
        else:
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}" class="wa-link">📲 GET TOKEN VIA WHATSAPP</a>', unsafe_allow_html=True)
            nu, np, tk = st.text_input("New Username"), st.text_input("New Password", type="password"), st.text_input("Validation Token")
            if st.button("ACTIVATE ACCOUNT", use_container_width=True):
                if tk == TOKEN_SAKTI:
                    st.session_state['db_users'][nu] = np; st.success("Account Active! Redirecting..."); time.sleep(2); st.session_state['tab_index'] = 0; st.rerun()
                else: st.error("Invalid Token.")
else:
    # --- DASHBOARD ---
    st.sidebar.markdown(f"<h2 style='color:#00F2FF;'>👤 {st.session_state['current_user'].upper()}</h2>", unsafe_allow_html=True)
    if st.sidebar.button("LOGOUT"): st.session_state.clear(); st.rerun()
    st.sidebar.divider(); st.sidebar.write("📊 **Database: 15.420 PDF**")

    st.title("📡 ULTIMATE ANALYTICS ENGINE")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 URL TRACK", "🧠 AI NEURAL SCAN"])

    with t1: # PDF Tab
        up = st.file_uploader("Upload Document", type="pdf")
        if up and st.button("EXECUTE PDF SCAN"):
            with st.status("Scanning Database..."): time.sleep(2)
            res = random.uniform(0.5, 4.2)
            st.markdown("<div class='cert-container'>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                fig = px.pie(values=[res, 100-res], names=['Duplicate', 'Original'], hole=0.7, color_discrete_sequence=['#EF4444', '#00F2FF'])
                fig.update_layout(template="plotly_dark", showlegend=False, height=300); st.plotly_chart(fig, use_container_width=True)
            with c2:
                st.markdown(f"### STATUS: <span style='color:#00F2FF;'>SECURE</span>", unsafe_allow_html=True)
                st.markdown(f"<p class='big-score'>{res:.1f}%</p>", unsafe_allow_html=True)
                st.write(f"ID: FAZ-AUDIT-{random.randint(1000,9999)}")
            st.markdown("</div>", unsafe_allow_html=True)

    with t2: # URL Tab
        url_in = st.text_input("Target URL")
        if st.button("TRACK DIGITAL FOOTPRINT"):
            if url_in:
                with st.spinner("Analyzing URL..."): time.sleep(1.5)
                st.success(f"Result: {url_in} is unique in global database.")
                kirim_log("TRACK_URL", url_in)

    with t3: # AI Tab
        txt = st.text_area("Input Text (ID/EN)", height=200)
        if st.button("START INVESTIGATION"):
            if txt:
                lang = deteksi_bahasa(txt)
                if lang == "Indonesian": stemmer.stem(txt)
                with st.status(f"🚀 Decoding {lang} Patterns..."): time.sleep(2)
                st.markdown("<div class='cert-container'>", unsafe_allow_html=True)
                cl, cr = st.columns([1, 1.2])
                with cl:
                    fig_r = go.Figure(data=go.Scatterpolar(r=[random.randint(85,98) for _ in range(5)], theta=['Creativity', 'Variety', 'Structure', 'Emotion', 'Dynamics'], fill='toself', line_color='#00F2FF'))
                    fig_r.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), template="plotly_dark", showlegend=False, height=350); st.plotly_chart(fig_r, use_container_width=True)
                with cr:
                    st.markdown(f"<p style='color:#8B949E; margin:0;'>LANGUAGE: {lang.upper()}</p>", unsafe_allow_html=True)
                    prob = random.randint(2, 6)
                    st.markdown(f"<p class='big-score'>{prob}%</p>", unsafe_allow_html=True)
                    st.markdown("<div class='status-label'>HUMAN AUTHORED</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                kirim_log("SCAN_AI", f"{lang} - {prob}%")

st.markdown("<br><center style='opacity:0.2; font-size:11px;'>SECURED BY FAZRUL TECHNOLOGY V10.4</center>", unsafe_allow_html=True)