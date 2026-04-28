import streamlit as st
import requests
import time
import random
from datetime import datetime
import pytz

st.set_page_config(page_title="Fazrul Anti-Plagiat", layout="wide", page_icon="🛡️")

def catat_ke_google(nama, otp):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    tz_jakarta = pytz.timezone('Asia/Jakarta')
    waktu_sekarang = datetime.now(tz_jakarta).strftime('%d/%m/%Y %H:%M:%S')
    data = {"entry.546015476": f"User: {nama} | OTP: {otp} | Login: {waktu_sekarang}"}
    try: requests.post(url, data=data)
    except: pass

if 'step' not in st.session_state: st.session_state.step = "input_nama"
if 'kode_acak' not in st.session_state: st.session_state.kode_acak = str(random.randint(100000, 999999))

if st.session_state.step == "input_nama":
    st.title("🛡️ Portal Fazrul")
    nama = st.text_input("Masukkan Nama Anda")
    if st.button("Dapatkan Kode"):
        if nama:
            st.session_state.temp_nama = nama
            st.session_state.kode_acak = str(random.randint(100000, 999999))
            st.session_state.step = "input_otp"
            st.rerun()

elif st.session_state.step == "input_otp":
    st.title("🔑 Verifikasi")
    st.warning(f"KODE OTP: {st.session_state.kode_acak}")
    input_otp = st.text_input("Masukkan Kode")
    if st.button("Masuk"):
        if input_otp == st.session_state.kode_acak:
            catat_ke_google(st.session_state.temp_nama, st.session_state.kode_acak)
            st.session_state.user = st.session_state.temp_nama
            st.session_state.step = "dashboard"
            st.rerun()

elif st.session_state.step == "dashboard":
    with st.sidebar:
        st.success(f"👤 {st.session_state.user}")
        if st.button("Logout"):
            st.session_state.step = "input_nama"
            st.rerun()
    
    st.title("🚀 Fazrul Plagiat-Check")
    tab1, tab2, tab3 = st.tabs(["📄 Scan PDF", "🌐 Cek URL", "🤖 Deteksi AI"])
    
    with tab1: st.file_uploader("Upload PDF", type="pdf")
    with tab2: st.text_input("Masukkan Link")
    with tab3: st.text_area("Tempel teks")

    # --- FOOTER SIMPEL ---
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: grey;'>
            <p><strong>Copyright © 2026 Fazrul. All Rights Reserved.</strong></p>
        </div>
        """, 
        unsafe_allow_html=True
    )
