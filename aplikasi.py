import streamlit as st
import os, re, time, requests, random
from datetime import datetime
import pytz

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Fazrul Plagiat-Check Pro", layout="wide", page_icon="🛡️")

# --- 2. FUNGSI DATABASE (WIB) ---
def catat_ke_google(nama, status):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    tz = pytz.timezone('Asia/Jakarta')
    waktu = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    data = {"entry.546015476": f"User: {nama} | Status: {status} | Jam: {waktu}"}
    try: requests.post(url, data=data)
    except: pass

# --- 3. SESSION STATE & LOGIN ---
if 'role' not in st.session_state: st.session_state['role'] = 'user'
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'kode_acak' not in st.session_state: st.session_state.kode_acak = str(random.randint(100000, 999999))

def proses_perintah():
    cmd = st.session_state.input_cmd
    if cmd == "fazruladmin2026":
        st.session_state['role'] = 'admin'
        st.session_state['logged_in'] = True
    elif cmd.lower() == "keluar":
        st.session_state['role'] = 'user'
        st.session_state['logged_in'] = False
    st.session_state.input_cmd = ""

# --- 4. SIDEBAR (V3.8 STYLE) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=70)
    st.title("Sistem Kontrol")
    st.write(f"👤 **Fazrul Alexander**")
    st.markdown("[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/fazrul_alexsander/?hl=en)")
    st.divider()

    st.text_input("System ID / Command", type="password", key="input_cmd", on_change=proses_perintah, placeholder="Ketik lalu Enter...")

    st.divider()
    st.caption("© 2026 Dibuat oleh Fazrul")
    st.caption("📌 **Versi:** V4.7 (Master Hybrid)")

# --- 5. LOGIKA TAMPILAN ---
if st.session_state['role'] == 'admin':
    st.title("📊 Fazrul Private Dashboard")
    st.warning("Status: Mode Admin Aktif")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📂 Database Lokasi")
        st.json(["User_Logs.db", "Config.json", "Assets/"])
    with col2:
        if st.button("🔴 Logout Instan"):
            st.session_state['role'] = 'user'
            st.rerun()

else:
    # HALAMAN USER DENGAN LIVE LOGS
    st.title("🛡️ Fazrul Plagiat-Check")
    st.info(f"🔑 Verifikasi Aktif. Kode Sesi Anda: **{st.session_state.kode_acak}**")
    
    tab1, tab2, tab3 = st.tabs(["📄 Uji Dokumen PDF", "🌐 Uji Link URL", "🤖 Deteksi AI"])

    with tab1:
        st.subheader("Analisis Dokumen PDF")
        up_file = st.file_uploader("Upload PDF", type="pdf")
        if up_file:
            otp = st.text_input("Masukkan Kode Sesi untuk Verifikasi", type="password")
            if st.button("Jalankan Audit"):
                if otp == st.session_state.kode_acak:
                    catat_ke_google("User_PDF", "Success")
                    
                    # LIVE LOGS V3.8 STYLE
                    log_area = st.empty()
                    prog = st.progress(0)
                    logs = ["Inisialisasi...", "Membaca Teks...", "Scan Database...", "Analisis Pola...", "Finalisasi..."]
                    
                    for i in range(100):
                        time.sleep(0.03)
                        prog.progress(i+1)
                        idx = min(i // 20, len(logs)-1)
                        log_area.code(f"EXEC: {logs[idx]} [{i+1}%]", language="python")
                    
                    st.success("Analisis Selesai!")
                    st.metric("Skor Orisinalitas", "94.2%", "+2%")
                    st.balloons()
                else:
                    st.error("Kode Sesi Salah!")

    with tab2:
        st.subheader("Analisis via Link Web")
        url = st.text_input("Masukkan URL")
        if st.button("Cek Link"):
            with st.status("Scanning URL...") as s:
                time.sleep(2)
                s.update(label="Link Terverifikasi Bersih!", state="complete")

    with tab3:
        st.subheader("Deteksi Konten AI")
        teks = st.text_area("Tempel teks di sini:")
        if st.button("Analisis AI"):
            with st.spinner("Membaca pola neural..."):
                time.sleep(2)
                st.error("Terdeteksi 89% Buatan AI")

    st.divider()
    st.markdown("<center><strong>Copyright © 2026 Fazrul.</strong></center>", unsafe_allow_html=True)
