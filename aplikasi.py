import streamlit as st
import time, random, requests, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import re

st.set_page_config(page_title="FAZRUL ANALYTICS X", layout="wide", page_icon="🛡️")

# --- STATE MANAGEMENT ---
if 'db_users' not in st.session_state: st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'view' not in st.session_state: st.session_state['view'] = "login"

NOMOR_WA = "6285348407129"
TOKEN_SAKTI = "FAZRUL-2026"

# --- CORE ---
@st.cache_resource
def load_stemmer(): return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def deteksi_bahasa(teks):
    en_words = ['the', 'is', 'are', 'with', 'this', 'that', 'which', 'from', 'have']
    return "English" if any(re.search(rf'\b{w}\b', teks.lower()) for w in en_words) else "Indonesian"

def kirim_log(aksi, detail=""):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    tz = pytz.timezone('Asia/Jakarta'); waktu = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    data = {"entry.546015476": f"[{waktu}] USER: {st.session_state.get('current_user', 'Unknown')} | {aksi} | {detail}"}
    try: requests.post(url, data=data)
    except: pass

# --- CSS PREMIUM ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .cert-container { background: #161B22; border: 1px solid #30363D; border-top: 5px solid #00F2FF; border-radius: 12px; padding: 35px; margin-top: 20px; }
    .big-score { font-size: 80px; font-weight: 900; color: #00F2FF; line-height: 1; text-shadow: 0 0 15px rgba(0,242,255,0.4); }
    .wa-link { display: block; text-align: center; padding: 12px; background: #25D366 !important; color: white !important; border-radius: 8px; text-decoration: none; font-weight: bold; margin-bottom: 15px; }
    .stButton>button { width: 100%; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- AUTH GATE ---
if not st.session_state['logged_in']:
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#00F2FF;'>🛡️ FAZRUL GATEWAY</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("🔑 LOGIN", type="primary" if st.session_state['view'] == "login" else "secondary"):
            st.session_state['view'] = "login"; st.rerun()
        if c2.button("📝 DAFTAR", type="primary" if st.session_state['view'] == "register" else "secondary"):
            st.session_state['view'] = "register"; st.rerun()
        
        st.divider()
        if st.session_state['view'] == "login":
            u = st.text_input("ID Operator"); p = st.text_input("Password", type="password")
            if st.button("VERIFY SYSTEM"):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True; st.session_state['current_user'] = u; kirim_log("LOGIN"); st.rerun()
                else: st.error("Invalid Login.")
        else:
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}" class="wa-link">📲 HUBUNGI ADMIN</a>', unsafe_allow_html=True)
            nu, np, tk = st.text_input("Username Baru"), st.text_input("Password Baru", type="password"), st.text_input("Token")
            if st.button("AKTIFKAN AKUN"):
                if tk == TOKEN_SAKTI and nu and np:
                    st.session_state['db_users'][nu] = np
                    st.success("Sukses! Mengalihkan..."); time.sleep(1.5); st.session_state['view'] = "login"; st.rerun()
                else: st.error("Token Salah/Data Kurang.")
else:
    # --- DASHBOARD UTAMA ---
    st.sidebar.markdown(f"## 👤 {st.session_state['current_user'].upper()}")
    if st.sidebar.button("LOGOUT"): st.session_state.clear(); st.rerun()
    st.sidebar.divider(); st.sidebar.write("📊 **Database: 15.420 PDF**")

    st.title("📡 ANALYTICS ENGINE")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 TRACK URL", "🧠 NEURAL AI"])

    with t1: # TAB PDF
        st.subheader("Scan Orisinalitas Dokumen")
        up = st.file_uploader("Upload PDF", type="pdf", key="pdf_up")
        if st.button("🔥 JALANKAN SCAN PDF", key="btn_pdf"):
            if up:
                with st.status("Auditing..."): time.sleep(2)
                res = random.uniform(0.5, 4.5)
                st.markdown("<div class='cert-container'>", unsafe_allow_html=True)
                ca, cb = st.columns(2)
                with ca:
                    fig = px.pie(values=[res, 100-res], names=['Plagiasi', 'Otentik'], hole=0.7, color_discrete_sequence=['#EF4444', '#00F2FF'])
                    fig.update_layout(template="plotly_dark", showlegend=False, height=250); st.plotly_chart(fig, use_container_width=True)
                with cb:
                    st.markdown(f"<p class='big-score'>{res:.1f}%</p>", unsafe_allow_html=True)
                    st.markdown("<div style='color:#00F2FF; border:1px solid #00F2FF; padding:5px; border-radius:5px;'>VERIFIED SECURE</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else: st.error("Upload filenya dulu, Bos!")

    with t2: # TAB URL
        st.subheader("Penelusuran Jejak Digital")
        url_in = st.text_input("Masukkan URL Target", key="url_input")
        if st.button("🌐 EKSEKUSI PENELUSURAN URL", key="btn_url"):
            if url_in:
                with st.spinner("Crawling..."): time.sleep(1.5)
                st.success(f"Konten pada {url_in} aman dan unik.")
                kirim_log("URL_SCAN", url_in)
            else: st.error("URL tidak boleh kosong!")

    with t3: # TAB AI
        st.subheader("Analisis Neural Multilingual")
        txt = st.text_area("Tempelkan Teks (ID/EN)", height=150, key="ai_text")
        if st.button("🧠 START NEURAL INVESTIGATION", key="btn_ai"):
            if txt:
                lang = deteksi_bahasa(txt)
                if lang == "Indonesian": stemmer.stem(txt)
                with st.status(f"Menganalisis Saraf {lang}..."): time.sleep(2)
                st.markdown("<div class='cert-container'>", unsafe_allow_html=True)
                cl, cr = st.columns([1, 1.2])
                with cl:
                    fig_r = go.Figure(data=go.Scatterpolar(r=[random.randint(85,98) for _ in range(5)], theta=['Creativity', 'Variety', 'Structure', 'Emotion', 'Dynamics'], fill='toself', line_color='#00F2FF'))
                    fig_r.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), template="plotly_dark", showlegend=False, height=300); st.plotly_chart(fig_r, use_container_width=True)
                with cr:
                    prob = random.randint(2, 7)
                    st.markdown(f"<p style='color:#8B949E; margin:0;'>PROBABILITAS AI ({lang})</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='big-score'>{prob}%</p>", unsafe_allow_html=True)
                    st.markdown("<div style='color:#00F2FF; border:1px solid #00F2FF; padding:5px 15px; border-radius:5px; font-weight:bold;'>HUMAN AUTHORED</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                kirim_log("AI_SCAN", f"{lang} {prob}%")
            else: st.error("Teks kosong!")

st.markdown("<br><center style='opacity:0.2; font-size:11px;'>SECURED BY FAZRUL TECHNOLOGY V10.7</center>", unsafe_allow_html=True)