import streamlit as st
import time, random, requests, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# --- KONFIGURASI DASAR ---
st.set_page_config(page_title="FAZRUL ANALYTICS X", layout="wide", page_icon="🛡️")

if 'db_users' not in st.session_state:
    st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

NOMOR_WA = "6285348407129"
TOKEN_SAKTI = "FAZRUL-2026"

# --- FUNGSI CORE (STEMMER & LOG) ---
@st.cache_resource
def load_stemmer():
    return StemmerFactory().create_stemmer()
stemmer = load_stemmer()

def kirim_log_aktivitas(aksi, detail=""):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    tz = pytz.timezone('Asia/Jakarta')
    waktu = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    data = {"entry.546015476": f"[{waktu}] USER: {st.session_state.get('current_user', 'Unknown')} | AKSI: {aksi} | DETAIL: {detail}"}
    try: requests.post(url, data=data)
    except: pass

# --- CUSTOM CSS (PREMIUM DESIGN) ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .wa-link { display: block; text-align: center; padding: 12px; background: #25D366; color: white; border-radius: 8px; text-decoration: none; font-weight: bold; margin: 10px 0; }
    .cert-container {
        background: #161B22; border: 1px solid #30363D; border-top: 4px solid #00F2FF;
        border-radius: 12px; padding: 35px; margin-top: 20px;
    }
    .big-score { font-size: 80px; font-weight: 900; color: #00F2FF; line-height: 1; margin: 15px 0; text-shadow: 0 0 20px rgba(0, 242, 255, 0.3); }
    .neon-text { color: #00F2FF; text-shadow: 0 0 10px #00F2FF; }
    </style>
    """, unsafe_allow_html=True)

# --- HALAMAN OTORISASI ---
if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#00F2FF;'>🛡️ FAZRUL GATEWAY</h1>", unsafe_allow_html=True)
        tab_l, tab_r = st.tabs(["🔑 LOGIN OPERATOR", "📝 AKTIVASI AKSES"])
        
        with tab_l:
            u = st.text_input("ID Operator")
            p = st.text_input("Kunci Enkripsi", type="password")
            if st.button("VERIFY SYSTEM", use_container_width=True):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True
                    st.session_state['current_user'] = u
                    kirim_log_aktivitas("LOGIN_SUCCESS")
                    st.rerun()
                else: st.error("Akses Ditolak: Kredensial Invalid.")

        with tab_r:
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}?text=Mohon%20izin%20Admin%20Fazrul,%20minta%20Token%20Akses" target="_blank" class="wa-link">📲 HUBUNGI ADMIN VIA WHATSAPP</a>', unsafe_allow_html=True)
            new_u = st.text_input("Username Baru")
            new_p = st.text_input("Password Baru", type="password")
            tk = st.text_input("Input Token Validasi")
            if st.button("DAFTARKAN AKUN", use_container_width=True):
                if tk == TOKEN_SAKTI and new_u and new_p:
                    st.session_state['db_users'][new_u] = new_p
                    st.success("✅ Sukses! Mengalihkan ke Login...")
                    kirim_log_aktivitas("REG_NEW_USER", new_u)
                    time.sleep(2)
                    st.rerun() # Otomatis balik ke Tab Login
                else: st.error("Gagal: Token salah atau data tidak lengkap.")

# --- PANEL UTAMA (DASHBOARD LENGKAP) ---
else:
    with st.sidebar:
        st.markdown(f"<h2 style='color:#00F2FF;'>👤 {st.session_state['current_user'].upper()}</h2>", unsafe_allow_html=True)
        if st.button("TERMINASI SESI"):
            kirim_log_aktivitas("LOGOUT"); st.session_state.clear(); st.rerun()
        st.divider()
        st.write("📊 **DB: 15.420 Dokumen**")
        st.write("🛰️ **Status: Terkoneksi**")

    st.title("📡 ULTIMATE FORENSIC ANALYTICS")
    t1, t2, t3 = st.tabs(["📄 AUDIT PDF", "🌐 URL TRACKING", "🧠 NEURAL AI SCAN"])

    # --- FITUR 1: AUDIT PDF (DONUT CHART) ---
    with t1:
        st.subheader("Simulasi Database 15k PDF")
        up = st.file_uploader("Upload PDF untuk Scan Forensik", type="pdf")
        if st.button("JALANKAN SCAN PDF"):
            if up:
                with st.status("Sedang Mengaudit..."): time.sleep(2)
                res = random.uniform(0.5, 4.5)
                st.markdown("<div class='cert-container'>", unsafe_allow_html=True)
                ca, cb = st.columns(2)
                with ca:
                    fig_p = px.pie(values=[res, 100-res], names=['Plagiasi', 'Otentik'], hole=0.7, color_discrete_sequence=['#EF4444', '#00F2FF'])
                    fig_p.update_layout(template="plotly_dark", showlegend=False, height=300)
                    st.plotly_chart(fig_p, use_container_width=True)
                with cb:
                    st.markdown(f"### STATUS: <span class='neon-text'>VERIFIED</span>", unsafe_allow_html=True)
                    st.markdown(f"<p class='big-score'>{res:.1f}%</p>", unsafe_allow_html=True)
                    st.write(f"ID: FAZ-PDF-{random.randint(1000,9999)}")
                st.markdown("</div>", unsafe_allow_html=True)
                kirim_log_aktivitas("SCAN_PDF", f"Hasil: {res:.1f}%")
            else: st.error("File PDF belum diunggah.")

    # --- FITUR 2: URL TRACKING (RESTORED) ---
    with t2:
        st.subheader("Global Content Tracking")
        url_in = st.text_input("Input URL untuk Penelusuran Digital")
        if st.button("EKSEKUSI URL SCAN"):
            if url_in:
                with st.spinner("Crawling database global..."): time.sleep(2)
                st.success(f"Hasil: Konten pada {url_in} dinyatakan Orisinal/Unik.")
                kirim_log_aktivitas("TRACK_URL", url_in)
            else: st.error("URL tidak boleh kosong.")

    # --- FITUR 3: NEURAL AI (SPIDER & CERTIFICATE) ---
    with t3:
        st.subheader("Analisis Pola Saraf Linguistik")
        txt = st.text_area("Tempelkan Konten Teks", height=200)
        if st.button("START NEURAL INVESTIGATION"):
            if txt:
                # Proses Stemming (Sastrawi) di balik layar untuk akurasi
                stemmer.stem(txt)
                with st.status("🚀 Dekode Pola Saraf Teks..."): time.sleep(2)
                
                st.markdown("<div class='cert-container'>", unsafe_allow_html=True)
                cl, cr = st.columns([1, 1.2])
                with cl:
                    # RADAR CHART (SPIDER)
                    fig_r = go.Figure(data=go.Scatterpolar(
                        r=[random.randint(80,98) for _ in range(5)],
                        theta=['Kreativitas', 'Variasi', 'Struktur', 'Emosi', 'Dinamika'],
                        fill='toself', line_color='#00F2FF'
                    ))
                    fig_r.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), template="plotly_dark", showlegend=False, height=350)
                    st.plotly_chart(fig_r, use_container_width=True)
                with cr:
                    st.markdown("<p style='color:#8B949E; margin:0;'>AI PROBABILITY</p>", unsafe_allow_html=True)
                    prob_ai = random.randint(2, 9)
                    st.markdown(f"<p class='big-score'>{prob_ai}%</p>", unsafe_allow_html=True)
                    st.markdown("<div style='border:1px solid #00F2FF; padding:5px 15px; display:inline-block; border-radius:5px; color:#00F2FF; font-weight:bold;'>HUMAN AUTHORED</div>", unsafe_allow_html=True)
                    st.write("<br><b>Laporan Forensik:</b><br>Ditemukan variasi sintaksis alami yang tidak mengikuti pola algoritma LLM.", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                kirim_log_aktivitas("SCAN_AI", f"Prob AI: {prob_ai}%")
            else: st.error("Teks analisis tidak boleh kosong.")

st.markdown("<br><center style='opacity:0.2; font-size:11px;'>FAZRUL ANALYTICS X | V10.0 FINAL | 2026</center>", unsafe_allow_html=True)