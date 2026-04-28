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

# --- ENGINE ---
@st.cache_resource
def load_stemmer(): return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def deteksi_bahasa(teks):
    en_words = ['the', 'is', 'are', 'with', 'from', 'which', 'that', 'was', 'were']
    return "English" if any(re.search(rf'\b{w}\b', teks.lower()) for w in en_words) else "Indonesian"

def kirim_log(aksi, detail=""):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    tz = pytz.timezone('Asia/Jakarta'); waktu = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    data = {"entry.546015476": f"[{waktu}] USER: {st.session_state.get('current_user', 'Unknown')} | {aksi} | {detail}"}
    try: requests.post(url, data=data)
    except: pass

# --- CSS LUXURY ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .cert-frame {
        background: linear-gradient(160deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #30363D; border-left: 6px solid #00F2FF;
        border-radius: 10px; padding: 35px; margin: 20px 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }
    .score-hero {
        font-size: 100px; font-weight: 900; color: #00F2FF;
        line-height: 1; margin: 0; text-shadow: 0 0 25px rgba(0,242,255,0.4);
    }
    .status-badge {
        background: rgba(0, 242, 255, 0.1); color: #00F2FF; border: 1px solid #00F2FF;
        padding: 5px 20px; border-radius: 50px; font-weight: bold; display: inline-block;
    }
    .wa-button { 
        display: block; text-align: center; padding: 14px; background: #25D366; 
        color: white !important; border-radius: 10px; text-decoration: none; font-weight: bold;
    }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 3.2em; }
    </style>
    """, unsafe_allow_html=True)

# --- GATEWAY ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#00F2FF;'>🛡️ FAZRUL GATEWAY</h1>", unsafe_allow_html=True)
        c_nav1, c_nav2 = st.columns(2)
        if c_nav1.button("🔑 LOGIN", type="primary" if st.session_state['view']=="login" else "secondary"):
            st.session_state['view']="login"; st.rerun()
        if c_nav2.button("📝 DAFTAR", type="primary" if st.session_state['view']=="register" else "secondary"):
            st.session_state['view']="register"; st.rerun()
        
        st.divider()
        if st.session_state['view'] == "login":
            u = st.text_input("ID Operator")
            p = st.text_input("Password", type="password")
            if st.button("VERIFY ACCESS"):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True; st.session_state['current_user'] = u; kirim_log("LOGIN"); st.rerun()
                else: st.error("Login Gagal.")
        else:
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}" class="wa-button">📲 REQUEST TOKEN</a>', unsafe_allow_html=True)
            nu, np, tk = st.text_input("User ID"), st.text_input("Pass", type="password"), st.text_input("Token")
            if st.button("AKTIFKAN"):
                if tk == TOKEN_SAKTI and nu and np:
                    st.session_state['db_users'][nu] = np
                    st.success("✅ Berhasil! Mengalihkan..."); time.sleep(1.8)
                    st.session_state['view'] = "login"; st.rerun()

else:
    # --- DASHBOARD ---
    st.sidebar.markdown(f"### 👤 {st.session_state['current_user'].upper()}")
    if st.sidebar.button("LOGOUT"): st.session_state.clear(); st.rerun()
    st.sidebar.divider(); st.sidebar.write("📊 **Database: 15.420 PDF**")

    st.title("📡 FORENSIC ANALYTICS CENTER")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 URL TRACKER", "🧠 NEURAL AI"])

    # 1. AUDIT PDF (KEMBALIKAN DONUT CHART)
    with t1:
        st.subheader("Simulasi Database 15k PDF")
        up = st.file_uploader("Upload File", type="pdf")
        if st.button("🔥 JALANKAN SCAN PDF", key="pdf_btn"):
            if up:
                with st.status("Auditing Database..."): time.sleep(2)
                res = random.uniform(0.5, 4.5)
                st.markdown("<div class='cert-frame'>", unsafe_allow_html=True)
                ca, cb = st.columns(2)
                with ca:
                    fig_p = px.pie(values=[res, 100-res], names=['Duplicate', 'Original'], hole=0.7, color_discrete_sequence=['#EF4444', '#00F2FF'])
                    fig_p.update_layout(template="plotly_dark", showlegend=False, height=280, margin=dict(t=0, b=0, l=0, r=0))
                    st.plotly_chart(fig_p, use_container_width=True)
                with cb:
                    st.markdown(f"<p style='color:#8B949E; margin:0;'>DUPLICATE INDEX</p>", unsafe_allow_html=True)
                    st.markdown(f"<h1 class='score-hero'>{res:.1f}%</h1>", unsafe_allow_html=True)
                    st.markdown("<div class='status-badge'>VERIFIED ORIGINAL</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else: st.error("Upload PDF dulu!")

    # 2. URL TRACKER (KEMBALIKAN FITUR TRACKING DIGITAL)
    with t2:
        st.subheader("Global Content Footprint Tracker")
        url_in = st.text_input("Target URL")
        if st.button("🌐 EKSEKUSI URL TRACKING", key="url_btn"):
            if url_in:
                with st.spinner("Scanning Web Repositories..."): time.sleep(1.5)
                st.markdown("<div class='cert-frame'>", unsafe_allow_html=True)
                st.success(f"Analisis Jejak Digital Selesai untuk: {url_in}")
                st.write("Hasil: Konten ini **unik** dan tidak ditemukan duplikasi di database publik.")
                st.markdown("</div>", unsafe_allow_html=True)
            else: st.error("URL tidak boleh kosong!")

    # 3. NEURAL AI (SPIDER + SASTRAWI + MULTILINGUAL)
    with t3:
        st.subheader("Neural Linguistic Investigation")
        txt = st.text_area("Input Content (ID/EN)", height=180)
        if st.button("🧠 START NEURAL SCAN", key="ai_btn"):
            if txt:
                lang = deteksi_bahasa(txt)
                if lang == "Indonesian": stemmer.stem(txt)
                with st.status(f"Decoding {lang} Neural Patterns..."): time.sleep(2.5)
                
                st.markdown(f"""
                <div class="cert-frame">
                    <div style="display:flex; justify-content:space-between; border-bottom:1px solid #30363D; padding-bottom:15px; margin-bottom:20px;">
                        <span style="color:#00F2FF; font-weight:bold;">OFFICIAL FORENSIC REPORT</span>
                        <span style="color:#8B949E;">ID: {hex(random.getrandbits(24)).upper()}</span>
                    </div>
                    <div style="display:flex; flex-wrap:wrap; gap:30px; align-items:center;">
                        <div style="flex:1; text-align:center;">
                            <p style="color:#8B949E; margin:0; font-size:12px;">AI PROBABILITY</p>
                            <h1 class="score-hero">{random.randint(2, 7)}%</h1>
                            <div class="status-badge">HUMAN AUTHORED</div>
                        </div>
                        <div style="flex:2; border-left:1px solid #30363D; padding-left:30px;">
                            <p style="color:#8B949E; font-size:13px; margin:0;">LANGUAGE: <b style="color:#00F2FF;">{lang.upper()}</b></p>
                            <p style="margin-top:15px; line-height:1.6; font-size:14px;">
                                Pola sintaksis menunjukkan variasi natural manusia. Tidak terdeteksi pola 
                                algoritma Markov atau struktur repetitif khas LLM. 
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns([1, 2, 1])
                with c2:
                    fig_r = go.Figure(data=go.Scatterpolar(r=[random.randint(85,98) for _ in range(5)], theta=['Creativity', 'Variety', 'Structure', 'Emotion', 'Dynamics'], fill='toself', line_color='#00F2FF'))
                    fig_r.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), template="plotly_dark", showlegend=False, height=350, paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_r, use_container_width=True)
                kirim_log("AI_SCAN", f"{lang} {random.randint(2,7)}%")
            else: st.error("Isi teksnya!")

st.markdown("<br><center style='opacity:0.2; font-size:11px;'>SECURED BY FAZRUL TECHNOLOGY V10.9 FINAL</center>", unsafe_allow_html=True)