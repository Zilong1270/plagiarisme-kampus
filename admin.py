import streamlit as st
import pandas as pd

st.set_page_config(page_title="Admin Panel Fazrul", layout="wide", page_icon="📊")

st.title("📊 Panel Monitoring Admin")
st.write("Data login user dari Google Sheets berhasil terhubung.")

# Link sakti hasil konversi terminal
URL_SHEET = "https://docs.google.com/spreadsheets/d/1iYY_yH7RtrPx57zI0scNoONf9qhvc4AARENtk_6SQkw/export?format=csv"

with st.sidebar:
    st.header("🔑 Keamanan")
    pw = st.text_input("Password Admin", type="password")
    st.divider()
    st.caption("v4.5 - Monitoring System")

if pw == "fazruladmin2026":
    st.subheader("📑 Daftar Jejak User (Real-Time)")
    try:
        # Mengambil data dari Google Sheets
        df = pd.read_csv(URL_SHEET)
        
        # Menampilkan tabel data
        st.dataframe(df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Segarkan Data"):
                st.rerun()
        with col2:
            st.write(f"**Total Aktivitas:** {len(df)} entri")
            
    except Exception as e:
        st.error("Gagal terhubung ke Database.")
        st.info("Pastikan di Google Sheets kamu sudah klik 'Bagikan' -> 'Siapa saja yang memiliki link'.")
else:
    st.warning("Silakan masukkan password admin untuk membuka data.")
