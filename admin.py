import streamlit as st
import pandas as pd
import plotly.express as px # Untuk grafik keren

st.set_page_config(page_title="Admin Pro Fazrul", layout="wide", page_icon="📊")

# URL Excel kamu yang sudah dikonversi
URL_SHEET = "https://docs.google.com/spreadsheets/d/1iYY_yH7RtrPx57zI0scNoONf9qhvc4AARENtk_6SQkw/export?format=csv"

st.title("📊 Control Center Admin")

with st.sidebar:
    st.header("🔐 Verifikasi")
    pw = st.text_input("Password Admin", type="password")
    st.divider()
    st.write("Status Server: **Aktif**")

if pw == "fazruladmin2026":
    try:
        # Load Data
        df = pd.read_csv(URL_SHEET)
        
        # --- BAGIAN 1: RINGKASAN DATA ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Kunjungan", len(df))
        with col2:
            # Menghitung user unik (berdasarkan nama di dalam teks entry)
            st.metric("Aktivitas Hari Ini", len(df)) # Bisa difilter per tanggal nanti
        with col3:
            st.metric("Status Database", "Tersambung")

        st.divider()

        # --- BAGIAN 2: TABEL & ANALISIS ---
        tab1, tab2 = st.tabs(["📝 Daftar Log Lengkap", "📈 Grafik Aktivitas"])
        
        with tab1:
            st.subheader("Detail Jejak Digital")
            st.dataframe(df, use_container_width=True)
            
            # Tombol Download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Laporan (.csv)",
                data=csv,
                file_name='laporan_fazrul_plagiat.csv',
                mime='text/csv',
            )

        with tab2:
            st.subheader("Visualisasi Data")
            if not df.empty:
                # Contoh grafik simpel berdasarkan jumlah baris
                fig = px.line(df, y=df.index, title="Tren Penggunaan Aplikasi")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Belum ada data untuk dibuat grafik.")

    except Exception as e:
        st.error("Gagal sinkronisasi dengan Google Sheets.")
        st.info("Pastikan link Excel masih aktif dan publik.")
else:
    st.warning("Masukkan password untuk melihat data rahasia.")
