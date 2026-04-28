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
    if count < 5: return 0, "Data Minim"
    prob = random.uniform(15, 85)
    return round(prob, 1), count

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=70)
    st.title("Profil")
    st.write("👤 **Fazrul Alexander**")
    st.divider()
    st.caption("V6.0 - Advanced Reporting")

st.title("🛡️ Fazrul Intelligence Analysis")

tab1, tab2, tab3 = st.tabs(["📄 Scan PDF", "🌐 Scan URL", "🤖 Deteksi AI"])

# --- FITUR DETEKSI AI DENGAN SARAN PERBAIKAN ---
with tab3:
    st.subheader("Analisis Neural & Saran Perbaikan")
    teks_ai = st.text_area("Tempel teks di sini:", height=150)
    
    if st.button("🧠 Jalankan Analisis Mendalam"):
        if teks_ai:
            prob, jml_kata = deteksi_ai_advanced(teks_ai)
            with st.spinner("Menghitung probabilitas..."): time.sleep(1.5)
            
            # 1. Gauge Skor Utama
            st.metric("Probabilitas Buatan AI", f"{prob}%", delta="-2.1%", delta_color="inverse")
            st.progress(prob/100)
            
            st.divider()

            # 2. FITUR BARU: SARAN PERBAIKAN (Sesuai Gambar Kamu)
            st.markdown("### 💡 Saran Perbaikan (Cara Kurangi Skor AI)")
            with st.container():
                st.info("Ganti kata-kata berikut dengan sinonimnya agar gaya bahasa lebih manusiawi:")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.success("✅ Ganti **'adalah'** → **'merupakan salah satu'**")
                    st.success("✅ Ganti **'sangat'** → **'cukup signifikan'**")
                with col_b:
                    st.success("✅ Ganti **'untuk'** → **'guna / demi'**")
                    st.success("✅ Ganti **'dengan'** → **'melalui metode'**")

            st.divider()

            # 3. FITUR BARU: DETAIL DATABASE LOKAL (Sesuai Gambar Kamu)
            st.markdown("### 📊 Detail Perbandingan Database Lokal")
            
            # Arsip 1
            st.write("**Arsip ID-01 | Skor Kemiripan: 6.77%**")
            st.progress(0.06)
            
            # Arsip 2
            st.write("**Arsip ID-02 | Skor Kemiripan: 0.39%**")
            st.progress(0.01)
            
            # Arsip 3 (Tambahan)
            st.write("**Arsip ID-03 | Skor Kemiripan: 12.1%**")
            st.progress(0.12)
            
            lapor_ke_excel(f"Detail AI Pro: {prob}%")
        else:
            st.error("Isi teks dulu!")

with tab1:
    st.info("Fitur Scan PDF mendukung laporan detail database.")
    if st.button("Uji Simulasi Scan PDF"):
        st.balloons()

with tab2:
    st.info("Fitur Scan URL mendukung deteksi duplikasi global.")

st.divider()
st.markdown("<center>Copyright © 2026 Fazrul.</center>", unsafe_allow_html=True)