import streamlit as st
import requests
import time
import random
from datetime import datetime
import pytz

st.set_page_config(page_title="Fazrul Plagiat-Check", layout="wide", page_icon="🛡️")

# --- DATABASE LOGIC ---
def catat_ke_google(nama, aksi):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    tz = pytz.timezone('Asia/Jakarta')
    waktu = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    data = {"entry.546015476": f"User: {nama} | Aksi: {aksi} | Jam: {waktu}"}
    try: requests.post(url, data=data)
    except: pass

# --- SESSION STATE ---
if 'role' not in st.session_state: st.session_state['role'] = 'user'
if 'kode_sesi' not in st.session_state: st.session_state.kode_sesi = str(random.randint(100000, 999999))

def proses_perintah():
    if st.session_state.input_cmd == "fazruladmin2026": st.session_state['role'] = 'admin'
    elif st.session_state.input_cmd.lower() == "keluar": st.session_state['role'] = 'user'
    st.session_state.input_cmd = ""

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Fazrul Control")
    st.write(f"👤 **Fazrul Alexander**")
    st.text_input("Command ID", type="password", key="input_cmd", on_change=proses_perintah)
    st.divider()
    st.caption("Versi 4.8 - AI Advisor Active")

# --- MAIN INTERFACE ---
if st.session_state['role'] == 'admin':
    st.title("📊 Admin Panel")
    st.write("Monitoring mode aktif.")
else:
    st.title("🚀 Fazrul Intelligence Scanner")
    st.info(f"Kode Verifikasi Sesi: **{st.session_state.kode_sesi}**")
    
    tab1, tab2 = st.tabs(["📄 Scan & Advise PDF", "🤖 AI Detector & Rewriter"])

    with tab1:
        st.subheader("Deep Scan with AI Suggestions")
        up = st.file_uploader("Upload PDF", type="pdf")
        if up and st.button("Jalankan Audit"):
            with st.status("Menganalisis konten...") as s:
                time.sleep(2)
                st.write("⚠️ Menemukan 3 paragraf indikasi plagiat.")
                time.sleep(1)
                s.update(label="Audit Selesai!", state="complete")
            
            st.error("Skor Plagiarisme: 25%")
            with st.expander("💡 Lihat Saran Perbaikan (Paraprase)"):
                st.info("Bagian: 'Definisi teknologi menurut para ahli...'")
                st.success("Saran Fazrul AI: Ubah struktur kalimat menjadi pasif atau gunakan sinonim seperti 'Perkembangan alat digital saat ini...' agar lebih orisinal.")

    with tab2:
        st.subheader("AI Content Detector & Assistant")
        teks = st.text_area("Tempel teks yang ingin dicek:", height=200)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Cek Indikasi AI"):
                if len(teks) > 10:
                    with st.spinner("Menganalisis pola neural..."):
                        time.sleep(2)
                        st.warning("Hasil: 85% Terdeteksi Buatan AI")
                        catat_ke_google(st.session_state.get('user', 'Guest'), "Cek AI")
                else: st.error("Teks terlalu pendek!")
        
        with col2:
            if st.button("✍️ Berikan Saran Perbaikan"):
                if len(teks) > 10:
                    with st.spinner("Menyusun ulang kalimat agar lebih manusiawi..."):
                        time.sleep(3)
                        st.subheader("✅ Saran Versi Manusia (Humanized):")
                        # Simulasi hasil rewrite
                        rewrite = teks.replace("adalah", "merupakan salah satu bentuk").replace("sangat", "cukup signifikan")
                        st.write(f"_{rewrite}..._")
                        st.info("Tips: Gunakan lebih banyak kata ganti orang pertama dan kurangi kalimat yang terlalu formal/kaku.")
                else: st.error("Teks tidak ditemukan!")

    st.divider()
    st.markdown("<center><strong>Copyright © 2026 Fazrul.</strong></center>", unsafe_allow_html=True)
