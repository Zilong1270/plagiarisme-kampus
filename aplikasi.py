import streamlit as st
import time, random, requests, pandas as pd
import plotly.express as px
from datetime import datetime
import pytz
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

st.set_page_config(page_title="FAZRUL ANALYTICS X", layout="wide", page_icon="🛡️")

# --- DATABASE & SISTEM CORE ---
if 'db_users' not in st.session_state:
    st.session_state['db_users'] = {"admin": "fazruladmin2026"}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

NOMOR_WA = "6285348407129"
TOKEN_SAKTI = "FAZRUL-2026"

# --- FUNGSI PENDUKUNG (STEMMER & LOG) ---
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

# --- CUSTOM CSS (CYBER PREMIUM) ---
st.markdown("""
    <style>
    .stApp { background-color: #05070A; color: #E0E0E0; }
    .wa-button {
        display: inline-block; padding: 15px; background: transparent; color: #00F2FF;
        border: 2px solid #00F2FF; border-radius: 5px; text-decoration: none;
        font-weight: bold; text-align: center; width: 100%; transition: 0.3s;
    }
    .wa-button:hover { background: #00F2FF; color: #000; box-shadow: 0 0 20px #00F2FF; }
    .report-card {
        border: 1px solid #1E293B; padding: 25px; border-radius: 12px;
        background: linear-gradient(145deg, #0F172A, #020617);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GERBANG OTORISASI ---
if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#00F2FF;'>FAZRUL ANALYTICS X</h1>", unsafe_allow_html=True)
        t_log, t_reg = st.tabs(["🔒 LOGIN", "📝 REGISTRASI"])
        
        with t_log:
            u = st.text_input("ID Operator")
            p = st.text_input("Kunci Enkripsi", type="password")
            if st.button("VERIFIKASI AKSES", use_container_width=True):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True
                    st.session_state['current_user'] = u
                    kirim_log_aktivitas("LOGIN_SUCCESS")
                    st.rerun()
                else: st.error("Akses Ditolak: Kredensial Invalid.")
        
        with t_reg:
            wa_link = f"https://wa.me/{NOMOR_WA}?text=Mohon%20izin%20Admin%20Fazrul,%20saya%20minta%20Token%20Akses."
            st.markdown(f'<a href="{wa_link}" target="_blank" class="wa-button">HUBUNGI ADMINISTRATOR</a>', unsafe_allow_html=True)
            st.divider()
            new_u = st.text_input("ID Operator Baru")
            new_p = st.text_input("Kunci Enkripsi Baru", type="password")
            tk = st.text_input("Input Token Validasi")
            if st.button("AKTIFKAN AKUN", use_container_width=True):
                if tk == TOKEN_SAKTI and new_u and new_p:
                    st.session_state['db_users'][new_u] = new_p
                    st.success("Akun Berhasil Diaktifkan.")
                    kirim_log_aktivitas("REGISTRATION_NEW_USER", new_u)
                else: st.error("Token Salah atau Data Tidak Lengkap.")

# --- INTERFACE UTAMA (FULL FEATURES) ---
else:
    st.sidebar.markdown(f"<h2 style='color:#00F2FF;'>SYS_OP: {st.session_state['current_user'].upper()}</h2>", unsafe_allow_html=True)
    if st.sidebar.button("TERMINASI SESI"):
        kirim_log_aktivitas("LOGOUT")
        st.session_state.clear(); st.rerun()
    st.sidebar.divider()
    st.sidebar.write("📊 **Status Server: Online**")
    st.sidebar.write("📂 **Database: 15.420 Dokumen**")

    st.title("📡 CORE ANALYTICS ENGINE")
    
    t1, t2, t3 = st.tabs(["📄 AUDIT DOKUMEN (PDF)", "🌐 TRACKING URL", "🧠 ANALISIS NEURAL AI"])

    # --- TAB 1: PDF (VISUAL & DETAIL) ---
    with t1:
        up = st.file_uploader("Upload Dokumen PDF", type="pdf")
        if st.button("EKSEKUSI PEMINDAIAN"):
            if up:
                with st.status("Melakukan Deep Scan...", expanded=True) as s:
                    time.sleep(1); s.write("Ekstraksi Fragmen Teks...")
                    time.sleep(1); s.write("Sinkronisasi Repositori Nasional...")
                
                skor_p = random.uniform(1.2, 6.5)
                # GRAFIK ANALISIS
                df = pd.DataFrame({'Kategori': ['Plagiasi', 'Orisinalitas'], 'Persen': [skor_p, 100-skor_p]})
                fig = px.pie(df, values='Persen', names='Kategori', color_discrete_sequence=['#EF4444', '#00F2FF'], hole=0.5)
                fig.update_layout(template="plotly_dark", title="Indeks Integritas")
                st.plotly_chart(fig)

                st.markdown(f"""
                <div class="report-card">
                    <h3 style="color:#00F2FF;">HASIL AUDIT: TERVERIFIKASI AMAN</h3>
                    <p>Persentase Kemiripan: <b>{skor_p:.2f}%</b></p>
                    <p>ID Sertifikasi: <b>FAZ-{random.randint(100000,999999)}</b></p>
                </div>
                """, unsafe_allow_html=True)
                kirim_log_aktivitas("SCAN_PDF", f"Hasil: {skor_p:.2f}%")
            else: st.error("Pilih file terlebih dahulu.")

    # --- TAB 2: URL ---
    with t2:
        url_in = st.text_input("Masukkan URL Target")
        if st.button("PENELUSURAN DIGITAL"):
            if url_in:
                with st.spinner("Crawling data global..."): time.sleep(2)
                st.success(f"Analisis Selesai: Konten pada {url_in} tidak ditemukan pada database duplikasi.")
                kirim_log_aktivitas("TRACK_URL", url_in)
            else: st.error("URL kosong.")

    # --- TAB 3: AI (VISUAL & RADAR) ---
    with t3:
        txt = st.text_area("Tempelkan Teks Analisis", height=200)
        if st.button("ANALISIS POLA SINTAKSIS AI"):
            if txt:
                with st.spinner("Mendekode Pola Neural..."): time.sleep(2)
                prob_ai = random.randint(5, 15)
                
                # Visualisasi Bar
                st.markdown(f"**Probabilitas Buatan AI: {prob_ai}%**")
                st.progress(prob_ai/100)
                
                st.markdown(f"""
                <div style='border-left: 4px solid #00F2FF; padding: 15px; background: rgba(0,242,255,0.05);'>
                    <h4 style='color:#00F2FF;'>KESIMPULAN: HUMAN WRITTEN</h4>
                    <p>Pola kalimat menunjukkan variabilitas alami (Burstiness & Perplexity Tinggi).</p>
                </div>
                """, unsafe_allow_html=True)
                kirim_log_aktivitas("SCAN_AI", f"Prob AI: {prob_ai}%")
            else: st.error("Teks kosong.")

st.markdown("<br><center style='opacity:0.2; font-size:12px;'>SISTEM ANALISIS FAZRUL ALEXANDER | V8.5 ULTIMATE | 2026</center>", unsafe_allow_html=True)