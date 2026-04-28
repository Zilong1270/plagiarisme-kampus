import streamlit as st
import pandas as pd

st.set_page_config(page_title="Admin Panel Fazrul", layout="wide", page_icon="📊")

st.title("📊 Panel Monitoring Admin")
st.write("Pantau jejak digital user secara real-time.")

# Link otomatis dari terminal
URL_SHEET = "LINK_GOOGLE_SHEETS_KAMU"

# Sidebar untuk keamanan
with st.sidebar:
    st.header("Konfigurasi")
    pw = st.text_input("Password Admin", type="password")
    st.divider()
    st.caption("v4.5 - Monitoring System")

if pw == "fazruladmin2026":
    st.subheader("📑 Buku Tamu Digital (Google Sheets)")
    
    try:
        # Mengambil data dari Google Sheets
        df = pd.read_csv(URL_SHEET)
        
        # Menampilkan tabel dengan desain yang bagus
        st.dataframe(
            df, 
            use_container_width=True, 
            column_config={
                "Timestamp": "Waktu Input",
                "entry.546015476": "Detail Aktivitas User"
            }
        )
        
        # Tombol Refresh dan Statistik Simpel
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Segarkan Data"):
                st.rerun()
        with col2:
            st.write(f"**Total Aktivitas:** {len(df)} entri")

    except Exception as e:
        st.error("Gagal terhubung ke Database.")
        st.info("Pastikan link Google Sheets sudah di-share 'Public' (Anyone with link).")
else:
    st.warning("Silakan masukkan password admin untuk membuka data.")
