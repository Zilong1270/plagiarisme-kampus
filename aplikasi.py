import streamlit as st
import requests
import time
from datetime import datetime

st.set_page_config(page_title="Fazrul Anti-Plagiat Pro", layout="wide", page_icon="🛡️")

def catat_ke_google(nama):
    # Link Form yang sudah diubah jadi formResponse
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    # Entry ID dari link yang kamu berikan
    data = {"entry.546015476": f"User: {nama} | Waktu: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"}
    try:
        requests.post(url, data=data)
    except:
        pass

if 'user' not in st.session_state:
    st.title("🛡️ Portal Keamanan Fazrul")
    st.subheader("Silakan Login")
    nama = st.text_input("Masukkan Nama atau No HP")
    if st.button("Masuk Sekarang"):
        if nama:
            st.session_state.user = nama
            catat_ke_google(nama)
            st.success(f"Selamat Datang, {nama}!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Nama tidak boleh kosong!")
else:
    with st.sidebar:
        st.success(f"Aktif: {st.session_state.user}")
        if st.button("Log Out"):
            del st.session_state.user
            st.rerun()

    st.title("🛡️ Fazrul Plagiat-Check V4.5")
    tab1, tab2, tab3 = st.tabs(["📄 PDF Scan", "🌐 URL Check", "🤖 AI Detector"])
    
    with tab1:
        st.file_uploader("Upload file dokumen", type="pdf")
    with tab2:
        st.text_input("Tempel link website di sini")
    with tab3:
        st.text_area("Masukkan teks untuk cek indikasi AI")
