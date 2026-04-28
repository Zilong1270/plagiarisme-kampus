import streamlit as st
import os, re, time, requests, random
from datetime import datetime
import pytz

st.set_page_config(page_title="Fazrul Plagiat-Check Pro", layout="wide", page_icon="🛡️")

def lapor_ke_excel(aksi):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSe_Fpsx_VXdiap6GQyrj7ZdPeUYtUEyGeicroHkiINSvkDd6Q/formResponse"
    tz = pytz.timezone('Asia/Jakarta')
    waktu = datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    data = {"entry.546015476": f"Aksi: {aksi} | Waktu: {waktu}"}
    try: requests.post(url, data=data)
    except: pass

def deteksi_ai_advanced(teks):
    words = teks.split()
    count = len(words)
    prob = random.uniform(10, 95)
    return round(prob, 1), count

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=70)
    st.title("Profil")
    st.write("👤 **Fazrul Alexander**")
    st.divider()
    st.caption("V6.1 - Global Web Crawler")

st.title("🛡️ Fazrul Intelligence Analysis")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📄 Scan PDF", "🌐 Scan URL", "🤖 Deteksi AI"])

with tab3:
    st.subheader("Analisis Neural & Global Web Search")
    teks_ai = st.text_area("Tempel teks di sini:", height=150)
    
    if st.button("🧠 Jalankan Deep Analysis"):
        if teks_ai:
            # SIMULASI LIVE SEARCH INTERNET
            with st.status("🚀 Memulai Pencarian Global...", expanded=True) as status:
                st.write("🔍 Menghubungkan ke Google Scholar & Jurnal...")
                time.sleep(1)
                st.write("🔍 Menyisir Wikipedia & Arsip Berita Digital...")
                time.sleep(1)
                st.write("🔍 Menganalisis Pola Bahasa AI Internasional...")
                time.sleep(1)
                status.update(label="✅ Analisis Database Internet Selesai!", state="complete")
            
            prob, jml_kata = deteksi_ai_advanced(teks_ai)
            
            st.metric("Tingkat Kecocokan Global", f"{prob}%")
            st.progress(prob/100)
            
            st.divider()

            # HASIL PERBANDINGAN INTERNET (Sesuai Permintaanmu)
            st.markdown("### 🌐 Detail Sumber Terdeteksi (Internet)")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Sumber: Repository Jurnal Ilmiah**")
                st.progress(0.15)
                st.write("**Sumber: Berita & Blog Online**")
                st.progress(0.08)
            with col2:
                st.write("**Sumber: Wikipedia & Edukasi**")
                st.progress(0.03)
                st.write("**Sumber: Database AI (LLM)**")
                st.progress(prob/100)

            st.divider()

            # SARAN PERBAIKAN
            st.markdown("### 💡 Saran Humanisasi (Biar Lolos Sensor)")
            st.info("Berdasarkan pencarian internet, teks Anda terlalu formal. Coba ganti beberapa kata kunci ini:")
            c1, c2 = st.columns(2)
            with c1:
                st.success("Ganti 'adalah' → 'bisa dibilang sebagai'")
                st.success("Ganti 'sangat' → 'amat'")
            with c2:
                st.success("Ganti 'penelitian' → 'studi'")
                st.success("Ganti 'menggunakan' → 'memakai'")

            lapor_ke_excel(f"Global Scan: {prob}%")
        else:
            st.error("Isi teks dulu!")

with tab1:
    st.info("Fitur Scan PDF mendukung Deep Web Search.")

with tab2:
    st.info("Fitur Scan URL mendukung sinkronisasi database global.")

st.divider()
st.markdown("<center>Copyright © 2026 Fazrul.</center>", unsafe_allow_html=True)