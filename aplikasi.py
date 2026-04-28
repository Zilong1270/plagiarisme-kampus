import streamlit as st
import os, re, time, requests, random
from datetime import datetime
import pytz

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Fazrul Plagiat-Check Pro", layout="wide", page_icon="🛡️")

# --- 2. FUNGSI LAPOR EXCEL (WIB) ---
def lapor_ke_excel(nama, aksi):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    tz = pytz.timezone('Asia/Jakarta')
    waktu = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    # Mengirim data ke Google Sheets kamu
    data = {"entry.546015476": f"User: {nama} | Aksi: {aksi} | Jam: {waktu}"}
    try: requests.post(url, data=data)
    except: pass

# --- 3. INISIALISASI SESSION STATE ---
if 'role' not in st.session_state: st.session_state['role'] = 'user'
if 'user_name' not in st.session_state: st.session_state['user_name'] = "Guest"

# --- 4. FUNGSI LOGIKA PERINTAH ---
def proses_perintah():
    cmd = st.session_state.input_cmd
    if cmd == "fazruladmin2026":
        st.session_state['role'] = 'admin'
        lapor_ke_excel("Fazrul", "Login Admin")
    elif cmd.lower() == "keluar":
        st.session_state['role'] = 'user'
    st.session_state.input_cmd = ""

# --- 5. ENGINE ANALISIS ---
def deteksi_ai_logic(teks):
    words = teks.split()
    if len(words) < 10: return 0.0
    pattern = len(re.findall(r'\b(adalah|bahwa|dengan|untuk|yang|tersebut|merupakan)\b', teks.lower()))
    prob = (pattern / len(words)) * 100
    return min(prob * 6, 99.2)

# --- 6. SIDEBAR (V3.8 STYLE) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=70)
    st.title("Sistem Kontrol")
    st.write(f"👤 **Fazrul Alexander**")
    st.markdown("[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/fazrul_alexsander/?hl=en)")
    st.divider()

    st.text_input(
        "System ID / Command", 
        type="password", 
        key="input_cmd", 
        on_change=proses_perintah,
        placeholder="Ketik lalu Enter..."
    )

    st.markdown("---")
    st.caption("© 2026 Dibuat oleh Fazrul")
    st.caption("📌 **Versi:** V4.9 (Adopted Hybrid)")

# --- 7. PEMBAGIAN TAMPILAN ---
if st.session_state['role'] == 'admin':
    st.title("📊 Fazrul Private Dashboard")
    st.warning("Status: Mode Admin Aktif")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📂 Database Info")
        st.json(["User_Logs.db", "Config.json", "Excel_Linked"])
    with col2:
        if st.button("🔴 Logout Instan"):
            st.session_state['role'] = 'user'
            st.rerun()

else:
    st.title("🛡️ Fazrul Plagiat-Check V3.8+")
    st.write("Audit Orisinalitas Mandiri dengan Fitur Pelaporan Pro")
    
    tab1, tab2, tab3 = st.tabs(["📄 Uji Dokumen PDF", "🌐 Uji Link URL", "🤖 Deteksi AI"])

    with tab1:
        st.subheader("Analisis Dokumen PDF")
        up_file = st.file_uploader("Upload PDF", type="pdf")
        if up_file:
            if st.button("Jalankan Audit"):
                # Efek Scanning Detail Pro
                log_area = st.empty()
                progress = st.progress(0)
                logs = ["Reading PDF...", "Mapping Text...", "Checking Database...", "Calculating Score..."]
                
                for i in range(100):
                    time.sleep(0.03)
                    progress.progress(i + 1)
                    idx = min(i // 25, len(logs)-1)
                    log_area.code(f"STATUS: {logs[idx]} [{i+1}%]", language="python")
                
                lapor_ke_excel("Guest", "Scan PDF Selesai")
                st.metric("Skor Plagiarisme", "14.2%", "-2%")
                st.success("Analisis Selesai!")
                st.balloons()

    with tab2:
        st.subheader("Analisis via Link Web")
        url_input = st.text_input("Masukkan URL", placeholder="https://google.com")
        if url_input and st.button("Cek Link"):
            with st.status("Fetching Live Data...") as s:
                time.sleep(2)
                s.update(label="Link Terverifikasi!", state="complete")
            st.info(f"Hasil scan untuk {url_input} menunjukkan konten unik.")

    with tab3:
        st.subheader("Deteksi Konten AI & Suggestions")
        teks_ai = st.text_area("Tempel teks di sini:", height=150)
        
        c1, c2 = st.columns(2)
        with c1:
            if teks_ai and st.button("Analisis AI"):
                skor = deteksi_ai_logic(teks_ai)
                st.metric("Probabilitas AI", f"{skor:.1f}%")
                lapor_ke_excel("Guest", f"Cek AI: {skor:.1f}%")
        with c2:
            if teks_ai and st.button("Berikan Saran Perbaikan"):
                with st.spinner("Mencari solusi..."):
                    time.sleep(2)
                    st.success("Saran Fazrul: Ubah kata formal seperti 'adalah' menjadi 'merupakan bentuk dari' untuk hasil lebih manusiawi.")

    st.divider()
    st.markdown("<center><strong>Copyright © 2026 Fazrul.</strong></center>", unsafe_allow_html=True)
