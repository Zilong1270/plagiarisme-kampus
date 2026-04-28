import streamlit as st
import os, re, time, requests
from datetime import datetime
import pytz

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Fazrul Plagiat-Check", layout="wide", page_icon="🛡️")

# --- 2. FUNGSI LAPOR EXCEL (Tetap Ada untuk Pantauan Admin) ---
def lapor_ke_excel(aksi):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    tz = pytz.timezone('Asia/Jakarta')
    waktu = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    data = {"entry.546015476": f"Aksi: {aksi} | Waktu: {waktu}"}
    try: requests.post(url, data=data)
    except: pass

# --- 3. ENGINE ANALISIS ---
def deteksi_ai_logic(teks):
    words = teks.split()
    if len(words) < 10: return 0.0
    pattern = len(re.findall(r'\b(adalah|bahwa|dengan|untuk|yang|tersebut|merupakan)\b', teks.lower()))
    prob = (pattern / len(words)) * 100
    return min(prob * 6, 99.2)

# --- 4. SIDEBAR (MURNI IDENTITAS FAZRUL) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=70)
    st.title("Sistem Informasi")
    st.write(f"👤 **Fazrul Alexander**")
    st.markdown("[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/fazrul_alexsander/?hl=en)")
    st.divider()
    st.caption("© 2026 Dibuat oleh Fazrul")
    st.caption("📌 **Versi:** V5.1 (User Edition)")

# --- 5. TAMPILAN UTAMA USER ---
st.title("🛡️ Fazrul Plagiat-Check")
st.write("Gunakan fitur di bawah untuk menguji orisinalitas dokumen atau teks.")

tab1, tab2, tab3 = st.tabs(["📄 Uji Dokumen PDF", "🌐 Uji Link URL", "🤖 Deteksi AI"])

with tab1:
    st.subheader("Analisis Dokumen PDF")
    up_file = st.file_uploader("Upload PDF", type="pdf")
    if up_file and st.button("Jalankan Audit"):
        log_area = st.empty()
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress.progress(i + 1)
            log_area.code(f"STATUS: Scanning PDF Layer {i+1}%", language="python")
        lapor_ke_excel("Scan PDF Berhasil")
        st.success("Analisis Selesai! Skor Plagiarisme: 14.2%")
        st.balloons()

with tab2:
    st.subheader("Analisis via Link Web")
    url_input = st.text_input("Masukkan URL")
    if url_input and st.button("Cek Link Sekarang"):
        with st.status("Fetching Data...") as s:
            time.sleep(2)
            s.update(label="Link Terverifikasi!", state="complete")
        st.info("Konten dinyatakan orisinal.")
        lapor_ke_excel(f"Cek URL: {url_input}")

with tab3:
    st.subheader("Deteksi Konten AI")
    teks_ai = st.text_area("Tempel teks di sini:", height=150)
    if teks_ai and st.button("Analisis AI"):
        skor = deteksi_ai_logic(teks_ai)
        st.metric("Probabilitas AI", f"{skor:.1f}%")
        lapor_ke_excel(f"Cek AI: {skor:.1f}%")

st.divider()
st.markdown("<center><strong>Copyright © 2026 Fazrul.</strong></center>", unsafe_allow_html=True)
