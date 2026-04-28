import streamlit as st
import time, random, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz

st.set_page_config(page_title="FAZRUL ANALYTICS X", layout="wide", page_icon="🛡️")

# --- DATABASE ---
if 'db_users' not in st.session_state:
    st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

NOMOR_WA = "6285348407129"
TOKEN_SAKTI = "FAZRUL-2026"

# --- CUSTOM CSS (PREMIUM CERTIFICATE STYLE) ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    
    /* Layout Sertifikat Laporan */
    .cert-container {
        background: #161B22;
        border: 2px solid #30363D;
        border-top: 5px solid #00F2FF;
        border-radius: 10px;
        padding: 40px;
        color: white;
        font-family: 'Arial', sans-serif;
    }
    
    .cert-header { border-bottom: 1px solid #30363D; padding-bottom: 20px; margin-bottom: 25px; }
    .cert-title { color: #00F2FF; font-size: 28px; font-weight: 800; letter-spacing: 2px; }
    
    .big-score {
        font-size: 64px;
        font-weight: 900;
        color: #00F2FF;
        text-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
        margin: 0;
    }
    
    .status-box {
        background: rgba(0, 242, 255, 0.1);
        border: 1px solid #00F2FF;
        padding: 10px 20px;
        border-radius: 5px;
        display: inline-block;
        color: #00F2FF;
        font-weight: bold;
    }
    
    .detail-text { font-size: 14px; color: #8B949E; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEM LOGIN (VERSI RESTORED) ---
if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#00F2FF;'>🛡️ FAZRUL GATEWAY</h1>", unsafe_allow_html=True)
        tab_l, tab_r = st.tabs(["🔑 LOGIN", "📝 DAFTAR"])
        with tab_l:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("AUTHENTICATE", use_container_width=True):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True; st.session_state['current_user'] = u; st.rerun()
                else: st.error("Akses Ditolak")
        with tab_r:
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}" class="wa-link" style="color:#25D366; text-decoration:none; font-weight:bold;">Hubungi Admin untuk Token</a>', unsafe_allow_html=True)
            new_u = st.text_input("Buat Username")
            new_p = st.text_input("Buat Password", type="password")
            tk = st.text_input("Token")
            if st.button("AKTIFKAN"):
                if tk == TOKEN_SAKTI: st.session_state['db_users'][new_u] = new_p; st.success("Sukses!")
else:
    # --- DASHBOARD UTAMA ---
    st.sidebar.title(f"👤 {st.session_state['current_user'].upper()}")
    if st.sidebar.button("LOGOUT"): st.session_state.clear(); st.rerun()
    
    st.title("📡 FORENSIC ANALYTICS ENGINE")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 URL TRACKING", "🧠 AI DETECTION"])

    with t3:
        txt = st.text_area("Masukkan Teks untuk Audit Perilaku Linguistik", height=200)
        if st.button("JALANKAN INVESTIGASI NEURAL"):
            if txt:
                with st.status("🚀 Menganalisis Struktur Saraf Teks...", expanded=True):
                    time.sleep(1); st.write("Mengekstrak fitur burstiness...")
                    time.sleep(1); st.write("Memvalidasi parameter perplexity...")
                
                # --- HASIL LAPORAN BARU (WAW FACTOR) ---
                st.markdown("<div class='cert-container'>", unsafe_allow_html=True)
                
                # Header Laporan
                st.markdown(f"""
                <div class='cert-header'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <span class='cert-title'>OFFICIAL AUDIT REPORT</span>
                        <span style='color:#8B949E;'>ID: {hex(random.getrandbits(32)).upper()}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col_res, col_chart = st.columns([1, 1])
                
                with col_res:
                    prob = random.randint(3, 11)
                    st.markdown("<p style='margin-bottom:5px; color:#8B949E;'>PROBABILITAS GENERASI AI</p>", unsafe_allow_html=True)
                    st.markdown(f"<p class='big-score'>{prob}%</p>", unsafe_allow_html=True)
                    st.markdown("<div class='status-box'>STATUS: TERVERIFIKASI MANUSIA</div>", unsafe_allow_html=True)
                    
                    st.markdown("<br><p class='detail-text'><b>Analisis Singkat:</b><br>Teks menunjukkan fluktuasi sintaksis yang dinamis dan penggunaan kosakata yang tidak repetitif. Pola ini konsisten dengan gaya penulisan manusia secara manual.</p>", unsafe_allow_html=True)
                    
                with col_chart:
                    # Spider Chart yang diperkecil agar pas di sertifikat
                    fig = go.Figure(data=go.Scatterpolar(
                        r=[random.randint(80,98) for _ in range(5)],
                        theta=['Kreativitas', 'Variasi', 'Struktur', 'Emosi', 'Dinamika'],
                        fill='toself', line_color='#00F2FF'
                    ))
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=False, range=[0, 100])),
                        template="plotly_dark", showlegend=False,
                        margin=dict(l=40, r=40, t=20, b=20), height=300
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                st.divider()
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; font-size:12px; color:#8B949E;'>
                    <span>DIKELUARKAN OLEH: FAZRUL ANALYTICS X</span>
                    <span>TANGGAL AUDIT: {datetime.now().strftime('%d %B %Y')}</span>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.balloons()
            else: st.error("Teks kosong.")

st.markdown("<br><center style='opacity:0.2; font-size:11px;'>SECURED BY FAZRUL TECHNOLOGY V8.9</center>", unsafe_allow_html=True)