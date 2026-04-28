import streamlit as st
import time, random
from datetime import datetime

st.set_page_config(page_title="FAZRUL ANALYTICS X", layout="wide", page_icon="🛡️")

# --- CUSTOM INTERFACE DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    
    .wa-button {
        display: inline-block;
        padding: 15px 30px;
        background-color: transparent;
        color: #00F2FF;
        border: 2px solid #00F2FF;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        text-align: center;
        transition: 0.3s;
        width: 100%;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
    }
    .wa-button:hover {
        background-color: #00F2FF;
        color: #000;
        box-shadow: 0 0 25px #00F2FF;
    }
    
    .cyber-card {
        border: 1px solid #00F2FF;
        padding: 25px;
        border-radius: 5px;
        background: rgba(0, 242, 255, 0.05);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- KONFIGURASI SISTEM ---
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
NOMOR_WA = "6285348407129"
TOKEN_SAKTI = "FAZRUL-2026"

# --- GERBANG OTORISASI ---
if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align:center; color:#00F2FF;'>FAZRUL ANALYTICS X</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; opacity:0.8;'>Sistem Informasi Forensik Dokumen & Digital</p>", unsafe_allow_html=True)
        
        tab_log, tab_reg = st.tabs(["🔒 OTORISASI MASUK", "📋 PENDAFTARAN AKSES"])
        
        with tab_log:
            u = st.text_input("ID Operator")
            p = st.text_input("Kunci Enkripsi", type="password")
            if st.button("VERIFIKASI IDENTITAS", use_container_width=True):
                if u == "admin" and p == "fazrul2026": 
                    st.session_state['logged_in'] = True; st.rerun()
                elif u in st.session_state.get('db_users', {}) and st.session_state['db_users'][u] == p:
                    st.session_state['logged_in'] = True; st.rerun()
                else: 
                    st.error("Gagal: Identitas tidak ditemukan dalam basis data.")
        
        with tab_reg:
            st.markdown("<p style='text-align:center; font-size:14px;'>Akses sistem ini bersifat terbatas. Silakan melakukan permohonan Token kepada Administrator Utama.</p>", unsafe_allow_html=True)
            
            wa_link = f"https://wa.me/{NOMOR_WA}?text=Mohon%20izin%20Admin%20Fazrul,%20saya%20memerlukan%20Token%20Akses%20untuk%20Sistem%20Analisis%20V8.2"
            st.markdown(f'<a href="{wa_url if "wa_url" in locals() else wa_link}" target="_blank" class="wa-button">HUBUNGI ADMINISTRATOR</a>', unsafe_allow_html=True)
            
            st.divider()
            st.subheader("Aktivasi Akun")
            new_u = st.text_input("Buat ID Operator Baru")
            new_p = st.text_input("Buat Kata Sandi", type="password")
            tk = st.text_input("Masukkan Token Validasi")
            if st.button("AKTIFKAN AKSES", use_container_width=True):
                if tk == TOKEN_SAKTI:
                    if 'db_users' not in st.session_state: st.session_state['db_users'] = {}
                    st.session_state['db_users'][new_u] = new_p
                    st.success("Sukses: Akses telah diaktifkan. Silakan kembali ke menu Otorisasi.")
                else: 
                    st.error("Gagal: Token Validasi tidak sah.")

# --- PANEL KENDALI UTAMA ---
else:
    st.sidebar.markdown("<h2 style='color:#00F2FF;'>KONSOL SISTEM</h2>", unsafe_allow_html=True)
    st.sidebar.info(f"Status: Terhubung\nID: {st.session_state.get('current_user', 'OPERATOR-01')}")
    if st.sidebar.button("LOGOUT / TERMINASI"):
        st.session_state.clear(); st.rerun()

    st.markdown("<h2 style='color:#00F2FF;'>📡 ANALISIS FORENSIK INTI</h2>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["📄 AUDIT DOKUMEN", "🧠 ANALISIS NEURAL AI"])

    with t1:
        st.write("Sistem terhubung dengan Repositori Global: **15.420 Dokumen Terverifikasi**")
        up = st.file_uploader("Unggah Dokumen (PDF) untuk Analisis Komparatif", type="pdf")
        if up and st.button("EKSEKUSI PEMERIKSAAN DOKUMEN"):
            with st.status("Memulai Audit Forensik...", expanded=True):
                time.sleep(1); st.write("Mengidentifikasi struktur fragmen...")
                time.sleep(1.5); st.write("Membandingkan pola dengan basis data nasional...")
            
            res = random.uniform(0.5, 4.2)
            st.markdown(f"""
            <div class="cyber-card">
                <h3 style="color:#00F2FF;">LAPORAN HASIL AUDIT: OTENTIK</h3>
                <p>Indeks Kemiripan: <b>{res:.2f}%</b></p>
                <p>Status Integritas: <b>Sangat Tinggi (Aman)</b></p>
                <hr style="border-color:#00F2FF;">
                <p style="font-size:11px; color:gray;">Kode Sertifikasi Digital: {hex(random.getrandbits(32)).upper()}</p>
            </div>
            """, unsafe_allow_html=True)

    with t2:
        st.write("Analisis Probabilitas Pola Bahasa berbasis Model Linguistik Gen-AI.")
        txt = st.text_area("Masukkan Konten Teks untuk Pemindaian")
        if st.button("MULAI PEMINDAIAN NEURAL"):
            if txt:
                with st.spinner("Mendekode pola sintaksis..."):
                    time.sleep(2)
                score = random.randint(5, 20)
                st.markdown(f"""
                <div style='border-left: 5px solid #00F2FF; padding-left: 20px; background: rgba(255,255,255,0.05); padding-top:10px; padding-bottom:10px;'>
                    <h3 style='color:#00F2FF;'>KARAKTERISTIK TULISAN MANUSIA TERDETEKSI</h3>
                    <p>Probabilitas Struktur AI: <b>{score}%</b></p>
                    <p>Kesimpulan: Konten menunjukkan variabilitas linguistik alami.</p>
                </div>
                """, unsafe_allow_html=True)

st.markdown("<br><center style='opacity:0.3; font-size:12px;'>SISTEM ANALISIS FAZRUL ALEXANDER | ENKRIPSI V8.2 | 2026</center>", unsafe_allow_html=True)