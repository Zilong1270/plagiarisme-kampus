import streamlit as st
import pandas as pd

st.set_page_config(page_title="Admin Panel Fazrul", layout="wide")
st.title("📊 Monitoring User (Google Sheets)")

# GANTI LINK DI BAWAH INI DENGAN LINK GOOGLE SHEETS KAMU
# Jangan lupa ujungnya diganti /export?format=csv
URL_SHEET = "MASUKKAN_LINK_GOOGLE_SHEETS_KAMU_DISINI"

pw = st.sidebar.text_input("Password Admin", type="password")
if pw == "fazruladmin2026":
    if URL_SHEET == "MASUKKAN_LINK_GOOGLE_SHEETS_KAMU_DISINI":
        st.info("Admin siap. Silakan masukkan link Google Sheets di dalam kode admin.py")
    else:
        try:
            df = pd.read_csv(URL_SHEET)
            st.dataframe(df, use_container_width=True)
            if st.button("Perbarui Data"):
                st.rerun()
        except:
            st.error("Gagal membaca data. Pastikan link Sheets sudah 'Public' (Anyone with link).")
else:
    st.warning("Akses Terbatas. Masukkan Password.")
