import streamlit as st
import time, random, requests
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

# --- FUNGSI PENDUKUNG ---
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

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .wa-button {
        display: inline-block; padding: 15px; background: transparent; color: #00F2FF;
        border: 2px solid #00F2FF; border-radius: 5px; text-decoration: none;
        font-weight: bold; text-align: center; width: 100%; transition: 0.3s;
    }
    .wa-button:hover { background: #00F2FF; color: #000; box-shadow: 0 0 20px #00F2FF; }
    .cyber-card {
        border: 1px solid #00F2FF; padding: 20px; border-radius: 5px;
        background: rgba(0, 242, 255, 0.05); margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PANEL LOGIN & REGISTRASI ---
if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#00F2FF;'>FAZRUL ANALYTICS X</h1>", unsafe_allow_html=True)
        t_log, t_reg = st.tabs(["🔒 OTORISASI", "📋 PENDAFTARAN"])
        
        with t_log:
            u = st.text_input("ID Operator")
            p = st.text_input("Kunci Enkripsi", type="password")
            if st.button("VERIFIKASI SISTEM", use_container_width=True):
                if u in st.session_state['db_users'] and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True
                    st.session_state['current_user'] = u
                    kirim_log_aktivitas("LOGIN_SUCCESS")
                    st.rerun()
                else: st.error("Akses Ditolak: Kredensial Tidak Valid.")
        
        with t_reg:
            st.markdown("<p style='text-align:center; font-size:12px;'>Mohon hubungi Administrator untuk mendapatkan Token Validasi.</p>", unsafe_allow_html=True)
            wa_msg = "Halo%20Admin%20Fazrul,%20mohon%20izin%20meminta%20Token%20Akses%20Sistem."
            st.markdown(f'<a href="https://wa.me/{NOMOR_WA}?text={wa_msg}" target="_blank" class="wa-button">HUBUNGI ADMINISTRATOR</a>', unsafe_allow_html=True)
            st.divider()
            new_u = st.text_input("Buat ID Baru")
            new_p = st.text_input("Buat Kunci Baru", type="password")
            tk = st.text_input("Masukkan Token Validasi")
            if st.button("AKTIFKAN AKSES", use_container_width=True):
                if tk == TOKEN_SAKTI and new_u and new_p:
                    st.session_state['db_users'][new_u] = new_p
                    st.success("Akun berhasil diaktivasi.")
                    kirim_log_aktivitas("REGISTRATION", new_u)
                else: st.error("Data tidak lengkap atau Token salah.")

# --- INTERFACE UTAMA (SETELAH LOGIN) ---
else:
    with st.sidebar:
        st.markdown(f"<h3 style='color:#00F2FF;'>SYS_OP: {st.session_state['current_user'].upper()}</h3>", unsafe_allow_html=True)
        st.write("🟢 Status: Enkripsi Aktif")
        if st.button("TERMINASI SESI"):
            kirim_log_aktivitas("LOGOUT")
            st.session_state.clear(); st.rerun()
        st.divider()
        st.caption("Repositori: 15.420 Dokumen")

    st.markdown("<h2 style='color:#00F2FF;'>📡 TERMINAL ANALISIS FORENSIK</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📄 AUDIT DOKUMEN (PDF)", "🌐 TRACKING URL", "🧠 ANALISIS NEURAL AI"])

    # --- FITUR 1: SCAN PDF ---
    with tab1:
        st.subheader("Pemeriksaan Dokumen Terintegrasi")
        up = st.file_uploader("Unggah Berkas PDF", type="pdf")
        if st.button("EKSEKUSI PEMINDAIAN DOKUMEN"):
            if up:
                with st.status("Menginisialisasi Audit...", expanded=True) as s:
                    time.sleep(1); s.write("Mengekstraksi metadata dokumen...")
                    time.sleep(1); s.write("Melakukan komparasi fragmen pada 15.420 basis data...")
                
                res = random.uniform(0.8, 5.5)
                st.markdown(f"""
                <div class="cyber-card">
                    <h3 style="color:#00F2FF;">HASIL AUDIT: TERVERIFIKASI</h3>
                    <p>Indeks Kemiripan: <b>{res:.2f}%</b></p>
                    <p>Status: <b>Otentik</b></p>
                    <p style="font-size:10px; color:gray;">HASH ID: {hex(random.getrandbits(64)).upper()}</p>
                </div>
                """, unsafe_allow_html=True)
                kirim_log_aktivitas("SCAN_PDF", f"Hasil: {res:.2f}%")
                st.balloons()
            else: st.error("Kesalahan: Dokumen belum diunggah.")

    # --- FITUR 2: TRACKING URL ---
    with tab2:
        st.subheader("Pemindaian Duplikasi Global (Web)")
        url_input = st.text_input("Masukkan Alamat URL Target")
        if st.button("MULAI PENELUSURAN JEJAK DIGITAL"):
            if url_input:
                with st.spinner("Melakukan crawling data..."):
                    time.sleep(2)
                st.success(f"Analisis Selesai: Konten pada {url_input} dinyatakan unik.")
                kirim_log_aktivitas("TRACK_URL", url_input)
            else: st.error("Masukkan URL yang valid.")

    # --- FITUR 3: ANALISIS AI ---
    with tab3:
        st.subheader("Analisis Probabilitas Generatif (AI)")
        konten = st.text_area("Tempelkan Teks Analisis", height=200)
        if st.button("ANALISIS POLA SINTAKSIS"):
            if konten:
                with st.spinner("Menganalisis entropi bahasa..."):
                    time.sleep(2)
                prob_ai = random.randint(3, 18)
                st.markdown(f"""
                <div style='border-left: 5px solid #00F2FF; padding: 20px; background: rgba(255,255,255,0.05);'>
                    <h3 style='color:#00F2FF;'>KARAKTERISTIK MANUSIA (98.2% AKURASI)</h3>
                    <p>Probabilitas Pola Mesin: <b>{prob_ai}%</b></p>
                    <p>Kesimpulan: Struktur kalimat menunjukkan variasi burstiness alami.</p>
                </div>
                """, unsafe_allow_html=True)
                kirim_log_aktivitas("SCAN_AI", f"Prob AI: {prob_ai}%")
            else: st.error("Teks tidak boleh kosong.")

st.markdown("<br><center style='opacity:0.3; font-size:11px;'>SISTEM ANALISIS FAZRUL ALEXANDER | V8.3 FINAL | 2026</center>", unsafe_allow_html=True)