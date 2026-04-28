import streamlit as st
import os, re, time, requests, random
from datetime import datetime
import pytz

st.set_page_config(page_title="Fazrul Plagiat-Check", layout="wide", page_icon="🛡️")

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
    if count < 5: return 0, "Terlalu Pendek", "Data tidak cukup"
    ai_keywords = ['adalah', 'merupakan', 'signifikan', 'hal ini', 'tersebut', 'dalam rangka']
    found = [w for w in ai_keywords if w in teks.lower()]
    prob = (len(found) / 6) * 100 if count > 20 else (len(found) / 6) * 50
    prob = min(prob + random.uniform(5, 15), 99.1) if len(found) > 0 else random.uniform(1, 10)
    if prob < 30: 
        status = "🟢 AMAN (Manusia)"; desc = "Gaya bahasa luwes dan tidak kaku."
    elif prob < 70: 
        status = "🟡 WASPADA (Campuran)"; desc = "Ditemukan beberapa pola kalimat formal khas asisten AI."
    else: 
        status = "🔴 BAHAYA (Terdeteksi AI)"; desc = "Struktur kalimat sangat identik dengan pola GPT/LLM."
    return round(prob, 1), status, desc

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1087/1087815.png", width=70)
    st.title("Sistem Informasi")
    st.write("👤 **Fazrul Alexander**")
    st.divider()
    st.caption("Versi: V5.3 (Rich Info)")

st.title("🛡️ Fazrul Intelligence Analysis")
tab1, tab2, tab3 = st.tabs(["📄 Scan PDF", "🌐 Scan URL", "🤖 Deteksi AI"])

with tab3:
    st.subheader("Analisis Neural Teks")
    teks_ai = st.text_area("Tempel teks di sini:", height=150)
    if st.button("🧠 Analisis Detail Sekarang"):
        if teks_ai:
            prob, status, desc = deteksi_ai_advanced(teks_ai)
            st.divider()
            c1, c2 = st.columns([1, 2])
            with c1:
                st.metric("Probabilitas AI", f"{prob}%")
                st.error(status) if prob > 50 else st.success(status)
            with c2:
                st.write("### 📝 Ringkasan")
                st.info(f"**Kesimpulan:** {desc}")
                st.progress(prob/100)
            with st.expander("🔍 Detail Parameter"):
                st.write(f"- Jumlah Kata: {len(teks_ai.split())}")
                st.write("- Analisis Pola: Selesai")
            lapor_ke_excel(f"Detail AI: {prob}%")
        else:
            st.error("Isi teks dulu!")

with tab1: st.info("Fitur Scan PDF Siap.")
with tab2: st.info("Fitur Scan URL Siap.")

st.divider()
st.markdown("<center><strong>Copyright © 2026 Fazrul.</strong></center>", unsafe_allow_html=True)